# Agent Unification Research Summary

**Date:** 2025-12-11
**Session:** 2
**Purpose:** Research how to unify 97 agents (56 BMAD + 41 claude-mpm) into ONE system
**Status:** Research complete, decision pending

---

## Executive Summary

We need to merge two agent systems with fundamentally different architectures:

| Aspect | BMAD (56 agents) | Claude-MPM (41 agents) |
|--------|------------------|------------------------|
| **Structure** | XML-rich personas, response gates | YAML frontmatter, protocol inheritance |
| **Size** | ~28K tokens per agent | ~12.5K tokens per agent |
| **Philosophy** | Persona-driven, identity-first | Protocol-driven, resilience-first |
| **Routing** | Module:agent-name, user menu | Keyword matching, PM delegation |
| **Missing** | PM routing metadata | Domain specialization depth |

**Critical Discovery:** Claude-MPM has a DELIBERATE CONTRACT (schema v1.3.0) that agents MUST follow for PM routing. BMAD agents don't have this metadata.

---

## The Agent Inventory

### BMAD Personal Architecture (56 agents, 11 modules)

| Module | Agents | Specialization |
|--------|--------|----------------|
| core | 3 | bmad-master, bmad-master-v2, enginex |
| bmm | 8 | analyst, pm, dev, sm, tea, tech-writer, ux-designer, enginex |
| cis | 5 | brainstorming-coach, design-thinking-coach, creative-problem-solver, innovation-strategist, storyteller |
| bmb | 1 | bmad-builder |
| bmgd | 4 | game-designer, game-dev, game-architect, game-scrum-master |
| android | 4 | android-framework-master, android-security-master, apk-analyst, android-educator |
| hooking | 4 | hook-architect, dobby-hook-master, jni-bridge-master, ndk-native-master |
| security | 6 | bypass-validator, detector-analyst, binary-analyst, kernel-syscall-master, native-debugger-master, precision-guardian |
| claude-builtin | 10 | multi-agent-analyzer, multi-agent-reviewer, multi-agent-debugger, escalation-handler, + 6 analyzers |
| advanced | 9 | architecture-surgeon, code-archaeologist, dependency-detective, pattern-master, + 5 more |
| utils | 2 | documentation-writer, test-guardian |

**Source:** `~/.claude/plugins/marketplaces/local/plugins/{module}/agents/`

### Claude-MPM (41 agents)

| Category | Count | Examples |
|----------|-------|----------|
| Engineering | 15 | engineer, python-engineer, typescript-engineer, nextjs-engineer, etc. |
| Operations | 7 | ops, vercel-ops, gcp-ops, local-ops, etc. |
| QA/Testing | 3 | qa, api-qa, web-qa |
| Research | 3 | research, code-analyzer, security |
| Documentation | 4 | documentation, ticketing, version-control, web-ui |
| Product/Content | 3 | product-owner, content-agent, prompt-engineer |
| System | 5 | agent-manager, mpm-agent-manager, mpm-skills-manager, project-organizer, memory-manager |
| Data | 1 | data-engineer |

**Source:** `/home/president/bmad-systems/claude-mpm/.claude/agents/`

---

## Claude-MPM Agent Contract (CRITICAL)

### Required Fields for PM Routing

```yaml
# MINIMUM CONTRACT - PM cannot route without these
name: unique-agent-id           # PM uses to identify and call
description: Purpose text       # PM shows to user
version: 1.0.0                  # Semantic versioning
model: opus|sonnet|haiku        # Resource tier
```

### Optional But Critical for Intelligent Routing

```yaml
agent_type: engineer|qa|research|security|ops|documentation|...
category: engineering|research|quality|operations|specialized
tags: [searchable, metadata, keywords]
capabilities:
  tools: [Read, Write, Edit, Bash, ...]
  resource_tier: basic|standard|intensive
```

### PM Routing Mechanism

1. **Keyword Detection** → User says "investigate" → Research agent
2. **Circuit Breakers** → 7 rules that FORCE delegation
3. **Capability Matching** → Uses metadata.tags and category
4. **Recommender Algorithm:**
   ```
   score = (language_match × 0.5) + (framework_match × 0.3) + (deployment_match × 0.2)
   ```

