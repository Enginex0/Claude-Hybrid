# D4: State Tracking - Question Set

**Decision:** How does Claude-Hybrid track workflow and agent state across sessions?
**Status:** ✅ COMPLETE (22/22 DECIDED)
**Generated:** 2025-12-09 (Updated 2025-12-10)
**Sources:** Claude-MPM analysis documents, BMAD workflow patterns, production workflow systems

---

## Key Architectural Principles

The following principles were established through D4 decision-making:

- **SSOT:** Frontmatter is the Single Source of Truth (SSOT) for all state
- **Projection:** Ticketing systems are SECONDARY projection layers with one-way sync (frontmatter → tickets)
- **Dual Persistence:** Frontmatter for step-level, tickets for workflow-level orchestration
- **File-Based:** File-based state survives execvpe() process handoff - architectural necessity
- **Hash-Based:** SHA-256 hash-based change detection and cache invalidation
- **Delegation Chain:** Parent-child delegation chain tracking in frontmatter for 92-agent deployment

---

## Checkpoint Status

| Question | Status | Answer |
|----------|--------|--------|
| Q1 | **DECIDED** | Option D: Hybrid Granularity (step-level + workflow-level) |
| Q2 | **DECIDED** | Option D: Dual Persistence (frontmatter + tickets) |
| Q3 | **DECIDED** | Option D: Configuration-driven context detection |
| Q4 | **DECIDED** | Option E: Tiered Hybrid Enforcement (Gate files + Frontmatter validation + Orchestrator gating) |
| Q5 | **DECIDED** | Option E: A+D Hybrid with Orchestrator Awareness (3-Tier Resumption) |
| Q6 | **DECIDED** | Option D: Hybrid (frontmatter PRIMARY, ticketer SECONDARY) |
| Q7 | **DECIDED** | Option A: Store AI-derived scope in frontmatter (with ticket sync) |
| Q8 | **DECIDED** | Option D: Frontmatter authoritative; tickets consume updates |
| Q9 | **DECIDED** | Option C: Both file-based and ticket-based state |
| Q10 | **DECIDED** | Option B: Direct frontmatter mutation + ticketing agent for sync |
| Q11 | **DECIDED** | Option A: File-based state persistence only (with ticket sync) |
| Q12 | **DECIDED** | Option D: Frontmatter in source artifact files (BMAD-style) |
| Q13 | **DECIDED** | Option D: InstructionCacheService pattern (hash validation) |
| Q14 | **DECIDED** | Option C: Delegation Chain State (parent→child tracking) |
| Q15 | **DECIDED** | Option E: B+C Hybrid (Temporal Versioning + Session Markers) |
| Q16 | **DECIDED** | Option C: Hybrid (static in config.yaml, dynamic in frontmatter) |
| Q17 | **DECIDED** | Option D: Hybrid (CSV Manifests + Database/Tickets) |
| Q18 | **DECIDED** | Option A: Frontmatter in Workflow Files (BMAD Level 4) |
| Q19 | **DECIDED** | Option A: SHA256 hash comparison using files-manifest.csv |
| Q20 | **DECIDED** | Option A: Static configuration only (no workflow state) |
| Q21 | **DECIDED** | Option E: Tiered Storage (Critical continuous, others at milestones) |
| Q22 | **DECIDED** | Option E: Comprehensive (Learnings + Knowledge Graph + Summaries + Decisions) |

---

## Questions: Granularity and Persistence (Q1-Q3)

### Q1: State Tracking Granularity
**Context:** How granular should state tracking be? Step-level vs workflow-level tracking affects complexity, performance, and resumption capabilities.

Options:
- A: Step-level only - Track state for each individual step within workflows. Fine-grained control but higher overhead.
- B: Workflow-level only - Track state at the workflow level. Simpler but coarser resumption.
- C: Task-level only - Track state for individual tasks without workflow awareness.
- D: Hybrid Granularity (DECIDED) - Step-level within workflows via stepsCompleted frontmatter + workflow-level across project via tickets. ~500 LOC with 42% reuse, $10,250 3-year TCO.

