# Claude-Hybrid Architectural Decisions

**Project:** Claude-Hybrid
**Repository:** https://github.com/Enginex0/Claude-Hybrid
**Created:** 2025-12-07 (Session 5)
**Last Updated:** 2025-12-07

---

## Brainstorming Methodology

| Aspect | Approach |
|--------|----------|
| **Facilitator** | BMad Master (maintains persona throughout) |
| **Style** | Hybrid - BMad Master + brainstorming techniques |
| **Techniques** | Divergent-convergent exploration, constraint mapping, trade-off analysis, synthesis |
| **Subagents** | Spawned for targeted deep-dives when needed |
| **Decision Authority** | President makes ALL decisions |
| **Principle** | Precision over speed |

---

## Decision Status Summary

| # | Decision | Status | Choice | Session |
|---|----------|--------|--------|---------|
| D1 | Execution Model | **DECIDED** | **Hybrid Model** | 5 |
| D2 | Enforcement Mechanism | PENDING | - | - |
| D3 | Multi-Agent Strategy | PENDING | - | - |
| D4 | State Tracking | PENDING | - | - |
| D5 | Context Management | PENDING | - | - |

**Legend:** PENDING | IN_PROGRESS | DECIDED | REVISED

---

## Decision Dependencies

```
D1 (Execution Model) ─── FOUNDATIONAL
        │
        ├──► D2 (Enforcement) ─── Depends on execution model
        │           │
        │           └──► D3 (Multi-Agent) ─── Depends on enforcement approach
        │                       │
        │                       └──► D4 (State Tracking) ─── Depends on agent model
        │
        └──► D5 (Context Management) ─── Partially independent, informed by D1
```

**Recommended Order:** D1 → D2 → D3 → D4 → D5

---

## D1: Execution Model

**Status:** DECIDED
**Priority:** FOUNDATIONAL - Must be decided first

### The Question

How does Claude-Hybrid execute? Does it deploy configuration and hand off (like Claude-MPM), or does it orchestrate at runtime (like BMAD)?

### Options

| Option | Source | Description |
|--------|--------|-------------|
| **A. Config Deployer** | Claude-MPM | Deploy agents/skills/hooks to ~/.claude/, assemble PM_INSTRUCTIONS.md, then os.execvpe("claude") - MPM process DIES, Claude Code takes over |
| **B. Runtime Orchestrator** | BMAD | workflow.xml executes at runtime, agents activated on-demand, persistent orchestration throughout session |
| **C. Hybrid** | Novel | Combine elements - e.g., deploy static config BUT maintain runtime orchestration layer |

### Trade-offs

| Aspect | Config Deployer (A) | Runtime Orchestrator (B) | Hybrid (C) |
|--------|---------------------|-------------------------|------------|
| **Simplicity** | Simpler - deploy once | Complex - continuous execution | Medium |
| **Control** | Less runtime control | Full runtime control | Flexible |
| **Context** | Lower overhead | Higher overhead | Configurable |
| **Debugging** | Harder (process dies) | Easier (persistent) | Medium |
| **Claude Code Native** | More aligned | Less aligned | Balanced |

### Discussion Notes

**Key insights from brainstorming:**
1. President wants upfront configuration (like MPM) for project-specific tailoring
2. President ALSO wants runtime control (like BMAD) for continuous steering
3. Critical insight: Make orchestrator a Claude Code AGENT, not external process
4. This avoids process-death visibility loss while maintaining Claude Code alignment

**The Hybrid Architecture:**
- LAYER 1 (Static): Deploy agents, skills, hooks, MCP config upfront
- LAYER 2 (Runtime): Orchestrator agent (like BMad Master) invokable during session
- NO external process - orchestrator IS a Claude Code agent
- User can invoke/dismiss orchestrator as needed

### Decision

**Choice:** Option C - Hybrid Model
**Rationale:**
- Upfront configuration for project-specific tailoring (from MPM)
- Runtime orchestration for continuous control (from BMAD)
- Orchestrator as Claude Code agent, not external process
- Aligns with President's "know every wire" and "precision" principles
- Flexibility to invoke/dismiss orchestrator as needed
**Date:** 2025-12-07
**Session:** 5

---

## D2: Enforcement Mechanism

**Status:** PENDING
**Depends On:** D1 (Execution Model)

### The Question

How does Claude-Hybrid enforce rules and prevent violations? Through hooks that can block actions, or through instructional workflow rules?

### Options

| Option | Source | Description |
|--------|--------|-------------|
| **A. Hook-Enforced** | Claude-MPM | Use PreToolUse hooks to block/modify tool calls. CB#1 & CB#2 are hook-enforced. Only PreToolUse and UserPromptSubmit can block. |
| **B. Instructional** | BMAD | Workflow rules, agent personas with principles, menu-driven constraints. Relies on LLM compliance. |
| **C. Hybrid** | Novel | Critical rules hook-enforced, lesser rules instructional. Tiered enforcement. |

### Trade-offs

| Aspect | Hook-Enforced (A) | Instructional (B) | Hybrid (C) |
|--------|-------------------|-------------------|------------|
| **Reliability** | High - code blocks | Medium - LLM may ignore | High for critical |
| **Flexibility** | Rigid | Flexible | Balanced |
| **Overhead** | Shell scripts execute | No overhead | Selective overhead |
| **Debuggability** | Clear block reasons | Harder to trace | Medium |

