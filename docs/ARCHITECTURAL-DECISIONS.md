# Claude-Hybrid Architectural Decisions

**Project:** Claude-Hybrid
**Repository:** https://github.com/Enginex0/Claude-Hybrid
**Created:** 2025-12-07 (Session 5)
**Last Updated:** 2025-12-11

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

| # | Decision | Status | Choice | Questions |
|---|----------|--------|--------|-----------|
| D1 | Execution Model | ✅ **DECIDED** | **Hybrid Model** | 1 |
| D2 | Enforcement Mechanism | ✅ **DECIDED** | **Hybrid Tiered Enforcement** | 20 |
| D3 | Multi-Agent Strategy | ✅ **DECIDED** | **Tiered Hybrid Multi-Agent** | 20 |
| D4 | State Tracking | ✅ **DECIDED** | **Frontmatter SSOT + Ticket Projection** | 20 |
| D5 | Context Management | ✅ **DECIDED** | **3-Level Progressive Disclosure** | 20 |
| D6 | Process Boundaries & Initialization | ✅ **DECIDED** | **os.execvpe + MCP Gateway + 12-Phase Init** | 18 |
| D7 | MCP Integration | ✅ **DECIDED** | **Aggregator + Progressive Disclosure** | 16 |
| D8 | Plugin & Agent Format | ✅ **DECIDED** | **Standard Manifest + Tiered Permissions** | 14 |
| D9 | Path Variables & File Structure | ✅ **DECIDED** | **Hybrid Resolution + Module-First** | 16 |
| D10 | Workflow Engine & Lifecycle | ✅ **DECIDED** | **Hybrid Executor + Deep Merge** | 14 |

**Legend:** ✅ DECIDED | 🔄 IN_PROGRESS | ⏳ PENDING

**🎉 ALL 159 ARCHITECTURAL DECISIONS COMPLETE (Sessions 1-78+)**

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

**Status:** DECIDED (20/20 questions complete)
**Depends On:** D1, D2
**Sessions:** 22-44

### The Question

How do multiple agents collaborate in Claude-Hybrid? Do they discuss in parallel (Party Mode), or delegate sequentially?

### Decision Summary

**Choice:** Tiered Hybrid Multi-Agent Strategy

Claude-Hybrid uses a **tiered hybrid approach** combining Party Mode for exploration with Sequential Delegation for execution:

```
TIER 1: USER-DIRECTED
├── User explicitly selects agents
├── Full control, no inference
└── Highest priority

TIER 2: SCENARIO-BASED (~80%)
├── Party Mode for exploration/brainstorming
├── Sequential Delegation for implementation
└── Orchestrator selects based on task type

TIER 3: INTELLIGENT SCORING (~15%)
├── Manifest-based agent selection
├── 2-3 relevant agents for parallel work
└── Domain expertise matching

TIER 4: ROTATION MODIFIER (~5%)
├── Prevents agent fixation
├── Introduces variety when appropriate
└── Secondary mechanism only
```

### D3 Sub-Decisions (20 Questions)