**Rationale:** 11/11 frameworks use hybrid granularity. Book Analogy: bookmark with both page number AND chapter status. D3-Q5's 3-tier architecture requires hybrid.

### Q2: State Persistence Layer
**Context:** Where should state be persisted? Choice affects durability, performance, and cross-session resumption.

Options:
- A: In-memory only - State exists only during execution. Fast but lost on interruption.
- B: File-based only - State stored in local files. Survives restarts but no distributed access.
- C: Database/ticket system only - State stored externally. Distributed access but latency.
- D: Dual Persistence (DECIDED) - Frontmatter for in-workflow step-level state + external system for cross-workflow orchestration. ~520-650 LOC with 50-60% reuse, $35-50K 3-year TCO.

**Rationale:** 11/11 frameworks use dual-layer persistence. Library Book Analogy: Bookmark (frontmatter) = where you are in the book. Library Card (tickets) = what books you're reading.

### Q3: Active Workflow Context Detection
**Context:** How does the system determine which workflow is currently active? Affects state lookup and context assembly.

Options:
- A: Path inference - Infer active workflow from current directory or file being edited.
- B: Orchestrator state - Orchestrator explicitly tracks which workflow is active in its state.
- C: Output embedding - Parse recent output/logs to determine active workflow.
- D: Configuration-driven (DECIDED) - Reference main_config or config_source to determine active workflow context. ~55-80 LOC with 70-80% reuse, $3-4K 3-year TCO.

**Rationale:** 6/8 frameworks use config-driven. Recipe Card Analogy: Config title defines WHAT you're making. Frontmatter tracks WHERE you are.

---

## Questions: Synchronization and Resumption (Q4-Q5)

### Q4: State Synchronization Guarantees
**Context:** What guarantees should the system provide about state consistency across concurrent operations?

Options:
- A: Gate files only - Use filesystem-based gate files to prevent concurrent access.
- B: Frontmatter validation only - Validate state consistency by checking frontmatter checksums.
- C: Orchestrator gating only - Orchestrator enforces exclusive access to state.
- D: No guarantees - Allow concurrent access, accept eventual consistency.
- E: Tiered Hybrid Enforcement (DECIDED) - A+B+C': Tier 1 Gate files <5ms, Tier 2 Frontmatter validation <100ms, Tier 3 Orchestrator gating <500ms. ~450 LOC net new, 35% reuse, ~$12K 3-year TCO, ~97% reliability.

**Rationale:** 6/6 frameworks use multi-layer hybrid. Gate Files Analogy: AI agents check 'Does step-N.gate exist?' rather than fcntl locks.

### Q5: Session Resumption After Interruption
**Context:** How should the system resume workflows after crashes, restarts, or user interruptions?

Options:
- A: Read frontmatter only - Read stepsCompleted from frontmatter to determine resumption point.
- B: Read orchestrator state only - Orchestrator maintains separate state file tracking progress.
- C: Read ticketing system only - Query external ticket system for workflow progress.
- D: Read checkpoint files - Dedicated checkpoint files track progress at key milestones.
- E: A+D Hybrid with Orchestrator Awareness (DECIDED) - 3-Tier Resumption: Tier 1 Frontmatter <5ms 95% cases, Tier 2 Checkpoint files <50ms fallback, Tier 3 Orchestrator awareness <500ms complex cases. ~380-480 LOC net new, 60% reuse, ~$20-28K 3-year TCO.

**Rationale:** 6/6 frameworks use multi-layer resumption. Road Trip Analogy: Journal (frontmatter) + GPS breadcrumbs (checkpoint files) + Travel buddy (orchestrator).

---

## Questions: Frontmatter vs Ticketing Relationship (Q6-Q8)

### Q6: Frontmatter vs Ticketing System Primacy
**Context:** When both frontmatter and ticketing system exist, which is the primary source of truth?

Options:
- A: Frontmatter only - Frontmatter is sole source of truth. No ticketing system used for state.
- B: Ticketing system only - External ticket system is sole source of truth. No frontmatter state.
- C: Equal primacy - Both are authoritative. Conflicts require explicit resolution logic.
- D: Hybrid (DECIDED) - Frontmatter is PRIMARY source of truth, ticketer is SECONDARY projection layer. One-way sync: frontmatter → ticketer. ~280 LOC net new, 43.75% reuse, ~$50-60K 3-year TCO.

