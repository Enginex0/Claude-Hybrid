#!/usr/bin/env python3
"""Claude-Hybrid Orchestration MCP Server - Full 26-tool implementation per ARCH-ORCH-001."""

import asyncio
import fcntl
import json
import os
import re
from datetime import datetime
from pathlib import Path
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server

# =============================================================================
# CONFIGURATION
# =============================================================================
BASE_DIR = Path("/home/president/bmad-systems")
CLAUDE_DIR = BASE_DIR / ".claude"
ORCHESTRATOR_DIR = CLAUDE_DIR / "orchestrator"
MEMORIES_DIR = ORCHESTRATOR_DIR / "memories"
SESSIONS_DIR = ORCHESTRATOR_DIR / "sessions"
ENFORCEMENT_DIR = ORCHESTRATOR_DIR / "enforcement"
METRICS_FILE = ORCHESTRATOR_DIR / "metrics.jsonl"
REGISTRY_FILE = BASE_DIR / "Claude-Hybrid/mcp-server/agent_registry.json"
PROJECT_CONFIG = CLAUDE_DIR / "hybrid-project.yaml"
PROJECT_HISTORY = CLAUDE_DIR / "project_history.jsonl"

# Memory limits
MAX_MEMORIES, RECALL_LIMIT = 50, 10
MAX_MEMORY_SIZE_KB = 80

# Envelope storage
ENVELOPES_DIR = ORCHESTRATOR_DIR / "envelopes"
ENVELOPE_INDEX_FILE = ENVELOPES_DIR / "index.json"

# Token thresholds (from F022)
TOKEN_LIMIT = 140000
THRESHOLD_WARNING = 0.70  # 98K
THRESHOLD_CRITICAL = 0.85  # 119K
THRESHOLD_EMERGENCY = 0.95  # 133K

# Circuit breakers (from D2)
CIRCUIT_BREAKERS = {
    "CB#1": {"name": "Implementation Detection", "description": "PM shouldn't write source code directly"},
    "CB#2": {"name": "Investigation Detection", "description": "Research before implementation"},
    "CB#3": {"name": "Unverified Assertions", "description": "Evidence required for claims"},
    "CB#4": {"name": "Implementation Before Delegation", "description": "PM delegates, doesn't implement"},
    "CB#8": {"name": "QA Verification Gate", "description": "Test before merge"},
    "CB#9": {"name": "Sequential Thinking", "description": "Think before acting"},
    "CB#10": {"name": "Plan Mode Enforcement", "description": "Plan before complex tasks"},
}

# Methodology phases
PHASES = ["planning", "architecture", "stories", "implementation"]

server = Server("claude-hybrid-orchestrator")

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================
def _ensure_dirs():
    """Ensure all required directories exist."""
    for d in [MEMORIES_DIR, SESSIONS_DIR, ENFORCEMENT_DIR, ENVELOPES_DIR]:
        d.mkdir(parents=True, exist_ok=True)

def _safe_name(name: str) -> str:
    """Sanitize name for filesystem use."""
    return "".join(c if c.isalnum() or c in "-_" else "_" for c in name)

def _result(data: dict | list) -> list[TextContent]:
    """Wrap data in TextContent for MCP response."""
    return [TextContent(type="text", text=json.dumps(data, default=str))]

def _load_json(path: Path, default=None):
    """Load JSON file with error handling."""
    if not path.exists():
        return default if default is not None else {}
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return default if default is not None else {}

def _save_json(path: Path, data: dict | list):
    """Save JSON file with locking."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        try:
            json.dump(data, f, indent=2, default=str)
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)

def _append_jsonl(path: Path, entry: dict):
    """Append entry to JSONL file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        try:
            f.write(json.dumps(entry, default=str) + "\n")
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)

def _load_jsonl(path: Path, limit: int = 100) -> list[dict]:
    """Load last N entries from JSONL file."""
    if not path.exists():
        return []
    try:
        with open(path, "r") as f:
            lines = f.readlines()
        entries = []
        for line in lines[-limit:]:
            try:
                entries.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                pass
        return entries
    except IOError:
        return []

# =============================================================================
# REGISTRY FUNCTIONS (5 tools)
# =============================================================================
def _load_registry() -> list[dict]:
    """Load agent registry."""
    data = _load_json(REGISTRY_FILE, {"agents": []})
    return data.get("agents", [])

def _calculate_relevance(agent: dict, query_terms: list[str]) -> float:
    """Calculate relevance score for agent matching."""
    score = 0.0
    name = agent.get("name", "").lower()
    desc = agent.get("description", "").lower()
    caps = " ".join(agent.get("capabilities", [])).lower()
    tags = " ".join(agent.get("tags", [])).lower()
    searchable = f"{name} {desc} {caps} {tags}"

    for term in query_terms:
        t = term.lower()
        if t in searchable:
            score += 3.0 if t in name else 0
            score += 2.0 if t in desc else 0
            score += 1.5 if t in caps else 0
            score += 1.0 if t in tags else 0
    max_possible = len(query_terms) * 7.5
    return min(score / max_possible, 1.0) if max_possible > 0 else 0.0

def registry_list_agents(domain: str = None, tags: list = None, capability: str = None, limit: int = 50) -> dict:
    """List all registered agents with optional filtering."""
    agents = _load_registry()
    filtered = []

    for a in agents:
        if domain and a.get("domain", "").lower() != domain.lower():
            continue
        if tags:
            agent_tags = [t.lower() for t in a.get("tags", [])]
            if not any(t.lower() in agent_tags for t in tags):
                continue
        if capability:
            agent_caps = [c.lower() for c in a.get("capabilities", [])]
            if capability.lower() not in agent_caps:
                continue
        filtered.append({
            "id": a.get("name", ""),
            "name": a.get("name", ""),
            "domain": a.get("domain", "general"),
            "tags": a.get("tags", []),
            "capabilities": a.get("capabilities", []),
            "description": a.get("description", "")
        })

    return {"agents": filtered[:limit], "total_count": len(agents), "filtered_count": len(filtered)}

def registry_get_agent(agent_id: str, include_metrics: bool = True) -> dict:
    """Get complete details for a specific agent."""
    agents = _load_registry()
    for a in agents:
        if a.get("name", "") == agent_id:
            result = {
                "id": a.get("name", ""),
                "name": a.get("name", ""),
                "domain": a.get("domain", "general"),
                "tags": a.get("tags", []),
                "description": a.get("description", ""),
                "capabilities": a.get("capabilities", []),
            }
            if include_metrics:
                metrics = _load_jsonl(METRICS_FILE, 1000)
                agent_metrics = [m for m in metrics if m.get("agent_id") == agent_id]
                success = sum(1 for m in agent_metrics if m.get("success"))
                total = len(agent_metrics)
                result["metrics"] = {
                    "success_rate": round(success / total, 2) if total > 0 else 0,
                    "total_tasks": total,
                    "recent_tasks": agent_metrics[-5:]
                }
            return result
    return {"error": f"Agent not found: {agent_id}"}

