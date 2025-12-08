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
| D2 | Enforcement Mechanism | **DECIDED** | **Hybrid Tiered Enforcement** | 6-21 |
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

**Status:** DECIDED (20/20 questions complete)
**Depends On:** D1 (Execution Model)
**Sessions:** 6-21

### The Question

How does Claude-Hybrid enforce rules and prevent violations? Through hooks that can block actions, or through instructional workflow rules?

### Decision Summary

**Choice:** Hybrid Tiered Enforcement

Claude-Hybrid uses a **three-tier enforcement architecture** that combines programmatic hooks for critical operations with instructional guidance for soft operations:

```
TIER 1: HOOK-ENFORCED (Critical) - 99.9%+ reliability
├── Circuit breakers CB#1, CB#2, CB#6
├── Config loading & variable resolution for System/Path variables
├── Security boundaries, destructive actions
└── PreToolUse blocks with fail-fast

TIER 2: STRUCTURAL (Hard) - 95%+ reliability
├── Workflow step ordering via mandates + hooks
├── Menu handler routing (schema at load + hook at invocation)
├── Config variable validation during agent activation
└── Checkpoint enforcement with configurable levels

TIER 3: INSTRUCTIONAL (Soft) - 70-90% reliability
├── Communication style, user preferences
├── Computed variables, soft fallbacks
├── Non-critical workflow guidance
└── Progress updates, quality checkpoints
```

### D2 Sub-Decisions (20 Questions)

| # | Topic | Decision |
|---|-------|----------|
| Q1 | Hook Events | Option E: Hybrid-Optimized (SessionStart + PreToolUse + Stop) |
| Q2 | Hook Priority | Option C: Orchestrator Semantic Grouping (P10/P20/P50/P80/P90) |
| Q3 | Response Schema | Option B: Block/Allow/Modify (decision + reason + updatedInput) |
| Q4 | Hook Integration | Option C: Hybrid (Claude Code External + MPM Internal) |
| Q5 | Failure Modes | Option C+D: Circuit-Breaker + Graceful Degradation |
| Q6 | CB Enforcement | Option D: 4-Layer CB Architecture (hooks + state + instructions + monitoring) |
| Q7 | Hook Blocking Return | Option F: Extended D2-Q3 + Translator Compliance |
| Q8 | Effectiveness Gap | Option D+C: Two-Tier + Monitoring (Hard=95% hooks, Soft=measurable) |
| Q9 | Error Recovery | Option D+B: Separate + Logging + Selective Hooks Influence |
| Q10 | Exception Classes | Option B: Unified Exception Hierarchy |
| Q11 | Enforcement Hooks | Option E: Confirms D2-Q1 (SessionStart + PreToolUse + Stop) |
| Q12 | Violation Communication | Option D: Combined (reason + additionalContext) |
| Q13 | Tool Granularity | Option D: Layered (baseline * + specific exceptions) |
| Q14 | Script vs Orchestrator | Option D: Scripts Delegate to Orchestrator (thin proxy → Python RuleEngine) |
| Q15 | Multi-Step Workflows | Option E: 4-Phase Lifecycle (SessionStart + PreToolUse + PreCompact + Stop) |
| Q16 | Step Ordering | Option D: Hybrid Enforcement (mandates + hooks for critical) |
| Q17 | User Checkpoints | Option D: Configurable Enforcement Levels (HARD/SOFT tiers) |
| Q18 | Menu Handler Routing | Option D: Dual-Layer Enforcement (schema at load + hook at invocation) |
| Q19 | Critical Actions | Option D: Tiered Criticality (hook for critical, instructional for soft) |
| Q20 | Variable Resolution | Option C: Hybrid Resolution (hooks for System/Path, LLM for Config/User) |

### Key Architectural Patterns

1. **Scripts Delegate to Orchestrator** (D2-Q14)
   - Thin shell proxy (~50 LOC) → Python RuleEngine (~350 LOC)
   - 89% LOC reduction vs pure script approach
   - Centralized policy enforcement

2. **4-Phase Workflow Lifecycle** (D2-Q15)
   - SessionStart: Load rules, restore state
   - PreToolUse: Enforce, validate prerequisites
   - PreCompact: Checkpoint state before compaction
   - Stop: Validate completion, audit trail

3. **Two-Tier Violation Handling** (D2-Q8, D2-Q12)
   - HARD violations: Block + permissionDecisionReason
   - SOFT violations: Allow + additionalContext warning

4. **Variable Resolution Cascade** (D2-Q20)
   - CRITICAL (System/Path): Hook-enforced, fail-fast
   - HARD (Config): Structural validation, mandatory activation step
   - SOFT (Computed): LLM with fallbacks

### Industry Validation

- 10/10 production systems use programmatic enforcement for critical operations
- 0 counterexamples found using instructional-only
- LangChain InjectedToolArg pattern validates D2-Q20 approach
- Temporal, Airflow, Prefect, LangGraph, CrewAI all use tiered enforcement

### Implementation Impact

| Component | LOC Estimate |
|-----------|-------------|
| RuleEngine (D2-Q14 base) | ~350 |
| 4-Phase Lifecycle (D2-Q15) | ~290 |
| Hybrid Enforcement (D2-Q16) | ~320 |
| Tiered Config (D2-Q17) | ~300 |
| Dual-Layer Menu (D2-Q18) | ~300 |
| Tiered Criticality (D2-Q19) | ~450 |
| Variable Resolution (D2-Q20) | ~1300 |
| **Total D2 Enforcement Layer** | **~3,310 LOC** |

**Date:** 2025-12-08
**Sessions:** 6-21 (16 sessions)

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
| 6 | 2025-12-07 | **D2-Q1** | Ultrathink pattern established, Option E (Hybrid-Optimized) |
| 7 | 2025-12-07 | **D2-Q2, Q3** | Hook priority + Response schema decisions |
| 8 | 2025-12-07 | **D2-Q4, Q5** | Workflow state file created for 5-step enforcement |
| 9 | 2025-12-07 | **D2-Q6** | 4-Layer CB Architecture |
| 10 | 2025-12-07 | **D2-Q7** | Extended D2-Q3 + Translator Compliance |
| 11 | 2025-12-07 | **D2-Q8** | DOCS_FIRST_THEN_CODE enforcement added |
| 12 | 2025-12-07 | **D2-Q9** | Error recovery with selective hooks |
| 13 | 2025-12-07 | **D2-Q10** | 50% milestone - Unified Exception Hierarchy |
| 14 | 2025-12-07 | **D2-Q11** | Question redundancy identified, confirms D2-Q1 |
| 15 | 2025-12-07 | **D2-Q12** | Combined violation communication |
| 16 | 2025-12-08 | **D2-Q13, Q14** | Layered matchers + Scripts delegate |
| 17 | 2025-12-08 | **D2-Q15, Q16** | 4-Phase Lifecycle + Hybrid Enforcement |
| 18 | 2025-12-08 | **D2-Q17** | Configurable Enforcement Levels |
| 19 | 2025-12-08 | **D2-Q18** | Dual-Layer Menu Handler Routing |
| 20 | 2025-12-08 | **D2-Q19** | Tiered Criticality |
| 21 | 2025-12-08 | **D2-Q20 - D2 COMPLETE** | Variable Resolution Cascade - D2 100% complete! |

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
| 2025-12-08 | D2 COMPLETE | Session 21 - All 20 D2 questions decided |

---

*This document is the single source of truth for Claude-Hybrid architectural decisions. Update after each decision is made.*