| # | Topic | Decision |
|---|-------|----------|
| Q1 | Agent Selection | Option E: Tiered Hybrid Selection (User-Directed > Scenario-Based > Intelligent Scoring > Rotation) |
| Q2 | Cross-Talk | Option D: Contextual Hybrid (Party Mode for brainstorm, Sequential for implementation) |
| Q3 | Termination | Option E: State-Managed with Mode-Tiered Mechanisms (~220 LOC) |
| Q4 | Party vs Sequential | Option D: Exploration vs Execution (Party=divergent, Sequential=deliverables) |
| Q5 | State Management | Option D: Hybrid 3-Tier (Working Memory, Session State/Frontmatter, Persistent/Tickets) |
| Q6 | Sub-Agent Invocation | Option E: Tiered Hybrid (User-Directed > Orchestrator-Validated > Proactive Triggers > Injection Hints) |
| Q7 | Specialization Granularity | Option D: Tiered Role-Based (Orchestrator, Phase Leads, Role Specialists, Sub-Agents, ~25-30 agents) |
| Q8 | Output Format | Option E: Tiered Output (Complete message 90-95%, File artifacts 5-10%, JSON metadata supplementary) |
| Q9 | Installation Location | Option C: Hybrid with Priority (Project > User > System, ~520 LOC, $18.5K 3-year TCO) |
| Q10 | Delegation Pattern | Option A: Hierarchical Single-Parent (Task returns to same parent, cross-branch via Orchestrator) |
| Q11 | IDE vs Web | Option B: Dual Orchestrator Pattern (BMad Master for IDE, BMad Web for Web, 185 LOC) |
| Q12 | Agent Transformation | Option C: Hybrid with User Override (Orchestrator suggests, user accepts/overrides) |
| Q13 | Party Mode Selection | Option C: Agent Manifest-Driven (dynamically select 2-3 agents via manifest, ~380-480 LOC) |
| Q14 | Persona Conflict | Option D: Hierarchical Persona Authority (role-based tier hierarchy, ~200 LOC net new) |
| Q15 | Agent Pool Scoping | Option E: Project Config with Sensible Defaults (all available by default, optional scoping) |
| Q16 | Agent Matching | Option A: Filename Stem Matching (Claude Code native, O(1) lookup, 0 LOC) |
| Q17 | Discovery Priority | Option B: Project Highest (Project > Remote > User > System, 50-80 LOC) |
| Q18 | PM Delegation | Option E: Hierarchical Manifest + Direct Task Invocation (~220 LOC, 90% reuse) |
| Q19 | Skill Loading | Option E: Tiered Registry with Agent Scoping (Registry-based + Project>User>System, ~55 LOC) |
| Q20 | Hot-Reload | Option D: Session Boundary Only (Claude Code native, 0 LOC - already implemented) |

### Key Architectural Patterns

1. **Exploration vs Execution Split** (D3-Q4)
   - Party Mode: Brainstorming, creative exploration, divergent thinking
   - Sequential Delegation: Implementation, deliverables, focused execution

2. **Hierarchical Single-Parent** (D3-Q10)
   - Task tool returns to same parent
   - Cross-branch communication via Orchestrator only
   - Prevents 41-86.7% failure rates from unrestricted delegation

3. **Dual Orchestrator** (D3-Q11)
   - BMad Master for IDE (file I/O, manifests, 18 handlers)
   - BMad Web Orchestrator for Web (embedded XML, no file I/O)

4. **3-Tier State Management** (D3-Q5)
   - Tier 1: Working Memory (conversation context)
   - Tier 2: Session State (frontmatter)
   - Tier 3: Persistent State (tickets)

### Industry Validation

- 100% of production systems use hybrid approaches
- 0/8 use pure Party Mode or pure Sequential in production
- LangGraph, CrewAI, AutoGen, Temporal, Prefect all validate tiered patterns

### Implementation Impact

| Component | LOC Estimate |
|-----------|-------------|
| Agent Selection Tiering | ~400 |
| Cross-Talk Controller | ~1,420 |
| State Management | ~240 |
| Sub-Agent Invocation | ~500 |
| Installation Priority | ~520 |
| Delegation Chain | ~280 |
| Manifest Selection | ~480 |
| **Total D3 Multi-Agent Layer** | **~3,840 LOC** |

**Date:** 2025-12-08 to 2025-12-09
**Sessions:** 22-44 (23 sessions)

---

## D4: State Tracking

**Status:** DECIDED (20/20 questions complete)
**Depends On:** D1, D2, D3
**Sessions:** 45-60

### The Question

How does Claude-Hybrid track workflow state, progress, and context across sessions?

### Decision Summary

**Choice:** Frontmatter SSOT + Ticket Projection

Claude-Hybrid uses **frontmatter as Single Source of Truth (SSOT)** with tickets as a secondary projection layer:

