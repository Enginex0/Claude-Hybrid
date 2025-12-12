# Unified Agent Template v3.0 Specification

**Created:** 2025-12-11 (Session 4)
**Status:** Ready for Approval
**Author:** Claude (Opus 4.5) + President

---

## Overview

| Aspect | Value |
|--------|-------|
| **Target** | 87 agents (46 BMAD + 41 claude-mpm) |
| **Token Budget** | L1: ~100-150 tokens, L2: ~2,000-2,500 tokens |
| **Line Target** | 600-900 lines per agent |
| **Pattern** | Claude-mpm rich style with BMAD structural improvements |

---

## FRONTMATTER SCHEMA (L1 - Always Loaded)

```yaml
---
# ══════════════════════════════════════════════════════════════
# REQUIRED FIELDS (PM routing depends on these)
# ══════════════════════════════════════════════════════════════
name: module:agent-name                    # Unique namespaced identifier
description: >-                            # 150-300 chars, NO <example> tags
  Use this agent when [primary trigger].
  PROACTIVELY use for [specific scenarios].
  Specializes in [3-5 key capabilities].
version: "1.0.0"                           # Semantic versioning
model: sonnet                              # opus | sonnet | haiku
agent_type: engineer                       # See Agent Types below
tags:                                      # Searchable keywords (5-10)
  - keyword1
  - keyword2

# ══════════════════════════════════════════════════════════════
# RECOMMENDED FIELDS (Improves routing precision)
# ══════════════════════════════════════════════════════════════
module: bmm                                # Organizational namespace
triggers:                                  # Explicit activation phrases
  - "implement feature"
  - "write production code"

# ══════════════════════════════════════════════════════════════
# OPTIONAL FIELDS (Domain-specific)
# ══════════════════════════════════════════════════════════════
capabilities:
  tools: [Read, Write, Edit, Bash, Grep, Glob]
  tier: standard                           # basic | standard | intensive

languages: [python, kotlin]                # For language-specific agents
frameworks: [django, fastapi]              # For framework-specific agents
orchestrates: [dev, qa, security]          # For orchestrator agents
authorization: educational-research        # For security research agents
deprecated: false                          # Set true with deprecated_notice
deprecated_notice: "Use unified:enginex instead"
---
```

### Agent Types (agent_type values)

| Type | Description | Examples |
|------|-------------|----------|
| `engineer` | Implementation specialists | dev, python-engineer, rust-engineer |
| `architect` | Design and structure | code-architect, game-architect |
| `qa` | Testing and quality | tea, web-qa, api-qa |
| `security` | Security analysis | security, bypass-validator |
| `research` | Investigation and analysis | research, code-archaeologist |
| `ops` | Operations and deployment | ops, vercel-ops, gcp-ops |
| `creative` | Creative and ideation | storyteller, brainstorming-coach |
| `workflow` | Process management | sm, pm, analyst |
| `orchestrator` | Multi-agent coordination | bmad-master, multi-agent-analyzer |
| `specialist` | Narrow domain expert | dobby-hook-master, jni-bridge-master |

---

## BODY STRUCTURE (L2 - Loaded on Activation)

```markdown
# Agent Display Name

## Expertise

[2-5 sentences describing deep domain knowledge. This is NOT a repeat of
the frontmatter description - this explains WHY this agent is exceptional
at what it does. Include years of experience, specific achievements, and
what makes this agent's approach unique.]

## Identity

[1-3 sentences defining the core role. No persona fluff, no "You are an
elite veteran" narratives. Just clear role definition.]

## When to Use

[Explicit trigger conditions with inline examples]

<example>
Context: User needs to implement a new feature with acceptance criteria
User: "Implement the user authentication story from the sprint backlog"
Agent: Loads story context, validates ACs, implements with test coverage
</example>

<example>
Context: When NOT to use this agent (negative example)
User: "Help me brainstorm feature ideas"
Agent: This is creative work - delegate to brainstorming-coach instead
</example>

## Core Capabilities

- **[Capability 1]:** [Brief description of what agent can do]
- **[Capability 2]:** [Brief description]
- [Continue for 8-15 capabilities]

## [Domain-Specific Sections]

[These sections vary by agent type. Choose appropriate sections:]

### For Engineers: Workflows / Patterns / Anti-Patterns
### For Security: Security Protocols / Detection Methods
### For Creative: Creative Methods / Techniques
### For Orchestrators: Delegation Patterns / Routing Rules
### For Specialists: Technical Reference / Implementation Details

[Include inline code examples where relevant]

## Boundaries

[Clear refusal conditions - condensed from BMAD's red_lines]

- **REFUSE:** [Condition] → [Why and what to do instead]
- **BLOCK:** [Condition requiring escalation] → [Escalation path]

## Tool Awareness

[Graceful degradation when tools unavailable]

- If `[Tool]` unavailable → [Fallback strategy]
- If `[MCP Server]` unavailable → [Alternative approach]

## Memory Integration

[Optional - only for agents that learn from interactions]

This agent stores [category] patterns for improved [benefit].

**Memory Categories:**
- **[Category 1]:** [What gets stored and why]
```

