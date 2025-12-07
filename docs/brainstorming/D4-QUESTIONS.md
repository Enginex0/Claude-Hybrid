# D4: State Tracking - Question Set

**Decision:** How does Claude-Hybrid track workflow state and progress?
**Status:** PENDING
**Generated:** 2025-12-07 (Session 5)
**Sources:** 4 documents analyzed by subagents

---

## Checkpoint Status

| Question | Status | Answer |
|----------|--------|--------|
| Q1-Q20 | PENDING | - |

---

## Questions from BMAD 05-WORKFLOWS-SYSTEM.md

### Q1: What granularity should state tracking use for workflow progress?
Options:
- A: Step-level tracking (stepsCompleted array tracking individual step numbers like [1, 2, 3])
- B: Phase-level tracking (tracking completion of major phases: Analysis, Planning, Solutioning, Implementation)
- C: Workflow-level tracking (tracking completion of entire workflows like "prd: complete", "architecture: in-progress")
- D: Hybrid granularity (step-level within workflows + workflow-level across the project lifecycle)

### Q2: Where should workflow state be persisted?
Options:
- A: Output file frontmatter (YAML embedded in the document being created)
- B: Separate state file (centralized .yaml or .json file tracking all workflow states)
- C: Ticket system (state stored in ticket metadata with PM_INSTRUCTIONS assembled at runtime)
- D: Dual persistence (frontmatter for in-workflow state + external system for cross-workflow orchestration)

### Q3: How should workflow type and context be identified during execution?
Options:
- A: Embedded in output frontmatter (workflowType field stored in the document being generated)
- B: Inferred from file path (derive workflow type from the step file location in directory structure)
- C: Explicit orchestrator state (PM/orchestrator agent maintains context in separate tracking mechanism)
- D: Configuration-driven (reference main_config or config_source to determine active workflow context)

### Q4: How should the system enforce sequential step execution and prevent skipping?
Options:
- A: Frontmatter validation (check stepsCompleted array before allowing next step to execute)
- B: Orchestrator gating (PM agent validates step completion before delegating next step)
- C: File-based locking (step files only loaded when previous step marked complete in frontmatter)
- D: Ticket-based workflow (ticket status transitions enforce sequence, blocking next step until previous resolves)

### Q5: How should the system handle workflow resumption after interruption?
Options:
- A: Read frontmatter state (parse stepsCompleted and current_step from output file to resume)
- B: Ticket query (query ticket system for last completed step and resume from there)
- C: Orchestrator memory (PM agent maintains session state and can resume from context)
- D: Checkpoint files (separate checkpoint files created at each step for robust recovery)

---

## Questions from Claude-MPM 07-MCP-TICKETING.md

### Q6: Should state transitions be managed via a ticketing system or through in-file tracking?
Options:
- A: Use mcp-ticketer with 6-state workflow (todo -> in_progress -> ready -> tested -> done, plus blocked)
- B: Use aitrackdown CLI for local fallback with state stored in tickets/ directory structure
- C: Use frontmatter YAML in markdown files to track states, avoiding external dependencies
- D: Hybrid approach where mcp-ticketer syncs external state to local frontmatter for offline resilience

### Q7: How should scope classification be tracked given that it uses AI Judgment rather than programmatic classification?
Options:
- A: Store AI-derived scope classification as frontmatter metadata in task files
- B: Rely on ticket metadata fields in mcp-ticketer to capture scope decisions with no local storage
- C: Use PM_INSTRUCTIONS to embed scope classification guidance, letting each session re-derive scope as needed
- D: Implement a local cache of scope decisions that can be validated against ticket state

### Q8: What is the authoritative source of truth for workflow state when multiple systems exist?
Options:
- A: External ticketing systems via mcp-ticketer are authoritative; local state is a cache
- B: Local aitrackdown tickets/ directory is authoritative; external systems are optional sync targets
- C: PM_INSTRUCTIONS assembled at runtime determines current state based on available sources
- D: Frontmatter in task files is authoritative; ticketing systems consume state updates from files

### Q9: Given that MCP Gateway spawns AFTER handoff (process replacement), how should state persist across this boundary?
Options:
- A: State written to files (frontmatter) before execvpe survives handoff naturally - files are durable
- B: State stored in ticketing systems persists independently of the process lifecycle
- C: Both file-based and ticket-based state should be used - files for local speed, tickets for distributed access
- D: PM_INSTRUCTIONS file is regenerated after handoff, pulling current state from whichever source is available

### Q10: Should the circuit breaker pattern influence how state tracking is architected?
Options:
- A: Centralize all state mutations through the ticketing agent, using tickets as the single state store
- B: Allow frontmatter state changes directly but require ticketing agent for ticket system synchronization
- C: Keep state tracking separate from ticket operations - frontmatter for workflow state, tickets for external visibility
- D: Make ticketing agent responsible for both ticket CRUD and local frontmatter state synchronization