```
FRONTMATTER (SSOT - PRIMARY)
├── stepsCompleted array
├── current_step
├── status
├── Stored IN workflow artifact files
└── Files survive process boundaries (execvpe)

TICKETS (SECONDARY - PROJECTION)
├── One-way sync: frontmatter → tickets
├── Async sync after MCP Gateway available
├── Query interface for cross-workflow visibility
└── Conflict resolution: frontmatter always wins
```

### D4 Sub-Decisions (20 Questions)

| # | Topic | Decision |
|---|-------|----------|
| Q1 | Granularity | Option D: Hybrid (step-level in frontmatter + workflow-level in tickets, ~500 LOC) |
| Q2 | Persistence Layer | Option D: Dual (frontmatter for in-workflow + external for cross-workflow, ~650 LOC) |
| Q3 | Context Identification | Option D: Configuration-driven (reference main_config, ~80 LOC) |
| Q4 | Enforcement | Option E: Tiered Hybrid (Gate files + Frontmatter validation + Orchestrator gating, ~450 LOC) |
| Q5 | Session Resumption | Option E: A+D Hybrid 3-Tier (Frontmatter + Checkpoint files + Orchestrator awareness, ~480 LOC) |
| Q6 | Ticket Sync | Option D: Hybrid with frontmatter PRIMARY, tickets SECONDARY, one-way sync (~280 LOC) |
| Q7 | Scope Classification | Option A: Store AI-derived scope in frontmatter metadata with ticket sync (~140 LOC) |
| Q8 | Authoritative Source | Option D: Frontmatter is SSOT; tickets consume state updates from files (~120 LOC) |
| Q9 | Process Boundary | Option C: Both file-based and ticket-based - files AUTHORITATIVE, tickets SECONDARY (~380 LOC) |
| Q10 | Circuit Breaker Tracking | Option B: Allow frontmatter changes directly, require ticketing agent for sync only (~330 LOC) |
| Q11 | Process Boundary Persistence | Option A: File-based state persistence only with D4-Q6 compliant ticket sync (~150 LOC) |
| Q12 | Progress Indicators | Option D: Frontmatter in source artifact files (BMAD-style, ~80 LOC) |
| Q13 | State Validation | Option D: InstructionCacheService pattern - hash validated, regenerated on change (~80 LOC) |
| Q14 | Delegation Chain | Option C: Delegation Chain State (parent→child tracking, ~225-700 LOC) |
| Q15 | Temporal Context | Option E: B+C Hybrid - Version history + Session markers, timestamps excluded from hash (~250 LOC) |
| Q16 | Variable Storage | Option C: Hybrid - Static in config.yaml, dynamic in frontmatter (~1300 LOC per D2-Q20) |
| Q17 | Component Tracking | Option D: Hybrid CSV Manifests + Database (CSV generated from frontmatter, ~850 LOC) |
| Q18 | Runtime State | Option A: Frontmatter in Workflow Files (BMAD Level 4, 0 LOC - pattern exists) |
| Q19 | Change Detection | Option A: SHA256 hash comparison using files-manifest.csv (~150 LOC) |
| Q20 | Config vs State | Option A: Static configuration only - NO workflow state in config.yaml (0 LOC - pattern exists) |

### Key Architectural Patterns

1. **Single Source of Truth (SSOT)** (D4-Q6, Q8)
   - Frontmatter = authoritative state
   - Tickets = secondary projection layer
   - One-way sync: frontmatter → tickets
   - Conflict resolution: frontmatter always wins

2. **3-Tier Resumption** (D4-Q5)
   - Tier 1: Frontmatter (<5ms, 95% cases)
   - Tier 2: Checkpoint files (<50ms fallback)
   - Tier 3: Orchestrator awareness (<500ms complex cases)

3. **Hash-Based Validation** (D4-Q13, Q19)
   - SHA-256 content hashing
   - State immutable DURING execution
   - Regenerated AT cycle boundaries
   - Timestamps EXCLUDED from hash

4. **Delegation Chain Tracking** (D4-Q14)
   - parent_id, root_id, depth, chain_path
   - O(chain_depth) scalability
   - Enables debugging, recovery, audit

### Industry Validation