### Discussion Notes

*(To be captured during brainstorming)*

### Decision

**Choice:** TBD
**Rationale:** TBD
**Date:** TBD
**Session:** TBD

---

## D3: Multi-Agent Strategy

**Status:** PENDING
**Depends On:** D1, D2

### The Question

How do multiple agents collaborate in Claude-Hybrid? Do they discuss in parallel (Party Mode), or delegate sequentially?

### Options

| Option | Source | Description |
|--------|--------|-------------|
| **A. Party Mode** | BMAD | 2-3 agents selected per message based on domain/expertise. Cross-talk enabled. Collaborative discussion. |
| **B. Sequential Delegation** | Claude-MPM | PM delegates to one agent at a time via Task tool. Agent completes, returns, PM decides next. |
| **C. Hybrid** | Novel | Default sequential, but Party Mode available for specific scenarios (brainstorming, code review). |

### Trade-offs

| Aspect | Party Mode (A) | Sequential (B) | Hybrid (C) |
|--------|----------------|----------------|------------|
| **Richness** | Multi-perspective | Single-focus | Contextual |
| **Control** | Harder to direct | Easy to direct | Flexible |
| **Context** | Higher usage | Lower usage | Optimized |
| **Complexity** | Complex orchestration | Simple | Medium |

### Discussion Notes

*(To be captured during brainstorming)*

### Decision

**Choice:** TBD
**Rationale:** TBD
**Date:** TBD
**Session:** TBD

---

## D4: State Tracking

**Status:** PENDING
**Depends On:** D1, D2, D3

### The Question

How does Claude-Hybrid track workflow state, progress, and context across sessions?

### Options

| Option | Source | Description |
|--------|--------|-------------|
| **A. Frontmatter Tracking** | BMAD | YAML frontmatter in workflow files tracks stepsCompleted, variables, phase. Files ARE state. |
| **B. Tickets + PM_INSTRUCTIONS** | Claude-MPM | mcp-ticketer for task tracking, PM_INSTRUCTIONS.md assembled per session (~108KB). |
| **C. Hybrid** | Novel | Frontmatter for workflow state, lightweight ticket system for tasks, structured decision files. |

### Trade-offs

| Aspect | Frontmatter (A) | Tickets (B) | Hybrid (C) |
|--------|-----------------|-------------|------------|
| **Simplicity** | Files are state | Separate DB | Medium |
| **Queryability** | Manual | Structured | Mixed |
| **Context Load** | Distributed | Centralized | Optimized |
| **Portability** | Git-native | DB dependent | Git-native |

### Discussion Notes

*(To be captured during brainstorming)*

### Decision

**Choice:** TBD
**Rationale:** TBD
**Date:** TBD
**Session:** TBD

---

## D5: Context Management

**Status:** PENDING
**Depends On:** D1 (partially independent)

### The Question

How does Claude-Hybrid manage the 200k context limit? What loading/unloading strategies does it use?

### Options

| Option | Source | Description |
|--------|--------|-------------|
| **A. Step-Files + Progressive Disclosure** | BMAD | Micro-files loaded just-in-time. 3-level skill loading (L1 metadata → L2 entry → L3 refs). |
| **B. Template Externalization** | Claude-MPM | 48.1% token reduction via file references instead of inline content. Templates in separate files. |
| **C. Hybrid** | Novel | Step-files for workflows, template externalization for prompts, 3-level progressive disclosure for skills. |

### Trade-offs

| Aspect | Step-Files (A) | Externalization (B) | Hybrid (C) |
|--------|----------------|---------------------|------------|
| **Token Savings** | High (JIT loading) | High (48.1% reduction) | Highest |
| **Complexity** | File management | Reference management | Both |
| **Flexibility** | Very flexible | Structured | Balanced |
| **Implementation** | YAML/MD parsing | File refs | Both |

### Discussion Notes

*(To be captured during brainstorming)*

### Decision

**Choice:** TBD
**Rationale:** TBD
**Date:** TBD
**Session:** TBD

---

## Session Log

| Session | Date | Decisions Made | Notes |
|---------|------|----------------|-------|
| 1-4 | 2025-12-07 | None | Documentation analysis, 100% coverage achieved |
| 5 | 2025-12-07 | **D1: Hybrid Model** | Brainstorming methodology established, this file created, D1 decided |

---

## Key Reference Files

| File | Purpose |
|------|---------|
| `/home/president/Claude-Hybrid/.claude/claude-progress.txt` | Chronological progress log |
| `/home/president/Claude-Hybrid/.claude/session-roundup.md` | Session handoff context |
| `/home/president/Claude-Hybrid/docs/CORE-VISION.md` | Original vision document |
| `/home/president/bmad-systems/personal bmad/BMAD-PERSONAL-ARCHITECTURE.md` | President's desired setup |

---

## Amendment History

| Date | Change | Reason |
|------|--------|--------|
| 2025-12-07 | Initial creation | Session 5 - brainstorming preparation |

---

*This document is the single source of truth for Claude-Hybrid architectural decisions. Update after each decision is made.*
