# Complete Investigation Findings - Session 6

**Date:** 2025-12-12
**Purpose:** Comprehensive investigation before Orchestrator-master design decisions
**Status:** Investigation Complete - Requires D1-D14 Review Before Proceeding

---

## Executive Summary

This investigation was conducted to achieve total clarity on:
1. How `--append-system-prompt` works in Claude Code
2. How claude-mpm's PM orchestrator is implemented
3. How bmad-master's intelligent routing works
4. The wrapper architecture and its implications for Claude-Hybrid

**Key Finding:** Claude-Hybrid's architecture is fundamentally different from claude-mpm's wrapper approach. Direct copying of claude-mpm patterns is NOT appropriate. A D1-D14 review is needed before proceeding.

---

## Part 1: --append-system-prompt Mechanism

### What It Does

| Aspect | Detail |
|--------|--------|
| **Mechanism** | APPENDS content to the END of Claude's base system prompt |
| **Effect** | Adds rules/behavior ON TOP of base Claude - does NOT replace |
| **Timing** | Applied at CLI launch, before Claude processes first input |
| **Scope** | Persistent across entire session |

### Message Flow Order

```
1. System Prompt (Claude's base behavior)
2. --append-system-prompt content (appended to system prompt)
3. CLAUDE.md content (first user message)
4. User messages/queries
```

### Key Distinction from CLAUDE.md

| Feature | --append-system-prompt | CLAUDE.md |
|---------|------------------------|-----------|
| **Placement** | Appended to system prompt | First user message |
| **Scope** | Global, persistent | Conversation-specific |
| **Use Case** | Core agent personality/rules | Project-specific context |