- 11/11 frameworks use dual-layer state management
- 100% use file-based state at process boundaries
- Git, Docker, Kubernetes, Terraform all use content-hash patterns
- POSIX fact: execvpe destroys memory, files survive

### Implementation Impact

| Component | LOC Estimate |
|-----------|-------------|
| Hybrid Granularity (D4-Q1) | ~500 |
| Dual Persistence (D4-Q2) | ~650 |
| Tiered Enforcement (D4-Q4) | ~450 |
| 3-Tier Resumption (D4-Q5) | ~480 |
| Ticket Sync (D4-Q6) | ~280 |
| Hash Validation (D4-Q13) | ~80 |
| Delegation Chain (D4-Q14) | ~700 |
| Component Tracking (D4-Q17) | ~850 |
| **Total D4 State Tracking Layer** | **~3,990 LOC** |

**Date:** 2025-12-09 to 2025-12-10
**Sessions:** 45-60 (16 sessions)

---

## D5: Context Management

**Status:** DECIDED (20/20 questions complete)
**Depends On:** D1 (partially independent)
**Sessions:** 61-71

### The Question

How does Claude-Hybrid manage the 200k context limit? What loading/unloading strategies does it use?

### Decision Summary

**Choice:** 3-Level Progressive Disclosure

Claude-Hybrid uses **BMAD-style step-files with 3-level progressive disclosure** for optimal context management:

```
L1: METADATA (Always Loaded)
├── Skill name, description
├── Available commands/capabilities
├── ~50-200 tokens per skill
└── Enables discovery without bloat

L2: ENTRY POINT (On Activation)
├── SKILL.md core instructions
├── Primary workflow content
├── ~1,000-2,500 tokens per step
└── Loaded when skill/workflow invoked

L3: REFERENCES (On Demand)
├── Deep-dive documentation
├── Examples, edge cases
├── Loaded via explicit Read tool
└── 50-98% token savings
```

### D5 Sub-Decisions (20 Questions)

| # | Topic | Decision |
|---|-------|----------|
| Q1 | Step Loading | Option A: Strict Sequential (only current step in memory, must complete in order, ~200 LOC) |
| Q2 | Step Granularity | Option A: Fine Granularity (1,000-2,500 tokens per step, avg 1,400, ~150 LOC) |
| Q3 | Workflow State Format | Option A: Frontmatter State in Output File (stepsCompleted, current_step, ~120 LOC) |
| Q4 | Workflow File Format | Option A: Dual Format Support (Markdown for complex, YAML for simple, ~250 LOC) |
| Q5 | Track Impact | Option E: Track as Workflow Selection + Loading Strategies (~330 LOC) |
| Q6 | Skill Priority | Option A: Project > User > Bundled (PRE-SELECTED by D3-Q9, 0 LOC - already implemented) |
| Q7 | Progressive Disclosure | Option A: Full 3-Level (L1 always, L2 on activation, L3 on demand, 1,378 LOC exists) |
| Q8 | Skill Restart | Option A: Require Explicit Restart (PRE-SELECTED by D3-Q20, 0 LOC - Claude Code native) |
| Q9 | Agent Discovery | Option C: Manifest-Based Selective Loading with progressive disclosure (~390 LOC) |
| Q10 | Skill Invocation | Option A: Registry-Based Linking Only (PRE-SELECTED by D3-Q16, -13 LOC simplification) |
| Q11 | Template Externalization | Option C: Hybrid Inline/External (critical-path inline, supplementary external, ~320 LOC) |
| Q12 | Cache Layering | Option C: Hash-Based Primary (SHA-256 as PRIMARY, TTL as secondary cleanup, ~420 LOC) |
| Q13 | Template Invalidation | Option A: Hash-Based Invalidation (SHA-256 content hashing, ~15 LOC) |
| Q14 | ETag Versioning | Option A: Full ETag Implementation (HTTP conditional + SHA-256 + SQLite, ~20 LOC) |
| Q15 | Template Organization | Option A: Categorical Templates (flat directory with semantic naming, 0 LOC) |
| Q16 | Skill Directory Structure | Option A: Three-tier Structure (SKILL.md + references/ + examples/, ~200 LOC) |
| Q17 | Skill Registry Loading | Option D: Progressive Loading (L1 always, L2 on activation, L3 on-demand, ~200 LOC) |
| Q18 | Skill Namespacing | Option B: Shorthand when unambiguous with tier-based priority foundation (~80 LOC) |
| Q19 | Reference Access | Option C: Reference files never auto-loaded; Claude uses Read tool based on hints (~210 LOC) |
| Q20 | Agent Restrictions | Option B: Single response model (PRE-SELECTED by D3-Q8, ~175 LOC) |