### Schema Locations

- `frontmatter_schema.json` - Lightweight routing schema
- `agent_schema.json` v1.3.0 - Full validation schema
- `agent_capabilities.yaml` - Capability registry
- `PM_INSTRUCTIONS.md` - Routing rules and Circuit Breakers

---

## Agent Format Comparison

### BMAD Agent Structure (Current)

```markdown
---
name: dev
description: "Long narrative description..."
model: inherit
permissionMode: bypassPermissions
skills: sequential-thinking, mcp-use
color: green
---

<session_config>...</session_config>        # 12 lines
<response_gate>...</response_gate>          # 72 lines (BLOAT for Task tool)
<core_identity>...</core_identity>          # 100+ lines
<battle_scars>...</battle_scars>            # 23 lines (BLOAT)
<communication_style>...</communication_style>
<principles>...</principles>
<behaviors>...</behaviors>                  # Essential
<red_lines>...</red_lines>                  # 87 lines (verbose)
<code_examples>...</code_examples>          # 454 lines (EXTERNALIZE)
<menu>...</menu>                            # 8 lines (BLOAT for Task tool)
```

**Total:** ~1,555 lines (~28K tokens)

### Claude-MPM Agent Structure (Current)

```markdown
---
name: engineer
description: "Brief with <example> tags..."
model: sonnet
type: engineer
version: "3.9.1"
---

# Agent Name

Follow BASE_ENGINEER.md for protocols.

## Core Principles
...

## Protocols
...

## Tool Awareness
- If [tool] unavailable → [fallback]
```

**Total:** ~700 lines (~12.5K tokens)

**Problem:** Description in frontmatter AND body = duplicate (~500 tokens wasted)

---

## Proposed Unified Format

```yaml
---
# ROUTING-CRITICAL (PM needs these)
name: bmm-dev                              # Unique ID
description: "Story-driven implementation" # Brief purpose (NO duplicates)
version: "1.0.0"                          # Semantic version
model: sonnet                             # opus|sonnet|haiku
agent_type: engineer                      # Category for routing
tags: [implementation, story-driven, tdd] # Capability keywords

# CLAUDE-HYBRID ADDITIONS (for MCP routing)
module: bmm                               # Preserve hierarchy
domain: [implementation, coding]          # Domain classification
keywords: [story, acceptance-criteria]    # Trigger words

# OPTIONAL
capabilities:
  tools: [Read, Write, Edit, Bash, Grep, Glob]
  resource_tier: standard
---

# Agent Name

## IDENTITY (5 lines max)
Elite [role] specialist. [1 sentence expertise]. [1 sentence philosophy].

## CAPABILITIES
- Capability 1
- Capability 2

## PRINCIPLES (numbered, 1-line each)
1. ZERO tolerance for [X]
2. MANDATORY [Y] before [Z]

## BEHAVIORS (task-specific, with triggers)

### Behavior 1: [Name]
**Trigger:** When [condition]
**Action:** [What agent does]

## RED LINES (enforcement rules only)
- REFUSE: [condition] → [response]

## TOOL AWARENESS
- If [tool] unavailable → [fallback]
```

**Target:** 400-600 lines (~8,000-12,000 tokens)

---

## Bloat Analysis: What to Remove from BMAD Agents

| Section | Lines | For Task Tool? | Action |
|---------|-------|----------------|--------|
| **Menus** | 8-11 | NO | REMOVE 100% |
| **Response Gates** | 29-71 | Overkill | REDUCE to 5 lines |
| **Battle Scars** | 7-23 | NO | REMOVE 100% |
| **Persona Narrative** | 20-30 | NO | REMOVE 100% |
| **Code Examples** | 454 | Reference only | EXTERNALIZE |
| **Red Line Justifications** | 50+ | Verbose | KEEP rules only |

**Potential savings:** ~71% reduction per agent (~3,339 tokens)

---

## Recommended Architecture

### MCP-Based Capability Discovery (Aligns with D6)

```
Claude-Hybrid MCP:
├── tool: get_agent_for_task(task_description) → advisory
├── tool: list_agents_by_domain(domain) → agent list
└── tool: get_agent_capabilities(agent_id) → full metadata
```