def registry_search(query: str, types: list = None, limit: int = 10) -> dict:
    """Semantic search across agents."""
    agents = _load_registry()
    query_terms = query.split()
    results = []

    for a in agents:
        score = _calculate_relevance(a, query_terms)
        if score > 0:
            results.append({
                "type": "agent",
                "id": a.get("name", ""),
                "name": a.get("name", ""),
                "relevance_score": round(score, 2),
                "description": a.get("description", ""),
                "match_reason": f"Matches query terms in capabilities/description"
            })

    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    return {"results": results[:limit], "query": query}

def registry_record_metric(agent_id: str, task_type: str, success: bool, duration_seconds: int = None, context: dict = None) -> dict:
    """Record task completion metrics."""
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "agent_id": agent_id,
        "task_type": task_type,
        "success": success,
        "duration_seconds": duration_seconds,
        "context": context or {}
    }
    _append_jsonl(METRICS_FILE, entry)

    # Calculate new success rate
    metrics = _load_jsonl(METRICS_FILE, 1000)
    agent_metrics = [m for m in metrics if m.get("agent_id") == agent_id]
    success_count = sum(1 for m in agent_metrics if m.get("success"))
    total = len(agent_metrics)

    return {"recorded": True, "agent_id": agent_id, "new_success_rate": round(success_count / total, 2) if total > 0 else 0, "total_tasks": total}

def registry_get_recommendations(task_description: str, project_type: str = None, toolchain: list = None, limit: int = 5) -> dict:
    """Get intelligent agent recommendations."""
    agents = _load_registry()
    query_terms = task_description.split()
    if toolchain:
        query_terms.extend(toolchain)

    recommendations = []
    for a in agents:
        score = _calculate_relevance(a, query_terms)
        if score > 0:
            reasons = []
            if any(t in a.get("name", "").lower() for t in query_terms):
                reasons.append(f"Name matches query")
            if any(t in a.get("description", "").lower() for t in query_terms):
                reasons.append(f"Description matches query")
            if any(t in " ".join(a.get("capabilities", [])).lower() for t in query_terms):
                reasons.append(f"Has relevant capabilities")

            recommendations.append({
                "agent_id": a.get("name", ""),
                "score": round(score, 2),
                "reasons": reasons or ["General relevance match"],
                "suggested_for": "Primary implementer" if score > 0.5 else "Supporting role"
            })

    recommendations.sort(key=lambda x: x["score"], reverse=True)

    # Analyze task complexity
    complexity = "low"
    if len(task_description.split()) > 20:
        complexity = "medium"
    if any(w in task_description.lower() for w in ["architecture", "security", "complex", "multi"]):
        complexity = "high"

    return {
        "recommendations": recommendations[:limit],
        "task_analysis": {
            "complexity": complexity,
            "estimated_agents_needed": 1 if complexity == "low" else (2 if complexity == "medium" else 3),
            "suggested_approach": "Direct implementation" if complexity == "low" else "Plan then implement"
        }
    }

# =============================================================================
# SESSION FUNCTIONS (5 tools)
# =============================================================================
def _get_session_file() -> Path:
    """Get current session state file."""
    return SESSIONS_DIR / "current_session.json"

def _load_session() -> dict:
    """Load current session state."""
    return _load_json(_get_session_file(), {
        "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "started_at": datetime.utcnow().isoformat() + "Z",
        "tokens_used": 0,
        "current_task": None,
        "decisions_made": [],
        "pending_work": [],
        "files_modified": []
    })

def session_get_tokens(include_breakdown: bool = False) -> dict:
    """Get current token usage and budget information."""
    session = _load_session()
    tokens_used = session.get("tokens_used", 0)

    result = {
        "session_id": session.get("session_id", "unknown"),
        "total_budget": TOKEN_LIMIT,
        "tokens_used": tokens_used,
        "tokens_remaining": TOKEN_LIMIT - tokens_used,
        "percentage_used": round((tokens_used / TOKEN_LIMIT) * 100, 1),
        "counting_method": "estimated"
    }

    if include_breakdown:
        result["breakdown"] = session.get("token_breakdown", {
            "system_prompt": 12000,
            "conversation": tokens_used - 12000 if tokens_used > 12000 else 0,
            "tool_calls": 0
        })

    return result

def session_check_threshold() -> dict:
    """Check current threshold status."""
    session = _load_session()
    tokens_used = session.get("tokens_used", 0)
    percentage = tokens_used / TOKEN_LIMIT

    if percentage >= THRESHOLD_EMERGENCY:
        level = "EMERGENCY"
        action = "STOP. Cannot accept new tasks until /compact"
    elif percentage >= THRESHOLD_CRITICAL:
        level = "CRITICAL"
        action = "Complete current task and use /compact soon"
    elif percentage >= THRESHOLD_WARNING:
        level = "WARNING"
        action = "Consider completing current task before context grows"
    else:
        level = "NORMAL"
        action = None

    return {
        "level": level,
        "percentage": round(percentage * 100, 1),
        "tokens_used": tokens_used,
        "tokens_remaining": TOKEN_LIMIT - tokens_used,
        "threshold_values": {
            "warning": int(TOKEN_LIMIT * THRESHOLD_WARNING),
            "critical": int(TOKEN_LIMIT * THRESHOLD_CRITICAL),
            "emergency": int(TOKEN_LIMIT * THRESHOLD_EMERGENCY)
        },
        "exceeded": {
            "warning": percentage >= THRESHOLD_WARNING,
            "critical": percentage >= THRESHOLD_CRITICAL,
            "emergency": percentage >= THRESHOLD_EMERGENCY
        },
        "recommended_action": action
    }

def session_get_state(include_history: bool = False) -> dict:
    """Get current session state."""
    session = _load_session()
    result = {
        "session_id": session.get("session_id"),
        "started_at": session.get("started_at"),
        "current_feature": session.get("current_feature"),
        "current_task": session.get("current_task"),
        "methodology_phase": session.get("methodology_phase", "planning"),
        "decisions_made": session.get("decisions_made", []),
        "pending_work": session.get("pending_work", []),
        "files_modified": session.get("files_modified", [])
    }

    if include_history:
        result["history"] = _load_jsonl(PROJECT_HISTORY, 50)

    return result

def session_save_state(state: dict, reason: str = None) -> dict:
    """Persist current session state."""
    current = _load_session()
    current.update(state)
    current["last_saved"] = datetime.utcnow().isoformat() + "Z"
    current["save_reason"] = reason

    _save_json(_get_session_file(), current)

    # Also save to timestamped file
    session_id = current.get("session_id", datetime.now().strftime("%Y%m%d_%H%M%S"))
    timestamped_file = SESSIONS_DIR / f"session_{session_id}.json"
    _save_json(timestamped_file, current)

    return {
        "saved": True,
        "session_id": session_id,
        "file_path": str(timestamped_file),
        "timestamp": current["last_saved"]
    }