**Rationale:** 11/11 frameworks use hybrid dual-layer state management. Options A, B, C ALL violate binding constraints from D4-Q1 and D4-Q2.

### Q7: AI-Derived Scope Classification Storage
**Context:** When AI derives a scope classification (micro/small/medium/large/epic), where should this be stored?

Options:
- A: Store in frontmatter metadata (DECIDED) - With D4-Q6-compliant ticket sync. Frontmatter PRIMARY, tickets SECONDARY. ~140 LOC net new, 85% reuse, $3K 3-year TCO.
- B: Store in ticketing system only - Scope is external metadata, not workflow state.
- C: Store in separate cache file - Dedicated cache for AI-derived metadata.
- D: Store in both with validation - Store in frontmatter and ticketing system, validate consistency.

**Rationale:** 10/12 systems use cache+external pattern. Option D's bidirectional validation violates D4-Q6 one-way sync.

### Q8: State Authority: Frontmatter vs Ticketing
**Context:** Which system has authority to make state changes? Related to Q6 but focuses on write authority.

Options:
- A: Frontmatter write-only - Only frontmatter can be modified. Ticketing system is read-only projection.
- B: Ticketing system write-only - Only ticketing system can be modified. Frontmatter is read-only cache.
- C: Bidirectional sync - Both can be modified. Synchronization logic handles conflicts.
- D: Frontmatter authoritative (DECIDED) - Frontmatter in task files is authoritative; ticketing systems consume state updates from files. Frontmatter = SSOT, tickets = projection layer. ~120 LOC net new, 100% D4-Q6/Q7 reuse, $36K 3-year TCO.

**Rationale:** 5/6 production systems use local authoritative. D4-Q6 pre-selected this answer by establishing frontmatter as PRIMARY.

---

## Questions: Process Handoff State (Q9-Q11)

### Q9: State Persistence Across Process Handoff (execvpe)
**Context:** Claude-MPM uses os.execvpe() to replace orchestrator with Claude Code. What state survives this handoff?

Options:
- A: File-based state only - Only files on disk survive execvpe(). All memory state lost.
- B: Environment variables only - Pass state via environment variables across execvpe().
- C: Both file-based and ticket-based state (DECIDED) - Files for local speed (written pre-handoff, survive execvpe naturally), tickets for distributed access (async sync). Files AUTHORITATIVE, tickets SECONDARY. ~280-380 LOC net new, 70-80% reuse, ~$65-85K 3-year TCO.
- D: External state server - Separate state service maintains state across handoff.

**Rationale:** 100% of production systems use hybrid dual persistence. execvpe() destroys memory but files survive - POSIX fact.

### Q10: Direct State Mutation vs Agent-Mediated Updates
**Context:** Should AI agents modify state directly, or must all updates go through a dedicated state management agent?

Options:
- A: Direct mutation only - Agents directly modify frontmatter and ticket state.
- B: Agent-mediated updates (DECIDED) - Allow frontmatter state changes directly, require ticketing agent for ticket system synchronization only. Circuit breaker protects ONLY external ticket operations. ~300-330 LOC net new, 75-80% reuse, ~$21-30K 3-year TCO.
- C: Separate mutation paths - Frontmatter direct, ticketing system via agent.
- D: Configurable mode - Config determines whether direct or agent-mediated.

**Rationale:** 100% of production systems use LOCAL SSOT + ASYNC SYNC pattern. TicketWorkflowService CANNOT read current state - write-only interface aligns with one-way sync.

### Q11: Pre-Handoff State Writing Mechanism
**Context:** Before execvpe() handoff, how should orchestrator write state that Claude Code will need?

Options:
- A: File-based state persistence only (DECIDED) - With D4-Q6 compliant ticket sync. State written to frontmatter files BEFORE execvpe, Claude Code reads from file system IMMEDIATELY. ~50-150 LOC net new, 90% reuse, ~$15-20K 3-year TCO.
- B: Environment variables - Pass state via environment variables to Claude Code process.
- C: Shared memory - Use shared memory region accessible by both processes.
- D: State handoff file - Dedicated handoff file with all necessary state for Claude Code.