**Flow:**
1. PM asks MCP: "What agent for: implement location hooks?"
2. MCP returns: `{suggested: "android:android-framework-master", confidence: 0.92}`
3. PM decides based on advisory + context
4. PM uses Task tool with selected agent

**Aligns with:**
- D1 (MCP is data plane) - capability lookup is data
- D2 (Control in-process) - PM makes routing decision
- D6 (Advisory pattern) - MCP suggests, Claude decides
- D7 (Graceful degradation) - PM fallback to keyword matching if MCP down

### File Structure (Hierarchical Namespace)

```
~/.claude/plugins/marketplaces/local/plugins/
├── bmm/agents/
│   ├── analyst.md
│   ├── dev.md
│   └── ...
├── android/agents/
│   ├── android-framework-master.md
│   └── ...
├── claude-mpm/agents/              # claude-mpm agents as a module
│   ├── engineer.md
│   ├── research.md
│   └── ...
└── unified/
    └── agent-registry.yaml         # Master capability index
```

**Invocation:** `subagent_type="bmm:dev"` or `subagent_type="claude-mpm:engineer"`

---

## Pending Decision (Session 3)

**How to handle 56 BMAD agents missing PM routing metadata?**

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A) Auto-generate** | Script reads agents, generates metadata | Fast, consistent | May miss nuance |
| **B) Manual curation** | Human reviews each agent | Precise | Time-consuming (56 agents) |
| **C) Hybrid** | Auto-generate + manual review for critical | Balanced | Still requires review effort |

**Critical agents requiring careful metadata:**
- android/* (4 agents) - Security research domain
- hooking/* (4 agents) - LSPosed/Dobby specialization
- security/* (6 agents) - Multi-layer validation
- advanced/* (9 agents) - Code archaeology, refactoring

---

## Key Files Referenced

| File | Purpose |
|------|---------|
| `/home/president/bmad-systems/personal bmad/BMAD-PERSONAL-ARCHITECTURE.md` | Personal BMAD full architecture |
| `/home/president/bmad-systems/claude-mpm/src/claude_mpm/schemas/agent_schema.json` | Agent contract v1.3.0 |
| `/home/president/bmad-systems/claude-mpm/src/claude_mpm/schemas/frontmatter_schema.json` | Routing schema |
| `/home/president/bmad-systems/claude-mpm/.claude-mpm/PM_INSTRUCTIONS.md` | PM routing rules |
| `/home/president/bmad-systems/claude-mpm/src/claude_mpm/config/agent_capabilities.yaml` | Capability registry |
| `/home/president/bmad-systems/claude-mpm/src/claude_mpm/services/agents/recommender.py` | Scoring algorithm |

---

## Session 3-4 Resolution

### Decision Made: COMPLETE REBUILD (Option D)

User clarified that Options A/B/C (metadata patching) were insufficient. The actual requirement is:
- **REBUILD** all 87 agents from scratch with unified template
- **NOT** just add metadata to existing agents

### Session 3 Key Clarifications

1. **Revised count:** 87 agents (exclude 10 claude-builtin)
2. **BMB deprecated:** bmad-builder is workflow, not Task agent
3. **Complete rebuild required:** New unified template, not patching
4. **Description collision:** Rename body section to "Expertise"

### Session 4: Unified Template v3.0 COMPLETE

**Template finalized with:**
- Frontmatter (L1): name, description (no examples), version, model, agent_type, tags
- Body (L2): Expertise, Identity, When to Use, Core Capabilities, [Domain Sections], Boundaries, Tool Awareness
- Token budget: 2,000-3,000 tokens per agent
- 10 agent_types defined
- Edge cases addressed

**See:** `UNIFIED-TEMPLATE-v3.0.md` for complete specification

### Next Steps (Session 5+)

1. **User approval** of template specification
2. **Plan unified-agent-builder workflow** (replaces bmad-builder)
3. **Tier 87 agents** by priority (Tier 1 critical, Tier 2 high-use, Tier 3 standard)
4. **Begin rebuild** with Tier 1 proof-of-concept

---

*Research conducted by Claude (Opus 4.5) | Sessions 2-4 | 2025-12-11*