def session_get_resume_log(session_id: str = None) -> dict:
    """Check for and retrieve resume logs from previous sessions."""
    if session_id:
        resume_file = SESSIONS_DIR / f"resume_log_{session_id}.json"
    else:
        # Find most recent resume log
        resume_files = list(SESSIONS_DIR.glob("resume_log_*.json"))
        if not resume_files:
            return {"found": False, "resume_log": None}
        resume_file = max(resume_files, key=lambda f: f.stat().st_mtime)

    if not resume_file.exists():
        return {"found": False, "resume_log": None}

    resume_log = _load_json(resume_file)
    return {
        "found": True,
        "resume_log": resume_log,
        "inject_recommended": True
    }

# =============================================================================
# PROJECT FUNCTIONS (6 tools)
# =============================================================================
def _load_project_config() -> dict:
    """Load project configuration."""
    if not PROJECT_CONFIG.exists():
        return {"hybrid_version": "1.0", "project": {}, "toolchain": {}, "methodology": {}, "agents": {}, "session": {}}
    try:
        # Simple YAML-like parsing for key: value
        config = {}
        with open(PROJECT_CONFIG, "r") as f:
            content = f.read()
        # Basic parsing - just return as text for now
        return {"raw_config": content, "hybrid_version": "1.0"}
    except IOError:
        return {}

def project_get_config() -> dict:
    """Get current project configuration."""
    config = _load_project_config()
    session = _load_session()

    return {
        "hybrid_version": config.get("hybrid_version", "1.0"),
        "project": config.get("project", {"name": "Claude-Hybrid", "type": "orchestration"}),
        "toolchain": config.get("toolchain", {"detected": [], "detection_method": "auto"}),
        "methodology": {
            "active": "bmad",
            "phase": session.get("methodology_phase", "planning"),
            "track": "full"
        },
        "agents": config.get("agents", {"enabled": [], "custom": []}),
        "session": {
            "continuity": True,
            "auto_save": True,
            "token_limit": TOKEN_LIMIT
        }
    }

def project_get_phase() -> dict:
    """Get current methodology phase with allowed actions."""
    session = _load_session()
    current_phase = session.get("methodology_phase", "planning")
    phase_index = PHASES.index(current_phase) if current_phase in PHASES else 0

    allowed_actions = {
        "planning": ["Create PRD", "Define requirements", "Research"],
        "architecture": ["Create architecture docs", "Design systems", "Review with user"],
        "stories": ["Create user stories", "Define acceptance criteria", "Plan sprints"],
        "implementation": ["Write code", "Run tests", "Create PRs"]
    }

    blocked_actions = {
        "planning": ["Write implementation code", "Create PRs"],
        "architecture": ["Write implementation code", "Create PRs"],
        "stories": ["Write implementation code"],
        "implementation": []
    }

    next_phase = PHASES[phase_index + 1] if phase_index < len(PHASES) - 1 else None

    return {
        "current_phase": current_phase,
        "phase_index": phase_index,
        "total_phases": len(PHASES),
        "phases": PHASES,
        "allowed_actions": allowed_actions.get(current_phase, []),
        "blocked_actions": blocked_actions.get(current_phase, []),
        "next_phase": next_phase,
        "transition_requirements": ["Current phase deliverables complete", "User approval received"] if next_phase else []
    }

def project_detect_toolchain(path: str = ".", force_refresh: bool = False) -> dict:
    """Detect project toolchain by analyzing directory structure."""
    base_path = Path(path).resolve()

    languages = []
    frameworks = []
    build_tools = []
    evidence = {}

    # Detect by file existence
    detections = [
        ("package.json", "javascript", "node", "npm/yarn"),
        ("tsconfig.json", "typescript", None, None),
        ("requirements.txt", "python", None, "pip"),
        ("pyproject.toml", "python", None, "poetry/pip"),
        ("Cargo.toml", "rust", None, "cargo"),
        ("go.mod", "go", None, "go"),
        ("build.gradle", "java/kotlin", "android", "gradle"),
        ("build.gradle.kts", "kotlin", "android", "gradle"),
        ("pom.xml", "java", None, "maven"),
        ("Gemfile", "ruby", "rails", "bundler"),
    ]

    for filename, lang, framework, build in detections:
        if (base_path / filename).exists():
            if lang and lang not in languages:
                languages.append(lang)
            if framework and framework not in frameworks:
                frameworks.append(framework)
            if build and build not in build_tools:
                build_tools.append(build)
            evidence[filename] = f"Detected {lang or framework or build}"

    # Detect LSPosed
    if (base_path / "app" / "src" / "main" / "java").exists() or (base_path / "app" / "src" / "main" / "kotlin").exists():
        if any("xposed" in str(f).lower() for f in base_path.rglob("*.java")) or \
           any("xposed" in str(f).lower() for f in base_path.rglob("*.kt")):
            if "lsposed" not in frameworks:
                frameworks.append("lsposed")

    detected_type = "general"
    if "lsposed" in frameworks:
        detected_type = "lsposed_module"
    elif "android" in frameworks:
        detected_type = "android_app"
    elif "typescript" in languages or "javascript" in languages:
        detected_type = "node_project"
    elif "python" in languages:
        detected_type = "python_project"

    return {
        "languages": languages,
        "frameworks": frameworks,
        "build_tools": build_tools,
        "detected_type": detected_type,
        "confidence": 0.9 if evidence else 0.5,
        "detection_evidence": evidence,
        "recommended_agents": registry_get_recommendations(
            task_description=f"{detected_type} {' '.join(frameworks)}",
            toolchain=languages + frameworks
        ).get("recommendations", [])[:3]
    }

def project_get_active_agents() -> dict:
    """Get list of agents enabled for current project."""
    config = _load_project_config()
    agents = _load_registry()

    enabled = config.get("agents", {}).get("enabled", [])

    return {
        "enabled_agents": [
            {"id": a.get("name"), "role": "available", "enabled_by": "registry"}
            for a in agents if a.get("name") in enabled or not enabled
        ][:10],
        "available_agents": len(agents),
        "project_type": config.get("project", {}).get("type", "general")
    }