### Key Architectural Patterns

1. **Step-File Discipline** (D5-Q1, Q2)
   - Only current step in memory
   - Strict sequential loading
   - 1,000-2,500 tokens per step
   - BMAD mandate: "NEVER load multiple step files simultaneously"

2. **3-Level Progressive Disclosure** (D5-Q7, Q16, Q17)
   - L1: Metadata always loaded (~50-200 tokens)
   - L2: Entry point on activation (~1,000-2,500 tokens)
   - L3: References on demand (50-98% savings)
   - Validated by Anthropic MCP (98.7% reduction)

3. **Hash-Based Caching** (D5-Q12, Q13)
   - SHA-256 content hashing as PRIMARY
   - TTL as secondary cleanup mechanism
   - InstructionCacheService pattern
   - Aligns with D4-Q13, Q19 decisions

4. **Shorthand Namespacing** (D5-Q18)
   - Use simple 'skill-name' when unique
   - Require 'plugin:skill' only on conflicts
   - Project > User > System priority

### Industry Validation

- Anthropic MCP: 98.7% token reduction with progressive disclosure
- 70% of agent failures from context overflow (CMU research)
- LangChain lazy_load() is production standard
- 8/8 frameworks use sequential-by-default loading

### Implementation Impact

| Component | LOC Estimate |
|-----------|-------------|
| Sequential Loading (D5-Q1) | ~200 |
| Fine Granularity Steps (D5-Q2) | ~150 |
| Dual Format Support (D5-Q4) | ~250 |
| Progressive Disclosure (D5-Q7) | 0 (exists) |
| Manifest-Based Discovery (D5-Q9) | ~390 |
| Hybrid Externalization (D5-Q11) | ~320 |
| Hash-Based Caching (D5-Q12) | ~420 |
| Three-tier Structure (D5-Q16) | ~200 |
| **Total D5 Context Management Layer** | **~1,930 LOC** |