---

## TOKEN BUDGET BREAKDOWN

| Section | Tokens | Lines | Notes |
|---------|--------|-------|-------|
| **Frontmatter** | 100-150 | 20-35 | L1 - Always loaded |
| **Expertise** | 100-150 | 5-10 | Rich domain depth |
| **Identity** | 50-75 | 3-5 | Concise role |
| **When to Use** | 200-400 | 25-50 | 2-4 examples |
| **Core Capabilities** | 150-250 | 15-25 | 8-15 bullets |
| **Domain Sections** | 800-1,500 | 100-200 | Flexible bulk |
| **Boundaries** | 100-200 | 10-20 | 5-10 rules |
| **Tool Awareness** | 100-150 | 10-15 | Graceful degradation |
| **Memory Integration** | 50-100 | 5-10 | Optional |
| **TOTAL** | **1,650-2,975** | **~600-900** | Within budget |

---

## MIGRATION PATHS

### From BMAD Agent → Unified Template

| BMAD Section | Action | Unified Location |
|--------------|--------|------------------|
| `<session_config>` | **REMOVE** | N/A - user-specific |
| `<response_gate>` | **REMOVE** | N/A - not for Task tool |
| `<core_identity>` | **CONDENSE** | `## Identity` (1-3 sentences) |
| `<specialized_expertise>` | **KEEP** | `## Core Capabilities` |
| `<operational_mindset>` | **CONDENSE** | Merge into `## Expertise` |
| `<behaviors>` | **TRANSFORM** | `## [Domain Sections]` with examples |
| `<challenge_patterns>` | **REMOVE** | N/A - interactive use |
| `<red_lines>` | **CONDENSE** | `## Boundaries` |
| `<ultimate_goal>` | **CONDENSE** | Last paragraph of `## Expertise` |
| `<menu>` | **REMOVE** | N/A - slash commands |

### From Claude-MPM Agent → Unified Template

| Claude-MPM Section | Action | Unified Location |
|--------------------|--------|------------------|
| `description` with `<example>` | **SPLIT** | description (no examples) + `## When to Use` |
| `type` field | **RENAME** | `agent_type` |
| BASE_ENGINEER duplication | **REMOVE** | Only unique content |

---

## VALIDATION CHECKLIST

Before an agent is considered "unified template compliant":

- [ ] Frontmatter has all REQUIRED fields
- [ ] `description` is 150-300 chars with NO `<example>` tags
- [ ] `agent_type` is valid value from list
- [ ] `tags` has 5-10 searchable keywords
- [ ] Body has `## Expertise` (not duplicate of description)
- [ ] Body has `## When to Use` with 2-4 `<example>` blocks
- [ ] Body has `## Boundaries` with clear refusal rules
- [ ] Body has `## Tool Awareness` with graceful degradation
- [ ] Total tokens within 1,650-2,975 budget
- [ ] Total lines within 600-900 range
- [ ] No persona narratives ("You are an elite veteran...")
- [ ] No session_config or hardcoded paths
- [ ] No response_gate or menu sections

---

## EDGE CASE TEMPLATES

### Orchestrator Agent
```yaml
agent_type: orchestrator
orchestrates: [dev, qa, architect, security]
```
Body adds: `## Delegation Patterns` section

### Security Research Agent
```yaml
agent_type: specialist
authorization: educational-research
```
Body adds: `## Security Protocols` section

### Language-Specific Agent
```yaml
agent_type: engineer
languages: [python]
frameworks: [django, fastapi]
```
Body adds: `## [Language] Patterns` section

### Deprecated Agent
```yaml
deprecated: true
deprecated_notice: "Use unified-agent-builder workflow instead"
```

---

*Specification created Session 4 | 2025-12-11 | Ready for approval*