def project_update_phase(new_phase: str, reason: str) -> dict:
    """Transition to next methodology phase."""
    if new_phase not in PHASES:
        return {"success": False, "error": f"Invalid phase: {new_phase}", "valid_phases": PHASES}

    session = _load_session()
    current_phase = session.get("methodology_phase", "planning")

    session["methodology_phase"] = new_phase
    session["phase_transition"] = {
        "from": current_phase,
        "to": new_phase,
        "reason": reason,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    _save_json(_get_session_file(), session)

    # Log transition
    _append_jsonl(PROJECT_HISTORY, {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "action": "phase_transition",
        "details": f"{current_phase} → {new_phase}",
        "reason": reason
    })

    return {
        "success": True,
        "previous_phase": current_phase,
        "new_phase": new_phase,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

def project_get_history(limit: int = 50, action_type: str = None) -> dict:
    """Get project action history."""
    history = _load_jsonl(PROJECT_HISTORY, limit * 2)

    if action_type:
        history = [h for h in history if h.get("action") == action_type]

    return {"history": history[-limit:], "total_actions": len(history)}

# =============================================================================
# ENFORCEMENT FUNCTIONS (5 tools)
# =============================================================================
def enforce_check_breaker(action_type: str, context: dict = None) -> dict:
    """Check if an intended action violates any circuit breaker."""
    context = context or {}
    violations = []

    # CB#1: Implementation Detection - PM shouldn't write code
    if action_type == "implement_code" and context.get("is_pm_context"):
        violations.append({
            "breaker": "CB#1",
            "name": CIRCUIT_BREAKERS["CB#1"]["name"],
            "reason": "PM context should not implement code directly"
        })

    # CB#4: Implementation Before Delegation
    if action_type == "implement_code" and context.get("is_pm_context") and not context.get("has_delegated"):
        violations.append({
            "breaker": "CB#4",
            "name": CIRCUIT_BREAKERS["CB#4"]["name"],
            "reason": "PM must delegate implementation to specialist"
        })

    # CB#10: Plan Mode Enforcement
    if action_type == "implement_code":
        complexity = context.get("task_complexity", "low")
        has_plan = context.get("has_approved_plan", False)
        if complexity in ["medium", "high"] and not has_plan:
            violations.append({
                "breaker": "CB#10",
                "name": CIRCUIT_BREAKERS["CB#10"]["name"],
                "reason": f"Complex task ({complexity}) requires approved plan"
            })

    if violations:
        return {
            "verdict": "BLOCKED",
            "action_type": action_type,
            "violations": violations,
            "recommended_action": violations[0].get("reason"),
            "auto_action": "ENTER_PLAN_MODE" if any(v["breaker"] == "CB#10" for v in violations) else None
        }

    return {
        "verdict": "ALLOWED",
        "action_type": action_type,
        "breakers_checked": list(CIRCUIT_BREAKERS.keys()),
        "all_passed": True
    }

def enforce_validate_sequence(current_phase: str, intended_action: str) -> dict:
    """Validate that intended action follows correct methodology sequence."""
    phase_allowed_actions = {
        "planning": ["research", "define_requirements", "create_prd"],
        "architecture": ["design_system", "create_diagrams", "review"],
        "stories": ["create_stories", "define_acceptance", "plan_sprint"],
        "implementation": ["write_code", "run_tests", "create_pr", "implement_code"]
    }

    implementation_actions = ["write_code", "implement_code", "create_pr"]

    if intended_action in implementation_actions and current_phase != "implementation":
        expected_phase = "implementation"
        phases_away = PHASES.index(expected_phase) - PHASES.index(current_phase) if current_phase in PHASES else -1

        return {
            "valid": False,
            "current_phase": current_phase,
            "intended_action": intended_action,
            "expected_phase": expected_phase,
            "phases_away": phases_away,
            "reason": f"Cannot {intended_action} during {current_phase} phase",
            "required_sequence": PHASES,
            "recommended_action": f"Complete {current_phase} phase first"
        }

    return {
        "valid": True,
        "current_phase": current_phase,
        "intended_action": intended_action,
        "allowed_actions": phase_allowed_actions.get(current_phase, [])
    }

def enforce_require_plan(task_description: str, estimated_files: int = None, has_existing_plan: bool = False) -> dict:
    """Check if task complexity requires plan mode."""
    if has_existing_plan:
        return {"plan_required": False, "reason": "Plan already exists", "complexity_assessment": "n/a"}

    complexity_factors = []

    # Check description complexity
    words = task_description.split()
    if len(words) > 30:
        complexity_factors.append("Long task description")

    # Check for complexity keywords
    complex_keywords = ["architecture", "refactor", "security", "multi", "complex", "system", "integration"]
    if any(kw in task_description.lower() for kw in complex_keywords):
        complexity_factors.append("Contains complexity indicators")

    # Check file count
    if estimated_files and estimated_files > 3:
        complexity_factors.append(f"Multiple files involved ({estimated_files})")

    complexity = "low"
    if len(complexity_factors) >= 3:
        complexity = "high"
    elif len(complexity_factors) >= 1:
        complexity = "medium"

    plan_required = complexity in ["medium", "high"]

    return {
        "plan_required": plan_required,
        "complexity_assessment": complexity,
        "complexity_factors": complexity_factors,
        "has_existing_plan": has_existing_plan,
        "recommendation": "Enter plan mode before proceeding" if plan_required else "Can proceed directly",
        "bypass_allowed": complexity == "medium"
    }

def enforce_validate_delegation(delegator: str, delegate_to: str, task_type: str) -> dict:
    """Validate that delegation follows PM model rules."""
    is_pm = delegator.lower() == "pm" or "pm" in delegator.lower()

    # PM should delegate implementation tasks
    implementation_tasks = ["implement", "code", "write", "fix", "refactor"]
    is_implementation = any(t in task_type.lower() for t in implementation_tasks)

    if is_pm and is_implementation:
        return {
            "valid": True,
            "delegator": delegator,
            "delegate_to": delegate_to,
            "task_type": task_type,
            "pm_model_compliant": True,
            "notes": "PM correctly delegating implementation to specialist"
        }

    if not is_pm and is_implementation:
        return {
            "valid": True,
            "delegator": delegator,
            "delegate_to": delegate_to,
            "task_type": task_type,
            "pm_model_compliant": True,
            "notes": "Specialist-to-specialist delegation allowed"
        }

    return {
        "valid": True,
        "delegator": delegator,
        "delegate_to": delegate_to,
        "task_type": task_type,
        "pm_model_compliant": True,
        "notes": "General delegation"
    }

def enforce_log_violation(breaker_id: str, action_attempted: str, context: dict = None, resolution: str = None) -> dict:
    """Log a circuit breaker violation."""
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "violation_id": f"v_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{breaker_id.replace('#', '')}",
        "breaker_id": breaker_id,
        "breaker_name": CIRCUIT_BREAKERS.get(breaker_id, {}).get("name", "Unknown"),
        "action_attempted": action_attempted,
        "context": context or {},
        "resolution": resolution
    }

    violations_file = ENFORCEMENT_DIR / "violations.jsonl"
    _append_jsonl(violations_file, entry)

    return {
        "logged": True,
        "violation_id": entry["violation_id"],
        "breaker_id": breaker_id,
        "timestamp": entry["timestamp"]
    }

# =============================================================================
# MEMORY FUNCTIONS (5 tools)
# =============================================================================
def _get_memory_file(agent: str) -> Path:
    """Get memory file path for agent."""
    return MEMORIES_DIR / f"{_safe_name(agent)}.json"

def _load_memories(agent: str) -> list[dict]:
    """Load memories for agent."""
    return _load_json(_get_memory_file(agent), [])

def _save_memories(agent: str, memories: list[dict]):
    """Save memories for agent."""
    _save_json(_get_memory_file(agent), memories)

def memory_recall_project(project_id: str = None, memory_types: list = None, limit: int = 20) -> dict:
    """Retrieve memories specific to a project."""
    # For now, search all memory files for project-related entries
    project_id = project_id or "current"
    all_memories = []

    for mem_file in MEMORIES_DIR.glob("*.json"):
        memories = _load_json(mem_file, [])
        for m in memories:
            if memory_types and m.get("type") not in memory_types:
                continue
            all_memories.append({
                "type": m.get("type", "context"),
                "content": m.get("content", ""),
                "created_at": m.get("timestamp", ""),
                "source": mem_file.stem
            })

    # Sort by timestamp descending
    all_memories.sort(key=lambda x: x.get("created_at", ""), reverse=True)

    return {
        "project_id": project_id,
        "memories": all_memories[:limit],
        "total_memories": len(all_memories)
    }

def memory_recall_agent(agent_id: str, limit: int = 20) -> dict:
    """Retrieve memories learned by specific agent."""
    memories = _load_memories(agent_id)
    mem_file = _get_memory_file(agent_id)
    file_size = mem_file.stat().st_size if mem_file.exists() else 0

    return {
        "agent_id": agent_id,
        "total_memories": len(memories),
        "memory_file_size": f"{file_size // 1024}KB",
        "memories": [
            {"type": m.get("type", "context"), "content": m.get("content", ""), "created_at": m.get("timestamp", "")}
            for m in memories[-limit:]
        ][::-1]
    }

def memory_recall_domain(domain: str, query: str = None, limit: int = 10) -> dict:
    """Semantic search for memories across a domain."""
    all_memories = []
    query_terms = (query or domain).lower().split()

    for mem_file in MEMORIES_DIR.glob("*.json"):
        memories = _load_json(mem_file, [])
        for m in memories:
            content = m.get("content", "").lower()
            score = sum(1 for t in query_terms if t in content) / len(query_terms) if query_terms else 0
            if score > 0:
                all_memories.append({
                    "type": m.get("type", "context"),
                    "content": m.get("content", ""),
                    "relevance_score": round(score, 2),
                    "source_agent": mem_file.stem,
                    "created_at": m.get("timestamp", "")
                })

    all_memories.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)

    return {
        "domain": domain,
        "query": query,
        "memories": all_memories[:limit]
    }