**Date:** 2025-12-10
**Sessions:** 61-71 (11 sessions)

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
| 22-23 | 2025-12-08 | **D3-Q1, Q2** | Agent Selection + Cross-Talk patterns |
| 24-25 | 2025-12-08 | **D3-Q3, Q4** | Termination + Exploration vs Execution |
| 26-27 | 2025-12-08 | **D3-Q5, Q6** | 3-Tier State + Sub-Agent Invocation |
| 28-29 | 2025-12-09 | **D3-Q7, Q8** | Role Specialization + Output Format |
| 30-31 | 2025-12-08 | **D3-Q9, Q10** | Installation Location + Delegation Pattern |
| 32-33 | 2025-12-08 | **D3-Q11, Q12** | Dual Orchestrator + Agent Transformation |
| 34-35 | 2025-12-09 | **D3-Q13, Q14** | Party Mode Selection + Persona Conflict |
| 36-37 | 2025-12-09 | **D3-Q15, Q16** | Agent Pool Scoping + Agent Matching |
| 38-39 | 2025-12-09 | **D3-Q17, Q18** | Discovery Priority + PM Delegation |
| 40-41 | 2025-12-09 | **D3-Q19** | Skill Loading with Research timeout correction |
| 42-44 | 2025-12-09 | **D3-Q20 - D3 COMPLETE** | Hot-Reload - Claude Code native behavior |
| 45-46 | 2025-12-09 | **D4-Q1, Q2** | Hybrid Granularity + Dual Persistence |
| 47-48 | 2025-12-09 | **D4-Q3, Q4** | Config-Driven Context + Tiered Enforcement |
| 49-50 | 2025-12-09 | **D4-Q5, Q6** | 3-Tier Resumption + Frontmatter SSOT |
| 51-52 | 2025-12-09 | **D4-Q7, Q8** | Scope Classification + Authoritative Source |
| 53-54 | 2025-12-09 | **D4-Q9, Q10** | Process Boundary + Circuit Breaker |
| 55-56 | 2025-12-09 | **D4-Q11, Q12, Q13** | File Persistence + Progress Indicators + Hash Validation |
| 56 | 2025-12-09 | **D4-Q15** | DEVIATION: Manual ultrathink deployment - President corrected |
| 57 | 2025-12-09 | **D4-Q16** | DEVIATION REPEATED - Same error despite reading log |
| 58-59 | 2025-12-10 | **D4-Q14, Q17** | Delegation Chain + Component Tracking |
| 60 | 2025-12-10 | **D4-Q18, Q19, Q20 - D4 COMPLETE** | Runtime State + Change Detection + Config vs State |
| 61-62 | 2025-12-10 | **D5-Q1, Q2** | Sequential Loading + Fine Granularity |
| 63-64 | 2025-12-10 | **D5-Q3, Q4, Q5, Q6** | Frontmatter State + Dual Format + Track Impact + Skill Priority |
| 65 | 2025-12-10 | **D5-Q7, Q8** | Progressive Disclosure + Skill Restart |
| 66 | 2025-12-10 | **D5-Q9, Q10** | Agent Discovery + Skill Invocation (parallel) |
| 67 | 2025-12-10 | **D5-Q11, Q12** | Template Externalization + Cache Layering (parallel) |
| 68 | 2025-12-10 | **D5-Q13, Q14** | Template Invalidation + ETag Versioning (parallel) |
| 69 | 2025-12-10 | **D5-Q15, Q16** | Template Organization + Skill Directory (parallel) |
| 70 | 2025-12-10 | **D5-Q17, Q18** | Skill Registry Loading + Namespacing (parallel) |
| 71 | 2025-12-10 | **D5-Q19, Q20 - D5 COMPLETE** | Reference Access + Agent Restrictions - **ALL DECISIONS COMPLETE!** |

---

## Key Reference Files

| File | Purpose |
|------|---------|
| `/home/president/bmad-systems/Claude-Hybrid/.claude/claude-progress.txt` | Chronological progress log |
| `/home/president/bmad-systems/Claude-Hybrid/.claude/session-roundup.md` | Session handoff context |
| `/home/president/bmad-systems/Claude-Hybrid/docs/CORE-VISION.md` | Original vision document |
| `/home/president/bmad-systems/personal bmad/BMAD-PERSONAL-ARCHITECTURE.md` | President's desired setup |

---

## Amendment History

| Date | Change | Reason |
|------|--------|--------|
| 2025-12-07 | Initial creation | Session 5 - brainstorming preparation |
| 2025-12-08 | D2 COMPLETE | Session 21 - All 20 D2 questions decided |
| 2025-12-09 | D3 COMPLETE | Session 44 - All 20 D3 questions decided |
| 2025-12-10 | D4 COMPLETE | Session 60 - All 20 D4 questions decided |
| 2025-12-10 | D5 COMPLETE | Session 71 - All 20 D5 questions decided |
| 2025-12-11 | **MAJOR UPDATE** | Synced from decision-workflow.json - D3/D4/D5 fully documented |

---

## Total Implementation Estimate

| Layer | LOC Estimate |
|-------|-------------|
| D2: Enforcement | ~3,310 |
| D3: Multi-Agent | ~3,840 |
| D4: State Tracking | ~3,990 |
| D5: Context Management | ~1,930 |
| **Total Claude-Hybrid Core** | **~13,070 LOC** |

*Plus significant BMAD/claude-mpm reuse (50-90% depending on component)*

---

*This document is the single source of truth for Claude-Hybrid architectural decisions. Update after each decision is made.*