---

## Questions from Claude-MPM 02-ARCHITECTURE-CORE.md

### Q11: How should workflow state survive the process replacement boundary (os.execvpe handoff)?
Options:
- A: File-based state persistence only - All state written to disk before handoff, Claude Code reads independently
- B: Hybrid file + database - Files for runtime consumption, database for durable state tracking across sessions
- C: Embedded state in assembled prompt - Encode current workflow state directly into PM_INSTRUCTIONS sections
- D: Environment variable state passing - Pass lightweight state indicators via the env parameter in os.execvpe

### Q12: Where should workflow progress indicators be tracked given the 10-section PM_INSTRUCTIONS assembly?
Options:
- A: Dedicated section in PM_INSTRUCTIONS (e.g., Section 11: Workflow State) - injected dynamically during assembly
- B: Within existing Memory sections - treat workflow state as a type of memory
- C: Separate file in .claude-mpm/ directory - read by orchestrator but not assembled into prompt
- D: Frontmatter in source artifact files (BMAD-style) - state distributed across workflow artifacts

### Q13: How should state tracking handle the distinction between pre-handoff and post-handoff phases?
Options:
- A: Single unified state store written pre-handoff, immutable post-handoff
- B: Split state: MPM manages config/setup state, Claude Code manages runtime/execution state via separate mechanism
- C: Hook-based state updates - Use Claude Code's native Hooks API to signal state changes back to external persistence
- D: InstructionCacheService pattern - State validated via hash, regenerated on change

### Q14: What granularity of state should be tracked for agent delegations given the 92 deployed agents?
Options:
- A: Global workflow state only - track overall phase
- B: Per-agent state tracking - each agent has independent state in their memory files
- C: Delegation chain state - track parent->child agent relationships and handoff history
- D: Capability-aware state - track state per capability

### Q15: How should temporal context integrate with state tracking?
Options:
- A: Temporal context separate from state - date/time is informational only, state tracked elsewhere
- B: Temporal context as state versioning - timestamp each state change for history/audit
- C: Session-based state with temporal boundaries - state scoped to session with temporal metadata
- D: Temporal triggers for state transitions - certain time-based conditions trigger workflow state changes

---

## Questions from BMAD 09-CONFIGURATION.md

### Q16: How should Claude-Hybrid implement the 4-level variable resolution cascade for state tracking?
Options:
- A: Flat approach - collapse all levels into a single config.yaml file
- B: Hierarchical approach - maintain separate resolution layers (system, config, context, runtime)
- C: Hybrid approach - static variables stored in config.yaml, dynamic variables computed on-demand in frontmatter
- D: Database approach - all 4 levels stored in a structured database that assembles full variable context at runtime

### Q17: Should Claude-Hybrid use CSV manifests or a unified database for tracking installed components?
Options:
- A: CSV manifests per component type (workflow-manifest.csv, agent-manifest.csv, etc.) - matches BMAD's approach
- B: Single unified manifest.yaml that contains all component metadata nested hierarchically
- C: Database/ticket system that tracks components as issues or records
- D: Hybrid - CSV manifests for static component inventory, database/tickets for dynamic workflow state

### Q18: Where should runtime state (stepsCompleted, current_step) be tracked?
Options:
- A: Frontmatter in workflow files - BMAD's Level 4 approach where runtime variables live in the workflow markdown itself
- B: Separate state file (state.yaml or similar) in the module directory
- C: PM_INSTRUCTIONS assembled file that aggregates runtime state from multiple sources
- D: External ticketing system where each workflow execution is a ticket with state tracked as fields/status

### Q19: How should configuration changes be detected and propagated?
Options:
- A: SHA256 hash comparison using files-manifest.csv to detect modified files
- B: Config file timestamps with version tracking in manifest.yaml
- C: Event-driven approach where configuration changes trigger notifications to dependent components
- D: Polling approach where components check their config sources periodically for changes

### Q20: What role should the module-level config.yaml files play in state tracking?
Options:
- A: Static configuration only - store user preferences, paths, skill levels but no workflow state
- B: Combined configuration and state - extend config.yaml to include workflow progress and completion status
- C: Configuration source for PM_INSTRUCTIONS - values from config.yaml assembled into instruction file at runtime
- D: Reference only - config.yaml values imported into a database/ticket system which becomes source of truth

---

## Resume Instructions

**Next session:** Read this file, continue from first PENDING question.
**Methodology:** BMad Master facilitates, President decides each question.
**After completion:** Update ARCHITECTURAL-DECISIONS.md with D4 decision.