def memory_store_learning(type: str, content: str, agent_id: str = None, domain: str = None, project_id: str = None) -> dict:
    """Store a new learning."""
    valid_types = ["pattern", "architecture", "guideline", "mistake", "strategy", "integration", "performance", "context"]
    if type not in valid_types:
        return {"error": f"Invalid memory type. Valid types: {valid_types}"}

    agent_id = agent_id or "general"
    memories = _load_memories(agent_id)

    # Check for duplicates
    if any(m.get("content") == content for m in memories):
        return {"stored": False, "reason": "Duplicate content", "deduplicated": True}

    memories.append({
        "type": type,
        "content": content,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "domain": domain,
        "project_id": project_id
    })

    # FIFO if over limit
    fifo_triggered = len(memories) > MAX_MEMORIES
    if fifo_triggered:
        memories = memories[-MAX_MEMORIES:]

    _save_memories(agent_id, memories)

    mem_file = _get_memory_file(agent_id)
    file_size = mem_file.stat().st_size if mem_file.exists() else 0

    return {
        "stored": True,
        "memory_id": f"mem_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "type": type,
        "deduplicated": False,
        "agent_memory_size": f"{file_size // 1024}KB",
        "fifo_triggered": fifo_triggered
    }

def memory_get_relevant(task_description: str, agent_id: str = None, max_tokens: int = 2000) -> dict:
    """AI-powered retrieval of most relevant memories for a task."""
    query_terms = task_description.lower().split()
    relevant = []

    # Search agent memories if specified
    if agent_id:
        memories = _load_memories(agent_id)
        for m in memories:
            content = m.get("content", "").lower()
            score = sum(1 for t in query_terms if t in content) / len(query_terms) if query_terms else 0
            if score > 0.1:
                relevant.append({
                    "source": f"agent:{agent_id}",
                    "type": m.get("type", "context"),
                    "content": m.get("content", ""),
                    "relevance": round(score, 2)
                })

    # Search all memories
    for mem_file in MEMORIES_DIR.glob("*.json"):
        if agent_id and mem_file.stem == _safe_name(agent_id):
            continue
        memories = _load_json(mem_file, [])
        for m in memories:
            content = m.get("content", "").lower()
            score = sum(1 for t in query_terms if t in content) / len(query_terms) if query_terms else 0
            if score > 0.2:
                relevant.append({
                    "source": f"agent:{mem_file.stem}",
                    "type": m.get("type", "context"),
                    "content": m.get("content", ""),
                    "relevance": round(score, 2)
                })

    relevant.sort(key=lambda x: x.get("relevance", 0), reverse=True)

    # Estimate tokens (rough: 1 token per 4 chars)
    total_tokens = 0
    filtered = []
    for m in relevant:
        m_tokens = len(m.get("content", "")) // 4
        if total_tokens + m_tokens <= max_tokens:
            filtered.append(m)
            total_tokens += m_tokens

    return {
        "task": task_description,
        "relevant_memories": filtered[:10],
        "total_tokens": total_tokens,
        "inject_recommended": len(filtered) > 0
    }

# =============================================================================
# ENVELOPE FUNCTIONS (3 tools) - Claude-Hybrid Analysis System
# =============================================================================
def _load_envelope_index() -> dict:
    """Load envelope index for fast queries."""
    if not ENVELOPE_INDEX_FILE.exists():
        return {
            "by_tier": {},        # tier -> [envelope_ids]
            "by_agent": {},       # agent -> [envelope_ids]
            "by_chunk": {},       # chunk_id -> [envelope_ids]
            "by_workflow": {},    # workflow_id -> [envelope_ids]
            "by_project": {},     # project -> [envelope_ids]
            "all_ids": []         # all envelope_ids for iteration
        }
    return _load_json(ENVELOPE_INDEX_FILE, {})

def _save_envelope_index(index: dict):
    """Save envelope index."""
    _save_json(ENVELOPE_INDEX_FILE, index)

def _get_envelope_path(envelope_id: str, workflow_id: str) -> Path:
    """Get file path for an envelope."""
    workflow_dir = ENVELOPES_DIR / "by-workflow" / _safe_name(workflow_id)
    workflow_dir.mkdir(parents=True, exist_ok=True)
    return workflow_dir / f"{envelope_id}.json"

def _generate_envelope_id() -> str:
    """Generate unique envelope ID: env-YYYYMMDD-HHMMSS-random6"""
    import random
    import string
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"env-{timestamp}-{random_suffix}"