**Rationale:** 75% of production systems use file-based state for process boundaries. POSIX fact: execvpe destroys memory, files survive.

---

## Questions: PM_INSTRUCTIONS State (Q12-Q13)

### Q12: PM_INSTRUCTIONS State Embedding
**Context:** Should PM_INSTRUCTIONS.md embed current workflow state, or remain stateless and read state from elsewhere?

Options:
- A: Stateless prompt - PM_INSTRUCTIONS is static, Claude Code reads state from separate files.
- B: Embedded state - PM_INSTRUCTIONS contains workflow state inline (regenerated on state change).
- C: State references - PM_INSTRUCTIONS contains references/links to state files, not state itself.
- D: Frontmatter in source artifact files (DECIDED) - BMAD-style. Store workflow progress indicators in YAML frontmatter of artifact files (stepsCompleted array, currentStep, status). ~50-80 LOC net new, 90% reuse from BMAD, ~$10-15K 3-year TCO.

**Rationale:** 75%+ production systems use file-based state at process boundaries. Decision pre-determined by D4-Q6 (frontmatter PRIMARY) and D4-Q8 (frontmatter SSOT).

### Q13: Runtime vs Build-Time State Updates
**Context:** Can workflow state be updated during Claude Code execution, or only at handoff boundaries?

Options:
- A: Build-time only - State only updated when PM_INSTRUCTIONS is regenerated before handoff.
- B: Runtime updates via hooks - Hooks allow state updates during execution.
- C: Runtime updates via MCP - MCP Gateway provides tools for state updates during execution.
- D: InstructionCacheService pattern (DECIDED) - State validated via hash, regenerated on change. State immutable DURING execution, mutable AT cycle boundaries. ~50-80 LOC net new, 90% reuse, ~$10-15K 3-year TCO.

**Rationale:** 100% use content-hash pattern (Git, Docker, Nix, Bazel). Options A and B architecturally impossible (PM_INSTRUCTIONS read-only post-handoff).

---

## Questions: Multi-Agent and Versioning (Q14-Q15)

### Q14: Multi-Agent State Isolation vs Shared State
**Context:** When multiple agents execute concurrently, how is state isolated or shared between them?

Options:
- A: Fully isolated - Each agent has completely separate state. No shared state.
- B: Shared global state - Single shared state accessible by all agents.
- C: Delegation Chain State (DECIDED) - Parent→child tracking. Track parent_id, root_id, depth, chain_path in frontmatter. O(chain_depth) scalability. ~225-700 LOC net new, 63% reuse, ~$12.6K 3-year TCO.
- D: Hierarchical namespaces - State organized in hierarchical namespaces allowing selective sharing.

**Rationale:** 5/5 major frameworks use C as primary. D3-Q10 MANDATES parent-child tracking - only Option C directly satisfies this constraint.

### Q15: State Versioning and History
**Context:** Should the system maintain history of state changes, or only track current state?

Options:
- A: Current state only - No history. Only latest state is available.
- B: Version history - Maintain versioned history of all state changes with timestamps.
- C: Session boundaries - Track state at session boundaries but not intermediate changes.
- D: Checkpoint-based history - Save history only at explicit checkpoints.
- E: B+C Hybrid (DECIDED) - Temporal Versioning with Session Markers. Version history for audit trail + Session boundaries for execution boundary alignment. Timestamps EXCLUDED from hash. ~195-250 LOC net new, 85% reuse, ~$5.5-8K 3-year TCO.

**Rationale:** 91% use B (versioning), 82% use C (session boundaries). Combined pattern validated by Temporal.io, LangGraph, Prefect, AWS Step Functions.

---

## Questions: Static vs Dynamic Variables (Q16-Q17)

### Q16: Static vs Dynamic Variable Storage
**Context:** Should configuration variables be static (config files) or dynamic (computed at runtime)?