**Source:** [Claude Code CLI Reference](https://code.claude.com/docs/en/cli-reference), [GitHub Issue #6973](https://github.com/anthropics/claude-code/issues/6973)

---

## Part 2: Claude-MPM Architecture

### Core Architecture: WRAPPER Pattern

Claude-mpm is a **WRAPPER** around Claude Code, NOT a plugin.

```
┌─────────────────────────────────────────────┐
│  User runs: claude-mpm                      │
└─────────────────┬───────────────────────────┘
                  │
                  v
┌─────────────────────────────────────────────┐
│  MPM Wrapper Process                        │
│  • Loads agent configurations               │
│  • Assembles ~450KB system prompt           │
│  • Caches instructions to file              │
│  • Builds CLI command with flags            │
└─────────────────┬───────────────────────────┘
                  │
                  v
┌─────────────────────────────────────────────┐
│  subprocess.run(['claude', ...])            │
│  OR os.execvpe(cmd, args, env)              │
│                                             │
│  Claude Code starts WITH PM behavior        │
└─────────────────────────────────────────────┘
```

### Why Wrapper, Not Plugin

From `docs/developer/why-not-a-plugin.md`:

> "Claude MPM cannot be distributed as a Claude Code plugin due to a fundamental architectural incompatibility. MPM must inject PM_INSTRUCTIONS **before** Claude Code starts, but plugins execute **after** Claude Code initializes."

**Plugin Execution Timing:**
```
1. Parse CLI arguments (happens first)
2. Load system configuration (including instructions)
3. Initialize LLM session (with baked-in instructions)
4. Load plugins (too late for #2 and #3)  ← PLUGINS HERE
5. Start interactive session
```

MPM needs to inject at step #2, but plugins load at step #4.

### System Prompt Assembly

The assembled system prompt (~450KB) contains:

```
1. FRAMEWORK_INSTRUCTIONS (from INSTRUCTIONS.md)
2. CUSTOM_INSTRUCTIONS (project-level .claude/INSTRUCTIONS.md)
3. WORKFLOW_INSTRUCTIONS (from WORKFLOW.md)
4. MEMORY_INSTRUCTIONS (from MEMORY.md)
5. ACTUAL_PM_MEMORIES (from .claude-mpm/memories/PM.md)
6. AGENT_MEMORIES (per agent)
7. AGENT_CAPABILITIES_SECTION (dynamically generated)
8. CONTEXT_SECTION (temporal/user context)
9. BASE_PM_INSTRUCTIONS (from BASE_PM.md)
10. OUTPUT_STYLE_CONTENT (conditional, for older Claude versions)
```

### Instruction Caching

**Problem:** Linux ARG_MAX limit ~128KB, assembled instructions ~450KB

**Solution:** Cache to file, pass via `--system-prompt-file`

```python
# If cache valid:
cmd.extend(["--system-prompt-file", str(cache_file)])
# Fallback:
cmd.extend(["--append-system-prompt", system_prompt])
```

### Final Command Construction

```bash
claude \
  --dangerously-skip-permissions \
  [custom-args] \
  --agents '<json>' \
  --system-prompt-file .claude-mpm/PM_INSTRUCTIONS.md
```

---

## Part 3: --agents Flag Mechanism

### JSON Schema

```json
{
  "agent-id": {
    "description": "string (REQUIRED) - when to use this agent",
    "prompt": "string (REQUIRED) - agent's system instructions",
    "tools": ["string"] (optional),
    "model": "string" (optional),
    "permissionMode": "string" (optional),
    "skills": ["string"] (optional)
  }
}
```

### Size Limits

| Limit | Value | Reason |
|-------|-------|--------|
| **Conservative** | 50,000 chars | Safety margin |
| **OS Limit** | ~128KB Linux, ~32KB Windows | ARG_MAX |
| **Practical** | 10-15 agents with full prompts | Token budget |
| **Maximum** | 30-40 agents with concise prompts | With optimization |

### Routing Mechanism

Claude uses multi-factor automatic delegation:
1. **Description Matching** - Task vs agent description
2. **Task Context Analysis** - Project, tools, complexity
3. **Explicit Invocation** - User requests specific agent
4. **Proactive Triggering** - Keywords like "PROACTIVELY"

**Estimated Compliance:** 70-90% when descriptions are clear

### Interaction with --append-system-prompt

```bash
# Execution order in command:
claude --agents '<json>' --append-system-prompt '<text>'
```

- **--agents** defines subagent configurations
- **--append-system-prompt** adds main Claude (PM) instructions
- Both operate independently, no merging

### Comparison with D13 (agent-index.yaml)

| Aspect | --agents Flag | D13 agent-index.yaml |
|--------|---------------|---------------------|
| **Mechanism** | CLI JSON argument | File-based aggregation |
| **Source** | Passed at launch | Extracted from .md files |
| **Token Overhead** | Variable (JSON size) | ~13K (87 agents × 150 tokens) |
| **Dependency** | Built into Claude Code | In-process Python script |
| **Scaling** | Hard ceiling ~40 agents | Scales to 100+ agents |
| **Failure Mode** | Agents unavailable if malformed | Works 100% without MCP |

**Key Insight:** D13's approach is more scalable for 87 agents than --agents flag.

---

## Part 4: Routing Comparison (bmad-master vs claude-mpm PM)

### bmad-master Routing

**Agent Discovery:**
- Reads CSV manifest at runtime (`/bmad/_cfg/agent-manifest.csv`)
- Extracts: name, displayName, role, identity, communicationStyle, principles
- Dynamic, no hardcoding

**Routing Algorithm:**
- Party mode orchestration
- Selects 2-3 most relevant agents per turn
- Based on conversation context + agent expertise
- Personality-aware selection

**Strengths:**
- Flexible agent discovery
- Contextual routing
- Runtime adaptability

**Weaknesses:**
- No confidence scoring
- No explicit workflow phases
- No verification gates
- No fallback chains

### claude-mpm PM Routing

**Agent Discovery:**
- Hardcoded in PM_INSTRUCTIONS.md
- No runtime discovery
- Assumes all agents available

**Routing Algorithm:**
- Explicit delegation matrix
- Task-type keyword matching ("API" → api-qa, "UI" → web-qa)
- 5-phase mandatory workflow:
  1. Research (always first)
  2. Code Analyzer Review
  3. Implementation
  4. QA (mandatory)
  5. Documentation

**Strengths:**
- Explicit workflow phases
- Verification gates (mandatory QA)
- File tracking discipline
- Circuit breaker enforcement

**Weaknesses:**
- No runtime agent discovery
- No contextual routing
- No confidence scoring
- No graceful degradation

### What Both Lack

1. **Confidence Scoring** - No quantified capability assessment
2. **Health Detection** - No availability checking
3. **Fallback Chains** - No alternative routing if agent unavailable
4. **Graceful Degradation** - Fails if expected agent missing

---

## Part 5: Implications for Claude-Hybrid

### Fundamental Architecture Difference

| Aspect | Claude-mpm | Claude-Hybrid (D1-D14) |
|--------|-----------|------------------------|
| **Process Model** | Subprocess wrapper | In-process SDK |
| **State SSOT** | Env vars + cached files | Frontmatter in files (D3) |
| **Hook Execution** | Claude Code plugin level | In-process Python (D2) |
| **Agent Deployment** | ~/.claude/agents/ (files) | Function registry + Task tool |
| **Command Interface** | CLI arguments | Direct API calls |
| **Process Boundary** | Python → subprocess | Python → optionally os.execvpe |

### What Claude-Hybrid CANNOT Do

1. **Use --append-system-prompt** - That's for CLI wrapper, not in-process
2. **Use --agents JSON for 87 agents** - Exceeds size limits
3. **Copy claude-mpm wrapper architecture** - We're already IN Claude Code

### What Claude-Hybrid SHOULD Do

1. **Agent Discovery:** D13's L1 frontmatter aggregation (scalable)
2. **Routing:** Task tool dispatch with agent-index.yaml lookup
3. **State:** Frontmatter SSOT (survives os.execvpe per D3)
4. **Hooks:** In-process Python (D2 control layer)
5. **Verification:** Adapt PM's mandatory QA pattern
6. **Intelligence:** Adapt bmad-master's detection protocols

---

## Part 6: Open Questions

### Critical Questions Before Proceeding

1. **How does Claude-Hybrid deliver orchestrator behavior?**
   - Not via --append-system-prompt (CLI wrapper mechanism)
   - Via CLAUDE.md? Via hooks? Via something else?

2. **How does Task tool agent routing actually work?**
   - Does it use --agents internally?
   - Or different mechanism?

3. **What is the ACTUAL delivery mechanism for Orchestrator-master?**

4. **Do D1-D14 decisions account for this architecture difference?**
   - D2 says "Control Layer In-Process" - but how?
   - D13 says "L1 Frontmatter Aggregation" - but how is it delivered?

### Recommendation

**BEFORE designing Orchestrator-master:**
1. Review D1-D14 decisions with this new understanding
2. Clarify the delivery mechanism for orchestrator instructions
3. Ensure decisions align with actual Claude Code capabilities

---

## Sources

- [Claude Code CLI Reference](https://code.claude.com/docs/en/cli-reference)
- [GitHub Issue #6973 - CLAUDE.md vs --append-system-prompt](https://github.com/anthropics/claude-code/issues/6973)
- [Claude-MPM why-not-a-plugin.md](https://github.com/bobmatnyc/claude-mpm/blob/main/docs/developer/why-not-a-plugin.md)
- claude-mpm source: `src/claude_mpm/core/interactive_session.py`
- claude-mpm source: `src/claude_mpm/services/native_agent_converter.py`
- claude-mpm source: `src/claude_mpm/agents/PM_INSTRUCTIONS.md`
- bmad-master: `~/.claude/plugins/cache/local/core/1.0.0/agents/bmad-master.md`
- bmad party-mode: `~/.bmad/core/workflows/party-mode/workflow.md`

---

*Investigation conducted Session 6 | 2025-12-12*