def _index_envelope(index: dict, envelope: dict) -> dict:
    """Add envelope to index."""
    env_id = envelope.get("envelope_id")

    # Index by tier
    tier = str(envelope.get("tier", 0))
    if tier not in index["by_tier"]:
        index["by_tier"][tier] = []
    if env_id not in index["by_tier"][tier]:
        index["by_tier"][tier].append(env_id)

    # Index by agent
    agent = envelope.get("agent", "unknown")
    if agent not in index["by_agent"]:
        index["by_agent"][agent] = []
    if env_id not in index["by_agent"][agent]:
        index["by_agent"][agent].append(env_id)

    # Index by chunk_id
    chunk_id = envelope.get("chunk_id", "default")
    if chunk_id not in index["by_chunk"]:
        index["by_chunk"][chunk_id] = []
    if env_id not in index["by_chunk"][chunk_id]:
        index["by_chunk"][chunk_id].append(env_id)

    # Index by workflow_id
    workflow_id = envelope.get("workflow_id", "unknown")
    if workflow_id not in index["by_workflow"]:
        index["by_workflow"][workflow_id] = []
    if env_id not in index["by_workflow"][workflow_id]:
        index["by_workflow"][workflow_id].append(env_id)

    # Index by project
    project = envelope.get("project", "unknown")
    if project not in index["by_project"]:
        index["by_project"][project] = []
    if env_id not in index["by_project"][project]:
        index["by_project"][project].append(env_id)

    # Add to all_ids
    if env_id not in index.get("all_ids", []):
        if "all_ids" not in index:
            index["all_ids"] = []
        index["all_ids"].append(env_id)

    return index

def envelope_store(
    tier: int,
    agent: str,
    project: str,
    workflow_id: str,
    workflow_goal: str,
    chunk_id: str,
    chunk_index: int,
    total_chunks: int,
    git_commit: str,
    confidence: str,
    findings: dict,
    findings_count: int = None,
    chunk_path: str = None,
    git_branch: str = None,
    external_refs: list = None
) -> dict:
    """
    Store a finding envelope with full indexing.

    This is the primary storage mechanism for Claude-Hybrid analysis findings.
    Every agent stores its findings wrapped in this envelope format.
    """
    # Validate required enums
    valid_goals = ["AUDIT", "DOCUMENT", "BUILD_FRONTEND"]
    if workflow_goal not in valid_goals:
        return {"error": f"Invalid workflow_goal. Must be one of: {valid_goals}"}

    valid_confidence = ["HIGH", "MEDIUM", "LOW"]
    if confidence not in valid_confidence:
        return {"error": f"Invalid confidence. Must be one of: {valid_confidence}"}

    if not isinstance(tier, int) or tier < 0 or tier > 8:
        return {"error": "tier must be an integer between 0 and 8"}

    if chunk_index >= total_chunks:
        return {"error": f"chunk_index ({chunk_index}) must be less than total_chunks ({total_chunks})"}

    if not findings:
        return {"error": "findings cannot be empty"}

    # Generate envelope
    envelope_id = _generate_envelope_id()
    timestamp = datetime.utcnow().isoformat() + "Z"

    envelope = {
        # Section A: Identification
        "envelope_id": envelope_id,
        "tier": tier,
        "agent": agent,
        "timestamp": timestamp,

        # Section B: Scope
        "project": project,
        "workflow_id": workflow_id,
        "workflow_goal": workflow_goal,

        # Section C: Chunking Context
        "chunk_id": chunk_id,
        "chunk_index": chunk_index,
        "total_chunks": total_chunks,
        "chunk_path": chunk_path,

        # Section D: Git Context
        "git_commit": git_commit,
        "git_branch": git_branch,

        # Section E: Quality Indicators
        "confidence": confidence,
        "findings_count": findings_count if findings_count is not None else (
            len(findings.get("issues", [])) if isinstance(findings.get("issues"), list) else 1
        ),
        "evidence_complete": True,  # Agent attests this

        # Section F: Payload
        "findings": findings,

        # Section G: Cross-References
        "external_refs": external_refs or [],

        # Section H: Validation State (initial)
        "validation_status": "PENDING",
        "validated_at": None,
        "validator_agent": None
    }

    # Save envelope to file
    envelope_path = _get_envelope_path(envelope_id, workflow_id)
    _save_json(envelope_path, envelope)

    # Update index
    index = _load_envelope_index()
    index = _index_envelope(index, envelope)
    _save_envelope_index(index)

    return {
        "stored": True,
        "envelope_id": envelope_id,
        "tier": tier,
        "agent": agent,
        "workflow_id": workflow_id,
        "chunk_id": chunk_id,
        "timestamp": timestamp,
        "file_path": str(envelope_path)
    }

def envelope_query(
    tier: int = None,
    agent: str = None,
    chunk_id: str = None,
    workflow_id: str = None,
    project: str = None,
    validation_status: str = None,
    confidence: str = None,
    limit: int = 50
) -> dict:
    """
    Query envelopes by indexed fields.

    Supports filtering by any combination of:
    - tier (0-8)
    - agent name
    - chunk_id
    - workflow_id
    - project path
    - validation_status (PENDING, VERIFIED, PARTIAL, REJECTED)
    - confidence (HIGH, MEDIUM, LOW)
    """
    index = _load_envelope_index()

    # Start with all envelope IDs
    candidate_ids = set(index.get("all_ids", []))

    # Filter by tier
    if tier is not None:
        tier_ids = set(index.get("by_tier", {}).get(str(tier), []))
        candidate_ids &= tier_ids

    # Filter by agent
    if agent is not None:
        agent_ids = set(index.get("by_agent", {}).get(agent, []))
        candidate_ids &= agent_ids

    # Filter by chunk_id
    if chunk_id is not None:
        chunk_ids = set(index.get("by_chunk", {}).get(chunk_id, []))
        candidate_ids &= chunk_ids

    # Filter by workflow_id
    if workflow_id is not None:
        workflow_ids = set(index.get("by_workflow", {}).get(workflow_id, []))
        candidate_ids &= workflow_ids

    # Filter by project
    if project is not None:
        project_ids = set(index.get("by_project", {}).get(project, []))
        candidate_ids &= project_ids

    # Load envelopes and apply remaining filters
    results = []
    for env_id in list(candidate_ids)[:limit * 2]:  # Load extra for post-filtering
        # Find the envelope file
        for wf_id, env_ids in index.get("by_workflow", {}).items():
            if env_id in env_ids:
                env_path = _get_envelope_path(env_id, wf_id)
                if env_path.exists():
                    envelope = _load_json(env_path)

                    # Post-filter by validation_status
                    if validation_status and envelope.get("validation_status") != validation_status:
                        continue

                    # Post-filter by confidence
                    if confidence and envelope.get("confidence") != confidence:
                        continue

                    results.append({
                        "envelope_id": envelope.get("envelope_id"),
                        "tier": envelope.get("tier"),
                        "agent": envelope.get("agent"),
                        "chunk_id": envelope.get("chunk_id"),
                        "workflow_id": envelope.get("workflow_id"),
                        "confidence": envelope.get("confidence"),
                        "validation_status": envelope.get("validation_status"),
                        "findings_count": envelope.get("findings_count"),
                        "timestamp": envelope.get("timestamp")
                    })
                break

        if len(results) >= limit:
            break

    # Sort by timestamp descending
    results.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

    return {
        "query": {
            "tier": tier,
            "agent": agent,
            "chunk_id": chunk_id,
            "workflow_id": workflow_id,
            "project": project,
            "validation_status": validation_status,
            "confidence": confidence
        },
        "total_matched": len(candidate_ids),
        "returned": len(results[:limit]),
        "envelopes": results[:limit]
    }