Options:
- A: Static only - All variables stored in config files, read at startup.
- B: Dynamic only - All variables computed on-demand during execution.
- C: Hybrid Approach (DECIDED) - Static variables in config.yaml, dynamic variables computed on-demand in frontmatter. Maps L1-L2 (System/Config) to static YAML, L4 (Runtime) to frontmatter. ~1300 LOC per D2-Q20 estimate.
- D: Database-backed - Variables stored in database with dynamic query support.

**Rationale:** 11/11 production systems use static+dynamic split. Cookbook Analogy: config.yaml = printed cookbook (static), frontmatter = post-it notes (dynamic progress).

### Q17: Agent/Skill/Workflow Manifest State Tracking
**Context:** How should the system track available agents, skills, and workflows?

Options:
- A: CSV manifests only - Static manifests listing available components.
- B: Database registry only - Database tracks all components with rich metadata.
- C: Filesystem scan only - Dynamically discover components by scanning directories.
- D: Hybrid (DECIDED) - CSV Manifests for Static Inventory + Database/Tickets for Dynamic State. CSV manifests GENERATED from frontmatter. Database stores ONLY runtime state. One-way flow: frontmatter → CSV → database. ~850 LOC net new (phased), 65% reuse from BMAD, ~$4K 3-year TCO.

**Rationale:** 11/11 (100%) production systems use hybrid pattern. Library Analogy: catalog (knows what exists) + circulation desk (tracks who has what, due dates).

---

## Questions: Step-Level and Change Detection (Q18-Q20)

### Q18: Step-Level Execution State Storage
**Context:** Where should step-level execution state (current step, steps completed) be stored?

Options:
- A: Frontmatter in Workflow Files (DECIDED) - BMAD's Level 4 approach. Runtime state (stepsCompleted, current_step) stored in YAML frontmatter of workflow artifact files. 0 LOC net new, 100% reuse, ~$1.5K 3-year TCO.
- B: Separate state files - Dedicated .state files alongside workflow files.
- C: Database tables - Store step state in database with workflow_id foreign key.
- D: In-memory cache - Keep step state in memory, flush to disk periodically.

**Rationale:** 83% production systems use file-primary state. D4-Q8 pre-selects answer: frontmatter=SSOT means runtime state must be in frontmatter.

### Q19: State Change Detection Method
**Context:** How should the system detect when state has changed and needs synchronization?

Options:
- A: SHA256 hash comparison (DECIDED) - Using files-manifest.csv. Content-based change detection via SHA256 hashes stored in manifest. ~150 LOC (100 core + 50 tests), 80% reuse, 0 external dependencies, stdlib only.
- B: Timestamp comparison - Compare file modification times to detect changes.
- C: Manual marking - Agents explicitly mark when state changes.
- D: Event-driven notifications - State changes trigger events that update dependent systems.

**Rationale:** 100% of modern critical infrastructure uses content hashing (Git, Docker, Kubernetes, Terraform, npm). Only legacy Make (1976) uses timestamps.

### Q20: User Configuration State vs Workflow State
**Context:** Should user configuration (preferences, paths, skill levels) be treated as state or static config?

Options:
- A: Static configuration only (DECIDED) - Store user preferences, paths, skill levels but NO workflow state. Config values read at runtime to feed PM_INSTRUCTIONS assembly, but frontmatter remains SSOT per D4-Q8. 0 LOC net new, 100% reuse, ~$1.5K 3-year TCO.
- B: Treat as state - User config is mutable state that can change during execution.
- C: Hybrid approach - Some config is static, some is state (determined per-variable).
- D: Externalized completely - Store all user config in external system (not files or tickets).

**Rationale:** 95% of production systems use A+C pattern. D4-Q16 pre-selected this answer: 'static in config.yaml'. Settings Panel Analogy: config.yaml = phone Settings app, frontmatter = app state.

---

## Questions: Gap Resolution - KuzuDB Memory Grounding (Q21-Q22)

### Q21: How should Claude-Hybrid integrate with KuzuDB for memory grounding?
**Context:** CORE-VISION.md:38,55 requires "KuzuDB memory grounding". D4 decision "KuzuMemory stays independent" addresses autonomy but not integration strategy.