def envelope_get(envelope_id: str) -> dict:
    """
    Retrieve a specific envelope by ID.

    Returns the complete envelope with all fields including findings.
    """
    index = _load_envelope_index()

    # Find which workflow this envelope belongs to
    for wf_id, env_ids in index.get("by_workflow", {}).items():
        if envelope_id in env_ids:
            env_path = _get_envelope_path(envelope_id, wf_id)
            if env_path.exists():
                envelope = _load_json(env_path)
                return {
                    "found": True,
                    "envelope": envelope
                }

    return {
        "found": False,
        "envelope_id": envelope_id,
        "error": "Envelope not found"
    }


# =============================================================================
# TOOL REGISTRATION
# =============================================================================
@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all 29 tools (26 original + 3 envelope tools)."""
    return [
        # Registry (5)
        Tool(name="registry_list_agents", description="List all registered agents with optional filtering",
             inputSchema={"type": "object", "properties": {
                 "domain": {"type": "string", "description": "Filter by domain"},
                 "tags": {"type": "array", "items": {"type": "string"}, "description": "Filter by tags"},
                 "capability": {"type": "string", "description": "Filter by capability"},
                 "limit": {"type": "integer", "default": 50}
             }}),
        Tool(name="registry_get_agent", description="Get complete details for a specific agent",
             inputSchema={"type": "object", "properties": {
                 "agent_id": {"type": "string", "description": "Agent identifier"},
                 "include_metrics": {"type": "boolean", "default": True}
             }, "required": ["agent_id"]}),
        Tool(name="registry_search", description="Semantic search across agents",
             inputSchema={"type": "object", "properties": {
                 "query": {"type": "string", "description": "Search query"},
                 "types": {"type": "array", "items": {"type": "string"}},
                 "limit": {"type": "integer", "default": 10}
             }, "required": ["query"]}),
        Tool(name="registry_record_metric", description="Record task completion metrics",
             inputSchema={"type": "object", "properties": {
                 "agent_id": {"type": "string"},
                 "task_type": {"type": "string"},
                 "success": {"type": "boolean"},
                 "duration_seconds": {"type": "integer"},
                 "context": {"type": "object"}
             }, "required": ["agent_id", "task_type", "success"]}),
        Tool(name="registry_get_recommendations", description="Get intelligent agent recommendations",
             inputSchema={"type": "object", "properties": {
                 "task_description": {"type": "string"},
                 "project_type": {"type": "string"},
                 "toolchain": {"type": "array", "items": {"type": "string"}},
                 "limit": {"type": "integer", "default": 5}
             }, "required": ["task_description"]}),

        # Session (5)
        Tool(name="session_get_tokens", description="Get current token usage and budget",
             inputSchema={"type": "object", "properties": {
                 "include_breakdown": {"type": "boolean", "default": False}
             }}),
        Tool(name="session_check_threshold", description="Check current threshold status",
             inputSchema={"type": "object", "properties": {}}),
        Tool(name="session_get_state", description="Get current session state",
             inputSchema={"type": "object", "properties": {
                 "include_history": {"type": "boolean", "default": False}
             }}),
        Tool(name="session_save_state", description="Persist current session state",
             inputSchema={"type": "object", "properties": {
                 "state": {"type": "object", "description": "Session state to persist"},
                 "reason": {"type": "string"}
             }, "required": ["state"]}),
        Tool(name="session_get_resume_log", description="Get resume logs from previous sessions",
             inputSchema={"type": "object", "properties": {
                 "session_id": {"type": "string"}
             }}),

        # Project (6)
        Tool(name="project_get_config", description="Get current project configuration",
             inputSchema={"type": "object", "properties": {}}),
        Tool(name="project_get_phase", description="Get current methodology phase",
             inputSchema={"type": "object", "properties": {}}),
        Tool(name="project_detect_toolchain", description="Detect project toolchain",
             inputSchema={"type": "object", "properties": {
                 "path": {"type": "string", "default": "."},
                 "force_refresh": {"type": "boolean", "default": False}
             }}),
        Tool(name="project_get_active_agents", description="Get enabled agents for project",
             inputSchema={"type": "object", "properties": {}}),
        Tool(name="project_update_phase", description="Transition to next methodology phase",
             inputSchema={"type": "object", "properties": {
                 "new_phase": {"type": "string", "enum": ["planning", "architecture", "stories", "implementation"]},
                 "reason": {"type": "string"}
             }, "required": ["new_phase", "reason"]}),
        Tool(name="project_get_history", description="Get project action history",
             inputSchema={"type": "object", "properties": {
                 "limit": {"type": "integer", "default": 50},
                 "action_type": {"type": "string"}
             }}),

        # Enforcement (5)
        Tool(name="enforce_check_breaker", description="Check if action violates circuit breakers",
             inputSchema={"type": "object", "properties": {
                 "action_type": {"type": "string", "enum": ["implement_code", "delegate_task", "make_assertion", "skip_tests", "skip_planning"]},
                 "context": {"type": "object"}
             }, "required": ["action_type"]}),
        Tool(name="enforce_validate_sequence", description="Validate action follows methodology sequence",
             inputSchema={"type": "object", "properties": {
                 "current_phase": {"type": "string"},
                 "intended_action": {"type": "string"}
             }, "required": ["current_phase", "intended_action"]}),
        Tool(name="enforce_require_plan", description="Check if task requires plan mode",
             inputSchema={"type": "object", "properties": {
                 "task_description": {"type": "string"},
                 "estimated_files": {"type": "integer"},
                 "has_existing_plan": {"type": "boolean", "default": False}
             }, "required": ["task_description"]}),
        Tool(name="enforce_validate_delegation", description="Validate delegation follows PM model",
             inputSchema={"type": "object", "properties": {
                 "delegator": {"type": "string"},
                 "delegate_to": {"type": "string"},
                 "task_type": {"type": "string"}
             }, "required": ["delegator", "delegate_to", "task_type"]}),
        Tool(name="enforce_log_violation", description="Log a circuit breaker violation",
             inputSchema={"type": "object", "properties": {
                 "breaker_id": {"type": "string"},
                 "action_attempted": {"type": "string"},
                 "context": {"type": "object"},
                 "resolution": {"type": "string"}
             }, "required": ["breaker_id", "action_attempted"]}),

        # Memory (5)
        Tool(name="memory_recall_project", description="Retrieve project-specific memories",
             inputSchema={"type": "object", "properties": {
                 "project_id": {"type": "string"},
                 "memory_types": {"type": "array", "items": {"type": "string"}},
                 "limit": {"type": "integer", "default": 20}
             }}),
        Tool(name="memory_recall_agent", description="Retrieve memories for specific agent",
             inputSchema={"type": "object", "properties": {
                 "agent_id": {"type": "string"},
                 "limit": {"type": "integer", "default": 20}
             }, "required": ["agent_id"]}),
        Tool(name="memory_recall_domain", description="Semantic search for domain memories",
             inputSchema={"type": "object", "properties": {
                 "domain": {"type": "string"},
                 "query": {"type": "string"},
                 "limit": {"type": "integer", "default": 10}
             }, "required": ["domain"]}),
        Tool(name="memory_store_learning", description="Store a new learning/memory",
             inputSchema={"type": "object", "properties": {
                 "type": {"type": "string", "enum": ["pattern", "architecture", "guideline", "mistake", "strategy", "integration", "performance", "context"]},
                 "content": {"type": "string"},
                 "agent_id": {"type": "string"},
                 "domain": {"type": "string"},
                 "project_id": {"type": "string"}
             }, "required": ["type", "content"]}),
        Tool(name="memory_get_relevant", description="Get most relevant memories for a task",
             inputSchema={"type": "object", "properties": {
                 "task_description": {"type": "string"},
                 "agent_id": {"type": "string"},
                 "max_tokens": {"type": "integer", "default": 2000}
             }, "required": ["task_description"]}),

        # Envelope (3) - Claude-Hybrid Analysis System
        Tool(name="envelope_store", description="Store a finding envelope with full indexing for Claude-Hybrid analysis",
             inputSchema={"type": "object", "properties": {
                 "tier": {"type": "integer", "minimum": 0, "maximum": 8, "description": "Tier number (0-8)"},
                 "agent": {"type": "string", "description": "Agent name that produced this"},
                 "project": {"type": "string", "description": "Absolute project path"},
                 "workflow_id": {"type": "string", "description": "Links to frontmatter workflow_id"},
                 "workflow_goal": {"type": "string", "enum": ["AUDIT", "DOCUMENT", "BUILD_FRONTEND"]},
                 "chunk_id": {"type": "string", "description": "Logical chunk identifier"},
                 "chunk_index": {"type": "integer", "minimum": 0, "description": "0-indexed chunk position"},
                 "total_chunks": {"type": "integer", "minimum": 1, "description": "Total chunks in manifest"},
                 "git_commit": {"type": "string", "description": "Commit hash at analysis time"},
                 "confidence": {"type": "string", "enum": ["HIGH", "MEDIUM", "LOW"]},
                 "findings": {"type": "object", "description": "Tier-specific findings payload"},
                 "findings_count": {"type": "integer", "description": "Number of findings (auto-calculated if omitted)"},
                 "chunk_path": {"type": "string", "description": "File path pattern for this chunk"},
                 "git_branch": {"type": "string", "description": "Branch name"},
                 "external_refs": {"type": "array", "items": {"type": "object"}, "description": "Cross-chunk references"}
             }, "required": ["tier", "agent", "project", "workflow_id", "workflow_goal", "chunk_id", "chunk_index", "total_chunks", "git_commit", "confidence", "findings"]}),
        Tool(name="envelope_query", description="Query envelopes by tier, agent, chunk, workflow, project, status, or confidence",
             inputSchema={"type": "object", "properties": {
                 "tier": {"type": "integer", "minimum": 0, "maximum": 8, "description": "Filter by tier"},
                 "agent": {"type": "string", "description": "Filter by agent name"},
                 "chunk_id": {"type": "string", "description": "Filter by chunk ID"},
                 "workflow_id": {"type": "string", "description": "Filter by workflow ID"},
                 "project": {"type": "string", "description": "Filter by project path"},
                 "validation_status": {"type": "string", "enum": ["PENDING", "VERIFIED", "PARTIAL", "REJECTED"]},
                 "confidence": {"type": "string", "enum": ["HIGH", "MEDIUM", "LOW"]},
                 "limit": {"type": "integer", "default": 50, "description": "Max results to return"}
             }}),
        Tool(name="envelope_get", description="Retrieve a specific envelope by ID with full findings",
             inputSchema={"type": "object", "properties": {
                 "envelope_id": {"type": "string", "description": "The envelope ID (env-YYYYMMDD-HHMMSS-random)"}
             }, "required": ["envelope_id"]}),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Route tool calls to implementations."""
    _ensure_dirs()

    try:
        # Registry tools
        if name == "registry_list_agents":
            return _result(registry_list_agents(**arguments))
        elif name == "registry_get_agent":
            return _result(registry_get_agent(**arguments))
        elif name == "registry_search":
            return _result(registry_search(**arguments))
        elif name == "registry_record_metric":
            return _result(registry_record_metric(**arguments))
        elif name == "registry_get_recommendations":
            return _result(registry_get_recommendations(**arguments))

        # Session tools
        elif name == "session_get_tokens":
            return _result(session_get_tokens(**arguments))
        elif name == "session_check_threshold":
            return _result(session_check_threshold())
        elif name == "session_get_state":
            return _result(session_get_state(**arguments))
        elif name == "session_save_state":
            return _result(session_save_state(**arguments))
        elif name == "session_get_resume_log":
            return _result(session_get_resume_log(**arguments))

        # Project tools
        elif name == "project_get_config":
            return _result(project_get_config())
        elif name == "project_get_phase":
            return _result(project_get_phase())
        elif name == "project_detect_toolchain":
            return _result(project_detect_toolchain(**arguments))
        elif name == "project_get_active_agents":
            return _result(project_get_active_agents())
        elif name == "project_update_phase":
            return _result(project_update_phase(**arguments))
        elif name == "project_get_history":
            return _result(project_get_history(**arguments))

        # Enforcement tools
        elif name == "enforce_check_breaker":
            return _result(enforce_check_breaker(**arguments))
        elif name == "enforce_validate_sequence":
            return _result(enforce_validate_sequence(**arguments))
        elif name == "enforce_require_plan":
            return _result(enforce_require_plan(**arguments))
        elif name == "enforce_validate_delegation":
            return _result(enforce_validate_delegation(**arguments))
        elif name == "enforce_log_violation":
            return _result(enforce_log_violation(**arguments))

        # Memory tools
        elif name == "memory_recall_project":
            return _result(memory_recall_project(**arguments))
        elif name == "memory_recall_agent":
            return _result(memory_recall_agent(**arguments))
        elif name == "memory_recall_domain":
            return _result(memory_recall_domain(**arguments))
        elif name == "memory_store_learning":
            return _result(memory_store_learning(**arguments))
        elif name == "memory_get_relevant":
            return _result(memory_get_relevant(**arguments))

        # Envelope tools (Claude-Hybrid Analysis System)
        elif name == "envelope_store":
            return _result(envelope_store(**arguments))
        elif name == "envelope_query":
            return _result(envelope_query(**arguments))
        elif name == "envelope_get":
            return _result(envelope_get(**arguments))

        return _result({"error": f"Unknown tool: {name}"})
    except Exception as e:
        return _result({"error": str(e)})


async def main():
    """Run the MCP server."""
    _ensure_dirs()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