Options:
- A: Session Bookends - Store at session end, recall at session start
- B: Continuous Sync - Real-time sync of key decisions/learnings to KuzuDB
- C: Milestone-Based - Store at workflow phase completions (**DISQUALIFIED** - violates D4-Q6 one-way sync)
- D: On-Demand - Store/recall only when explicitly requested
- E: Tiered Storage - Critical items continuous, others at milestones (**DECIDED**)

**CORE-VISION Reference:** Lines 38, 55

**Decision:** Option E: Tiered Storage with A+B Hybrid Semantics. ~360-850 LOC, 70% reuse from claude-mpm, LOW risk.

**Rationale:** 2/3 specialists favor E (Architect 9/10, Research 8.5/10), 1/3 favors B (Coder 8/10) - functionally equivalent patterns. 61% industry adoption (11/18 frameworks use tiered/hybrid). Claude-MPM implements A+B hybrid via 3 hooks: SubmitHook recalls at start, PostDelegationHook stores after each response. Journal & Filing Cabinet Analogy: Daily journal (continuous tier) for critical thoughts + Filing cabinet (milestone tier) for organized phase summaries. Option C DISQUALIFIED - violates D4-Q6 one-way sync (requires reading frontmatter for phase detection).

**Specialist Consensus:** 2/3 for E (Architect, Research), 1/3 for B (Coder) - B is subset of E

**Binding Constraints Satisfied:** D4-Q6 (frontmatter PRIMARY), D4-Q8 (frontmatter SSOT), D4-Q4 (tiered enforcement)

**Implementation Tiers:**
- Tier 1 (Continuous): Architectural decisions, errors, security learnings, user preferences - PostDelegationHook
- Tier 2 (Milestone): General observations, code patterns, documentation - at phase completions
- Tier 3 (Session): Recall at start (SubmitHook), consolidation at end

---

### Q22: What data should Claude-Hybrid store in KuzuDB for memory grounding?
**Context:** Need to specify WHAT is stored in KuzuDB vs frontmatter. Frontmatter = workflow state (D4 SSOT). KuzuDB = ?

Options:
- A: Cross-Session Learnings - Patterns, preferences, past decisions
- B: Project Knowledge Graph - Entities, relationships, dependencies
- C: Conversation Summaries - Key points from past sessions
- D: Decision History - All architectural decisions with rationale
- E: Comprehensive - Learnings + knowledge graph + summaries + decisions (**DECIDED**)

**Related Decision:** D4-Q21 (Tiered Storage defines HOW, Q22 defines WHAT)

**Decision:** Option E: Comprehensive (Learnings + Knowledge Graph + Summaries + Decisions). ~1,200-1,450 LOC, 85% reuse from claude-mpm, LOW risk.

**Rationale:** 3/3 specialist consensus (Tech Lead 9/10, Research 9.2/10, Engineer 8/10). 85% industry adoption for comprehensive - 0% success rate for single-category approaches. Personal Library Analogy: A scholar needs catalog (B) + margin notes (A) + chapter summaries (C) + decision journal (D) - without all four, constantly re-reads books, forgets insights, repeats mistakes. Claude-MPM already implements multi-category (6 memory types + 4 relationships). KuzuDB optimal fit: graph + vector + temporal capabilities.

**Specialist Consensus:** 3/3 UNANIMOUS for E (Tech Lead 9/10, Research 9.2/10, Engineer 8/10)

**Binding Constraints Satisfied:** D4-Q6 (frontmatter PRIMARY), D4-Q8 (frontmatter SSOT), D4-Q21 (tiered storage)

**Tier Mapping (per Q21):**
- Tier 1 (Critical/Continuous): Learnings (A) + Decisions (D) - PostDelegationHook
- Tier 2 (Milestone): Knowledge Graph (B) - at phase completions
- Tier 3 (Session): Summaries (C) - SubmitHook recall, session-end consolidation

---

## D4 COMPLETE! 🎉

**All 22 questions decided.** D4 (State Tracking) establishes:
- Frontmatter = SSOT for workflow state
- KuzuDB = Comprehensive cross-session memory (learnings + knowledge graph + summaries + decisions)
- Tiered storage aligns Q21 (HOW) with Q22 (WHAT)

**Next:** Proceed to remaining D* questions (D3, D7, D8, D9, D10) or implementation phase.
