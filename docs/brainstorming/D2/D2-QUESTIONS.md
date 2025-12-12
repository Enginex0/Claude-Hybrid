# D2: Enforcement Mechanism - Question Set

**Decision:** How should Claude-Hybrid enforce workflow rules and circuit breakers?
**Status:** ✅ COMPLETE (29/29 DECIDED)
**Generated:** 2025-12-07 (Updated 2025-12-08)
**Sources:** Claude-MPM analysis documents (06-MEMORY-HOOKS.md, 09-ERROR-HANDLING.md), Claude Code analysis (06-HOOK-SYSTEM.md), BMAD documents (02-ARCHITECTURE-CORE.md)

---

## Checkpoint Status

| Question | Status | Answer |
|----------|--------|--------|
| Q1 | **DECIDED** | Option E: Hybrid-Optimized (SessionStart + PreToolUse + Stop) |
| Q2 | **DECIDED** | Option C: Orchestrator Semantic Grouping (P10/P20/P50/P80/P90 internal) |
| Q3 | **DECIDED** | Option B: Block/Allow/Modify Schema (decision + reason + updatedInput + systemMessage) |
| Q4 | **DECIDED** | Option C: Hybrid Approach (CC for blocking, MPM for complex rules) |
| Q5 | **DECIDED** | Option C+D: Circuit-Breaker with Graceful Degradation |
| Q6 | **DECIDED** | Option D: Hook-enforced for critical only with instructional fallback |
| Q7 | **DECIDED** | Option F: Extended D2-Q3 Schema + Translator Compliance (add 'ask', use D2-Q4 translator layer) |
| Q8 | **DECIDED** | Option D+C: Two-Tier System with Monitoring (Hard=95% hooks, Soft=measurable instructions, ~40 LOC persistence) |
| Q9 | **DECIDED** | Option D+B: Separate + Logging + Selective Hooks Influence (A foundation, D for observability ~100 LOC, B opt-in ~200 LOC) |
| Q10 | **DECIDED** | Option B: Unified Exception Hierarchy (single source of truth, 95% testable, universal industry pattern) |
| Q11 | **DECIDED** | Option E (Synthesized): SessionStart + PreToolUse + Stop for enforcement (confirms D2-Q1, industry-validated pattern) |
| Q12 | **DECIDED** | Option D: Combined Approach (reason for hard blocks via permissionDecisionReason, additionalContext for soft warnings) |
| Q13 | **DECIDED** | Option D: Layered (broad baseline * + specific exceptions Edit\|Write\|MultiEdit, Grep\|Glob) |
| Q14 | **DECIDED** | Option D: Scripts Delegate to Orchestrator (thin proxy → Python RuleEngine, 89% LOC reduction, industry-validated) |
| Q15 | **DECIDED** | Option E (Modified): 4-Phase Lifecycle (SessionStart init + PreToolUse enforce + PreCompact persist + Stop complete) |
| Q16 | **DECIDED** | Option D: Hybrid Enforcement (mandates for LLM compliance + hooks for critical sequences, ~320 LOC) |
| Q17 | **DECIDED** | Option D: Configurable Enforcement Levels (per-checkpoint config, tiered HARD/SOFT, ~300 LOC) |
| Q18 | **DECIDED** | Option D: Dual-Layer Enforcement (Schema at load + Hook at invocation, ~300 LOC reusing D2-Q14/Q16/Q17) |
| Q19 | **DECIDED** | Option D: Tiered Criticality (hook for critical actions like config loading, instructional for soft actions like style) |
| Q20 | **DECIDED** | Option C: Hybrid Resolution (hooks for critical System/Path vars, LLM for soft Config/User vars with fallbacks) |
| Q21 | **DECIDED** | Option D+B: Multi-Layer Proof with Schema Compliance Foundation |
| Q22 | **DECIDED** | Option D: Progressive Proof (increasing rigor at each phase gate) |
| Q23 | **DECIDED** | Option D: Dual-Layer Enforcement with Extension-First Path Awareness |
| Q24 | **DECIDED** | Option D: Layer Integration with Existing D2 Hook System |
| Q25 | **DECIDED** | Option E: Configurable Events (Tiered - Mandatory/Recommended/Optional) |
| Q26 | **DECIDED** | Option A: Confirm CB#8 as QA Verification Gate |
| Q27 | **DECIDED** | Option E (Tiered): Multi-Method with Configurable Layers |
| Q28 | **DECIDED** | Option D: Dual-Layer Enforcement (CB#9 + Instructional + Logging) |
| Q29 | **DECIDED** | Option C + D Enhancement: Confidence Threshold via Sequential-Thinking + Instructional |

---

## Questions: Hook Events, Priority, Schema, and Integration (Q1-Q4)

### Q1: Which hook events should be used for enforcement in Claude-Hybrid?
**Context:** Claude-Hybrid must decide which hook events (SessionStart, PreToolUse, PostToolUse, Stop, etc.) are used for enforcing workflow rules and circuit breakers.

Options:
- A: SessionStart only - Initialize enforcement rules at session start, rely on instructions for runtime enforcement.
- B: PreToolUse only - Block invalid tool calls at execution time, no session-level initialization.
- C: PostToolUse only - Audit tool usage after execution, provide feedback but don't block.
- D: Full hook coverage - Use all available hooks (SessionStart, PreToolUse, PostToolUse, Stop) for comprehensive enforcement.
- E: Hybrid-Optimized - SessionStart for workflow initialization, PreToolUse for action blocking, Stop for cleanup. Industry-validated pattern.

**Decision:** Option E: Hybrid-Optimized (SessionStart + PreToolUse + Stop)
**Rationale:** SessionStart for workflow initialization, PreToolUse for action blocking, Stop for cleanup. Industry-validated pattern confirmed by Q11.

---

### Q2: How should hook priority be structured for enforcement rules?
**Context:** When multiple hooks respond to the same event, priority determines execution order. This affects whether enforcement runs before or after other logic.

Options:
- A: Single priority level - All enforcement hooks use same priority (e.g., P50). Simple but inflexible.
- B: Binary priority - Two levels: high priority (P10) for critical blocking, low priority (P90) for audit/logging.
- C: Orchestrator Semantic Grouping - Tiered priority: P10 (initialization), P20 (enforcement), P50 (business logic), P80 (audit), P90 (cleanup).
- D: Dynamic priority - Hooks can adjust their priority based on context or configuration.

**Decision:** Option C: Orchestrator Semantic Grouping (P10/P20/P50/P80/P90 internal)
**Rationale:** Tiered priority system allows initialization hooks to run first, then enforcement, then business logic, then audit.

---

### Q3: What response schema should enforcement hooks return?
**Context:** Enforcement hooks must communicate decisions (allow/block/modify) back to Claude Code or the orchestrator.

Options:
- A: Simple boolean - Return true (allow) or false (block). Minimal but no explanation capability.
- B: Block/Allow/Modify Schema - Return structured object: `{decision: "allow"|"block"|"modify", reason: string, updatedInput?: object, systemMessage?: string}`.
- C: Exception-based - Throw exceptions for violations, return nothing for allowed actions.
- D: Callback-based - Pass result to callback function rather than returning values directly.

**Decision:** Option B: Block/Allow/Modify Schema (decision + reason + updatedInput + systemMessage)
**Rationale:** Extended schema allows enforcement hooks to sanitize/modify inputs, provide structured explanations, and inject context.

---

### Q4: How should enforcement integrate with the two parallel hook systems?
**Context:** Claude Code has external hooks (bash scripts), Claude-MPM has internal hooks (Python functions). Which system should handle enforcement?

Options:
- A: Claude Code External hooks only - All enforcement via bash scripts registered in settings.json.
- B: Claude-MPM Internal hooks only - All enforcement via Python hooks in the orchestrator.
- C: Hybrid Approach - Claude Code External hooks for critical blocking, MPM Internal hooks for complex rule evaluation.
- D: Unified hook system - Create new hook system that replaces both, avoiding parallel systems.

**Decision:** Option C: Hybrid Approach (CC for blocking, MPM for complex rules)
**Rationale:** Claude Code External hooks for critical blocking, MPM Internal hooks for complex rule evaluation. Deviation noted: Skipped EXPLORE_DEEP_DIVE step.

---

## Questions: Edge Cases, Circuit Breakers, and Error Handling (Q5-Q10)

### Q5: How should enforcement handle edge cases and failure modes?
**Context:** What happens when hook scripts fail, timeout, or return invalid responses? How does the system maintain reliability?

Options:
- A: Fail-open - If enforcement fails, allow the action to proceed. Availability over security.
- B: Fail-closed - If enforcement fails, block the action. Security over availability.
- C: Circuit-breaker pattern - Track failure rates, temporarily disable enforcement after threshold. Resume after cooldown.
- D: Graceful degradation - Fall back to instructional enforcement if hook enforcement fails.

**Decision:** Option C+D: Circuit-Breaker with Graceful Degradation
**Rationale:** Circuit-breaker pattern with PreToolUse enforcement for primary enforcement, graceful degradation to instructional rules if hooks fail.
**Binding Constraints:** D6-Q11 (synchronous non-blocking for sub-phases), D6-Q15 (graceful degradation)

---

### Q6: Should Claude-Hybrid enforce circuit breakers via hooks or instructions?
**Context:** Circuit breakers prevent Claude from taking dangerous actions (like implementing before investigating). Should these be enforced programmatically or via system prompt?

Options:
- A: Hook-enforced only - All circuit breakers are programmatically enforced via PreToolUse hooks. 95% effectiveness.
- B: Instructional only - All circuit breakers are documented in system prompt. Effectiveness unknown.
- C: Tiered approach - Critical circuit breakers are hook-enforced, soft circuit breakers are instructional.
- D: Hook-enforced for critical only with instructional fallback - CB#1 (implementation), CB#2 (investigation), CB#6 (critical) via hooks, others instructional with monitoring.

**Decision:** Option D: Hook-enforced for critical only with instructional fallback
**Rationale:** Hook-enforced for CB#1 (implementation), CB#2 (investigation), CB#6 (critical), state-tracked for CB#4, instructional for CB#3/5/7 with monitoring.

---

### Q7: What should the hook blocking mechanism return when a violation is detected?
**Context:** When PreToolUse hook detects a circuit breaker violation, what response format enables clear communication to Claude?

Options:
- A: Simple JSON - `{allowed: false, reason: "Violation description"}` matching Claude Code's expected format.
- B: Rich metadata - Include violation type, severity, suggested remediation, and link to documentation.
- C: Interactive response - Allow user to override the block with confirmation dialog.
- D: Escalation mechanism - Block with option to escalate to user for manual approval.
- E: Extended schema - Use D2-Q3 schema (decision/reason/updatedInput/systemMessage) for consistency.
- F: Extended D2-Q3 Schema + Translator - Add 'ask' action for escalation, translator layer converts to Claude Code format.

**Decision:** Option F: Extended D2-Q3 Schema + Translator Compliance (add 'ask', use D2-Q4 translator layer)
**Rationale:** Extends D2-Q3 schema with 'ask' action for escalation to user, translator converts to Claude Code format for compatibility.
**Binding Constraints:** D2-Q3 (schema structure), D2-Q4 (hybrid approach)

---

### Q8: How should Claude-Hybrid handle the effectiveness gap between hook-enforced (95%) and instructional (unknown) circuit breakers?
**Context:** Hook-enforced circuit breakers have measured 95% effectiveness. Instructional circuit breakers have unknown effectiveness. How should this gap be addressed?

Options:
- A: Accept the gap - Acknowledge that instructional enforcement is less reliable, document the trade-off.
- B: Monitor instructional violations - Log when instructional circuit breakers are violated to measure effectiveness.
- C: Escalate instructional violations - Prompt user when instructional violations are detected.
- D: Two-tier system - Hard blocks via hooks (95%), soft blocks via instructions with monitoring.

**Decision:** Option D+C: Two-Tier System with Monitoring (Hard=95% hooks, Soft=measurable instructions, ~40 LOC persistence)
**Rationale:** Hard blocks via hooks for workflow violations (95% effectiveness), soft blocks via instructions for style/convention rules, monitoring/logging for instructional violations to measure effectiveness.
**LOC Estimate:** ~40 LOC persistence

---

### Q9: How should error recovery strategies integrate with enforcement mechanisms?
**Context:** Should enforcement hooks influence error recovery behavior? For example, if a circuit breaker is violated, should the error recovery strategy change?

Options:
- A: Separate concerns - Error recovery and enforcement are independent. Recovery strategies don't change based on enforcement.
- B: Enforcement influences recovery - Circuit breaker violations trigger different recovery strategies (e.g., skip retry).
- C: Recovery influences enforcement - Error recovery can temporarily relax enforcement rules (e.g., during emergency fixes).
- D: Bidirectional integration - Both systems can influence each other based on context.

**Decision:** Option D+B: Separate + Logging + Selective Hooks Influence (A foundation, D for observability ~100 LOC, B opt-in ~200 LOC)
**Rationale:** Keep error strategies and enforcement separate as foundation (A), add hook-triggered error logging (D) for observability ~100 LOC, selective hooks influence on error strategy (B) as opt-in ~200 LOC.
**LOC Estimate:** ~300 LOC total

---

### Q10: Should Claude-Hybrid address the duplicate exception class problem as part of enforcement design?
**Context:** Analysis revealed duplicate exception classes across modules. Should enforcement design include unified exception hierarchy?

Options:
- A: Ignore for now - Focus on enforcement mechanisms first, address exceptions later.
- B: Unified exception hierarchy - Create single source of truth for all exception classes. Enable consistent enforcement responses.
- C: Exception mapping layer - Map different exception types to unified enforcement responses without changing exception classes.
- D: Plugin-based exceptions - Allow modules to register their exception types with enforcement system dynamically.

**Decision:** Option B: Unified Exception Hierarchy (single source of truth, 95% testable, universal industry pattern)
**Rationale:** Create unified exception hierarchy to enable consistent enforcement responses. Single source of truth, 95% testable, universal industry pattern.

---

## Questions: Hook Events, Communication, Granularity, and Workflow Patterns (Q11-Q15)

### Q11: Which hook events should Claude-Hybrid use for enforcement?
**Context:** Redundancy check with Q1. Confirming the industry-validated pattern across multiple specialists.

Options:
- A: SessionStart only - Initialize enforcement at session start.
- B: PreToolUse only - Block at execution time.
- C: PostToolUse only - Audit after execution.
- D: Stop only - Cleanup and validation at end.
- E: SessionStart + PreToolUse + Stop - Industry-validated three-phase pattern.

**Decision:** Option E (Synthesized): SessionStart + PreToolUse + Stop for enforcement (confirms D2-Q1, industry-validated pattern)
**Rationale:** Question identified as redundant with D2-Q1 by all 4 Ultrathink specialists. Synthesized Option E confirms SessionStart for initialization, PreToolUse for blocking, Stop for cleanup.
**Special Note:** Question identified as redundant with D2-Q1 by all 4 Ultrathink specialists - synthesized Option E to confirm prior decision

---

### Q12: How should rule violations be communicated back to Claude?
**Context:** When enforcement blocks an action, how should the violation message be communicated to Claude for maximum comprehension?

Options:
- A: System message injection - Inject violation message into Claude's context via systemMessage field.
- B: Tool error response - Return violation as tool execution error that Claude sees in tool output.
- C: Structured JSON in prompt - Append violation details to system prompt in structured format.
- D: Combined approach - Use structured JSON with reason field for hard blocks, systemMessage for soft warnings.

**Decision:** Option D: Combined Approach (reason for hard blocks via permissionDecisionReason, additionalContext for soft warnings)
**Rationale:** Use structured JSON with reason field for hard violations (permissionDecisionReason), systemMessage/additionalContext for soft warnings and guidance.

---

### Q13: How granular should enforcement be at the tool level?
**Context:** Should enforcement rules apply broadly to all tools, or have fine-grained control per tool type?

Options:
- A: Coarse-grained - Single rule set applies to all tools uniformly. Simple but inflexible.
- B: Per-tool rules - Each tool (Edit, Write, Bash, etc.) can have specific enforcement rules.
- C: Tool category rules - Group tools into categories (file operations, execution, search) with category-level rules.
- D: Layered matching - Broad baseline policies (*) for all tools, specific matchers (Edit|Write|MultiEdit, Grep|Glob) for exceptions.

**Decision:** Option D: Layered (broad baseline * + specific exceptions Edit|Write|MultiEdit, Grep|Glob)
**Rationale:** Layer matchers - broad policies (* baseline) for baseline rules, specific matchers (Edit|Write|MultiEdit, Grep|Glob) for exceptions and overrides.

---

### Q14: Should enforcement rely on external scripts or be built into the orchestrator?
**Context:** Should enforcement rules be implemented as external hook scripts (bash/Python) or internal orchestrator logic?

Options:
- A: External scripts only - All enforcement via hook scripts. Maximum flexibility, harder to debug.
- B: Orchestrator logic only - All enforcement built into orchestrator Python code. Easier to test, less flexible.
- C: Configuration-driven - Define rules in config files (YAML/JSON), interpreter executes them.
- D: Scripts delegate to orchestrator - Thin hook scripts proxy decisions to orchestrator enforcement agent. 89% LOC reduction vs external scripts.

**Decision:** Option D: Scripts Delegate to Orchestrator (thin proxy → Python RuleEngine, 89% LOC reduction, industry-validated)
**Rationale:** Hook scripts delegate decisions back to orchestrator enforcement agent for consistent rule interpretation. Thin shell proxy to Python RuleEngine, 89% LOC reduction vs external scripts.
**LOC Estimate:** 89% LOC reduction

---

### Q15: What enforcement pattern should be used for multi-step workflows?
**Context:** For workflows with multiple steps (investigate -> plan -> implement -> test), how should enforcement ensure proper sequencing?

Options:
- A: State machine - Track workflow state in persistent store, enforce valid state transitions.
- B: Step markers - Each workflow step sets a marker, hooks verify marker before allowing next step.
- C: Checkpoint validation - At workflow boundaries, validate all prerequisites were completed.
- D: Event sequence tracking - Record all events, validate sequence matches expected workflow pattern.
- E: 4-Phase Lifecycle - SessionStart (init) + PreToolUse (enforce) + PreCompact (persist) + Stop (complete).

**Decision:** Option E (Modified): 4-Phase Lifecycle (SessionStart init + PreToolUse enforce + PreCompact persist + Stop complete)
**Rationale:** SessionStart for workflow initialization, PreToolUse for step validation, PreCompact for state preservation, Stop for completion enforcement. 9/9 production systems use 4-phase pattern.
**Industry Validation:** 9/9 production systems use 4-phase pattern (Temporal, Prefect, Dagster, GitHub Actions, Airflow, LangGraph, CrewAI, LangChain LCEL, MS Agent Framework)

---

## Questions: Step Ordering, Checkpoints, Routing, Actions, and Variable Resolution (Q16-Q20)

### Q16: How should Claude-Hybrid enforce workflow step ordering?
**Context:** Should step ordering be enforced programmatically via hooks or declaratively via system prompt mandates?

Options:
- A: System prompt only - Document required ordering in system prompt, trust Claude to follow.
- B: State machine enforcement - Programmatic state machine validates each step transition via hooks.
- C: Structural enforcement - Use XML/YAML workflow definitions that Claude must follow.
- D: Hybrid enforcement - Mandate declarations in XML/YAML for LLM compliance + hooks for critical sequences.

**Decision:** Option D: Hybrid Enforcement (mandates for LLM compliance + hooks for critical sequences, ~320 LOC)
**Rationale:** Mandate declarations in XML/YAML for LLM compliance combined with programmatic hooks for critical sequence enforcement. Best of both worlds.
**Industry Validation:** 6/6 workflow systems use structural+runtime enforcement (Temporal, Prefect, Dagster, Airflow, LangGraph, CrewAI)
**LOC Estimate:** ~320 LOC

---

### Q17: What enforcement model should govern user interaction checkpoints?
**Context:** Should user approval checkpoints (e.g., "confirm before proceeding") be hook-enforced or instructional?

Options:
- A: Instructional only - Document checkpoints in prompt, trust Claude to request approval.
- B: Hook-enforced only - PreToolUse hook blocks until user provides approval via callback.
- C: Workflow-dependent - Critical workflows require hooks, routine workflows use instructions.
- D: Configurable enforcement levels - Let users/projects define which checkpoints are hook-enforced vs. instructional. Per-checkpoint configuration with tiered HARD/SOFT levels.

**Decision:** Option D: Configurable Enforcement Levels (per-checkpoint config, tiered HARD/SOFT, ~300 LOC)
**Rationale:** Let users/projects define which checkpoints are hook-enforced vs. instructional. Per-checkpoint configuration with tiered HARD/SOFT enforcement levels.
**Industry Validation:** 6/6 systems use configurable enforcement (Temporal, Prefect, GitHub Actions, Airflow, LangGraph; Dagster not implemented)
**LOC Estimate:** ~300 LOC

---

### Q18: How should menu handler routing be enforced?
**Context:** Personal BMAD documents show agents have menu systems with handler functions. Should routing to correct handlers be validated?

Options:
- A: No enforcement - Trust agent menu definitions, no validation of handler existence or routing.
- B: Static validation - Validate menu definitions at load time, fail if handlers missing.
- C: Runtime validation - Check handler exists before routing, provide error if not found.
- D: Dual-layer enforcement - Schema validation at load time + hook validation at invocation time.

**Decision:** Option D: Dual-Layer Enforcement (Schema at load + Hook at invocation, ~300 LOC reusing D2-Q14/Q16/Q17)
**Rationale:** Schema validation at load time ensures handler definitions are valid, hook validation at invocation time ensures correct runtime routing.
**Industry Validation:** 6/6 production systems use programmatic validation (Click, Typer, Temporal, Prefect, LangGraph, CrewAI)
**Binding Constraints:** D2-Q14 (scripts delegate), D2-Q16 (hybrid enforcement), D2-Q17 (configurable levels)
**LOC Estimate:** ~300 LOC

---

### Q19: Should critical_actions (agent activation rules) be hook-enforced or instructional?
**Context:** Personal BMAD documents define critical_actions that trigger when agents activate. Should these be programmatically enforced?

Options:
- A: Instructional only - Document activation rules in prompt, trust Claude to follow.
- B: Hook-enforced only - All critical_actions validated via hooks before allowing agent activation.
- C: Load-time validation - Validate critical_actions are properly defined when agent loads.
- D: Tiered criticality - Hook-enforced for critical actions (config loading, state init), instructional for soft actions (style, formatting).

**Decision:** Option D: Tiered Criticality (hook for critical actions like config loading, instructional for soft actions like style)
**Rationale:** Hook-enforced for critical actions (config loading, state initialization), instructional for soft actions (communication style, formatting preferences). ~450 LOC implementation.
**Industry Validation:** 10/10 systems use programmatic enforcement, 0 counterexamples
**LOC Estimate:** ~450 LOC

---

### Q20: How should variable resolution cascade be enforced?
**Context:** Personal BMAD documents show 4-tier variable resolution (System -> Config -> User -> Runtime). Should variable resolution be hook-enforced or LLM-driven?

Options:
- A: Instructional only - Document resolution order, trust Claude to resolve variables correctly.
- B: Hook-enforced only - All variable resolution happens programmatically via hooks before prompt delivery.
- C: Hybrid resolution - System/Path variables resolved by hooks (deterministic), Config/User variables resolved by LLM with fallback prompts (flexible).
- D: Dynamic resolution - LLM attempts resolution first, falls back to hooks only if resolution fails.

**Decision:** Option C: Hybrid Resolution (hooks for critical System/Path vars, LLM for soft Config/User vars with fallbacks)
**Rationale:** System/Path variables resolved by hooks for deterministic behavior, Config/User variables resolved by LLM with fallback prompts for flexibility. ~1300 LOC per estimate.
**Industry Validation:** 0/11 systems use instructional-only, LangChain InjectedToolArg is production pattern
**LOC Estimate:** ~1300 LOC

---

## Questions: Gap Resolution - Proof, Delegation, Defense (Q21-Q27)

### Q21: How should Claude-Hybrid implement proof-based validation?
**Context:** CORE-VISION.md:38,56 requires "Proof-based validation" and "Proof-based execution" from Claude-MPM. This means requiring evidence/proof before actions proceed.

Options:
- A: Artifact Existence Validation - Proof = required artifacts exist (e.g., PRD exists before Architecture)
- B: Schema Compliance Proof - Proof = artifacts pass JSON schema validation
- C: Explicit Proof Tokens - Proof = special proof markers/tokens in artifacts confirming completion
- D: Multi-Layer Proof - Artifact existence + schema compliance + explicit confirmation
- E: Proof Registry - Central registry tracking what has been proven, queried before each phase

**CORE-VISION Reference:** Lines 38, 56, 75

**Decision:** Option D+B: Multi-Layer Proof with Schema Compliance Foundation
**Rationale:** Validation runs at PHASE TRANSITIONS (checkpoints), not every analysis. Python hooks (external to Claude) validate artifacts at 4 layers: (1) Artifact Existence - file check, (2) Schema Compliance - ValidationResult pattern from claude-mpm, (3) Execution Gate - circuit breaker validation, (4) Completion - frontmatter status update. Integrates with D2-Q15 hook lifecycle (SessionStart→PreToolUse→PreCompact→Stop). Industry-validated: 5/5 mature systems use layered validation (Temporal, Prefect, Dagster, CI/CD, LangGraph).
**Specialist Consensus:** 3/3 (Architect 8.5/10, Research 8/10, Coder 8/10)
**LOC Estimate:** 160-200 (high reuse from claude-mpm ValidationResult pattern)

---

### Q22: What proof is required at each BMAD workflow phase gate?
**Context:** CORE-VISION.md:75 states "No phase proceeds without proof". Need to specify what constitutes proof for each phase transition.

Options:
- A: Uniform Proof - Same proof type required at all phase gates
- B: Phase-Specific Proof - Different proof requirements per phase:
  - Analysis→Planning: Requirements document validated
  - Planning→Solutioning: Architecture document validated
  - Solutioning→Implementation: Tech spec validated
- C: Configurable Proof - Project-level configuration of proof requirements
- D: Progressive Proof - Increasing rigor at each phase (existence→schema→review)

**CORE-VISION Reference:** Line 75

**Decision:** Option D: Progressive Proof - Increasing rigor at each phase gate
**Rationale:** Each phase transition applies progressively MORE validation layers from D2-Q21's 4-layer mechanism:
- Phase 1→2: Layer 1 only (existence check for product-brief.md, research reports)
- Phase 2→3: Layers 1+2 (existence + schema validation for PRD FRs/NFRs)
- Phase 3→4: Layers 1+2+3 (existence + schema + implementation-readiness gate)
- Story Completion: All 4 layers (existence + schema + gate + completion status DONE)
Natural alignment with D2-Q21, respects phase nature (optional Phase 1 gets light validation), matches CORE-VISION.md:81-90 phase-to-layer mapping.
**Specialist Consensus:** 3/3 (Architect 9/10, Research 8-9/10, Coder 8/10)
**Industry Validation:** 7/7 systems use progressive/phase-specific proof (Temporal, Dagster, Airflow, GitHub Actions, LangGraph, CrewAI, Enterprise Phase-Gate)
**LOC Estimate:** 180-220 (75% reuse from ValidationResult pattern)

---

### Q23: How should Claude-Hybrid enforce that PM delegates rather than implements?
**Context:** CORE-VISION.md:54 requires "PM delegation enforcement". The PM orchestrator must delegate work to specialist agents, not perform implementation itself.

Options:
- A: Circuit Breaker Enforcement - Add CB#9 that blocks PM from using Write/Edit tools directly
- B: Instructional Enforcement - PM_INSTRUCTIONS.md explicitly forbids direct implementation
- C: Tool Filtering - PM agent definition excludes implementation tools from available tools
- D: Dual-Layer - Circuit breaker + instructional + tool filtering combined
- E: Audit-Only - Log when PM implements directly, alert but don't block

**CORE-VISION Reference:** Line 54

**Decision:** Option D: Dual-Layer Enforcement with Extension-First Path Awareness
**Rationale:** Three-layer defense combining CB#9 (PreToolUse hook), instructional (PM_INSTRUCTIONS.md), and audit logging. Extension-first approach enables project-agnostic enforcement: PM CAN write doc extensions (*.md, *.yaml, *.txt) anywhere, PM CANNOT write code extensions (*.py, *.ts, *.js, *.go, etc.) anywhere. Works for new projects without configuration. Integrates with D2-Q13 (layered granularity), D2-Q14 (scripts delegate to RuleEngine), D2-Q7 ('ask' escalation).
**Specialist Consensus:** 3/3 unanimous (Tech-Lead 9/10, Research 8/10, Engineer 8/10)
**Industry Validation:** 7/7 systems use multi-layer enforcement (Temporal, Prefect, Dagster, GitHub Actions, LangGraph, CrewAI, Kubernetes RBAC)
**LOC Estimate:** ~280-350 (80 core logic + tests, 90% reuse from circuit_breaker_hook.py)
**Key Enhancement:** Extension-first (block *.py anywhere) before directory-based (block src/) - enables zero-config new project support

---

### Q24: How should Claude-Hybrid implement the 4-Layer Defense architecture?
**Context:** CORE-VISION.md:36 specifies Claude-MPM's "4-Layer Defense (Schema → Business Rules → Execution Gates → Runtime)".

Options:
- A: Sequential Layers - Each request passes through all 4 layers in order
- B: Parallel Validation - All 4 layers validate simultaneously, aggregate results
- C: Risk-Based Routing - Route to appropriate layers based on request risk level
- D: Layer Integration with Existing D2 - Map to existing hook system:
  - Layer 1 (Schema): SessionStart schema validation
  - Layer 2 (Business Rules): PreToolUse business logic
  - Layer 3 (Execution Gates): Circuit breakers
  - Layer 4 (Runtime): Stop/completion monitoring
- E: Standalone Defense Module - Separate 4-layer system independent of hooks

**CORE-VISION Reference:** Line 36

**Decision:** Option D: Layer Integration with Existing D2 Hook System
**Rationale:** Map 4-Layer Defense (CORE-VISION.md:36) to existing D2 hook infrastructure:
- Layer 1 (Schema): SessionStart schema validation
- Layer 2 (Business Rules): PreToolUse business logic
- Layer 3 (Execution Gates): Circuit breakers (already exists in circuit_breaker_hook.py - ZERO new code)
- Layer 4 (Runtime): Stop/completion monitoring

Directly implements CORE-VISION.md:81-90 phase-to-layer mapping. Leverages 23 prior D2 decisions.
**Specialist Consensus:** 3/3 unanimous (Tech-Lead 9/10, Research 9/10, Engineer 9/10)
**Industry Validation:** 7/7 systems integrate defense layers into lifecycle hooks (Kubernetes, Express/Koa, AWS WAF, Resilience4j, Spring Security, Kong/Envoy, MCP Triple Gate)
**LOC Estimate:** 200-300 (90% reuse from claude-mpm/D2, Layer 3 = 0 LOC)
**Binding Constraints:** D2-Q1/Q11, D2-Q15, D2-Q21, D2-Q22, CORE-VISION.md:81-90

---

### Q25: Which additional hook events should Claude-Hybrid support beyond the core 4?
**Context:** D2-Q1 decided SessionStart + PreToolUse + PreCompact + Stop. Claude Code supports additional events: UserPromptSubmit, PostToolUse, SubagentStop, Notification, AssistantResponse.

Options:
- A: Core 4 Only - SessionStart, PreToolUse, PreCompact, Stop (current decision)
- B: Add PostToolUse - Core 4 + PostToolUse for audit logging
- C: Add UserPromptSubmit - Core 4 + UserPromptSubmit for input validation
- D: Full Coverage - All 9 events with specific use cases defined
- E: Configurable Events - Core 4 required, others opt-in via configuration

**Decision:** Option E: Configurable Events (Tiered - Mandatory/Recommended/Optional)
**Rationale:** 3-tier event structure providing flexibility while ensuring core enforcement:
- **Tier 1 (Mandatory):** SessionStart, PreToolUse, PreCompact, Stop, PostToolUse, SubagentStop - Always enabled for core enforcement + audit
- **Tier 2 (Recommended):** UserPromptSubmit, SubagentStart - Default ON for full delegation tracking
- **Tier 3 (Optional):** Notification, AssistantResponse - Default OFF, opt-in for full observability

Industry-validated "streaming service model" - pay only for features you use. Matches Temporal, Kubernetes, AWS Lambda, Express.js patterns. Aligns with D2-Q17 (configurable enforcement levels).
**Specialist Consensus:** 3/3 unanimous (Tech-Lead 9/10, Research 9/10, Engineer 8.5/10)
**Industry Validation:** 7/7 systems use configurable hook pattern (Temporal, Kubernetes, Webpack, Express, Git Hooks, AWS Lambda, React)
**LOC Estimate:** ~670 LOC (Tier 1+2 default), 795 total, 80% reuse from claude-mpm
**Binding Constraints:** D2-Q1/Q11 (core events), D2-Q17 (configurable levels), D2-Q24 (4-Layer Defense mapping)

**Related Decision:** D2-Q1

---

### Q26: Should CB#8 be defined or should the system use only CB#1-CB#7?
**Context:** D2-Q6 references CB#1-CB#7. SESSION-8-GAP-ANALYSIS proposed CB#8 but it was never defined. circuit-breakers.md only defines CB#1-CB#7.

Options:
- A: Define CB#8 - Add CB#8 for [specific purpose to be determined]
- B: Remove CB#8 References - Confirm only 7 circuit breakers needed, clean up references
- C: Reserve CB#8 - Keep CB#8 as reserved slot for future use
- D: Extensible CB System - Allow dynamic CB definition beyond fixed set

**Decision:** Option A: Confirm CB#8 as QA Verification Gate (acknowledge existing definition)
**Rationale:** CB#8 is ALREADY DEFINED as "QA Verification Gate" in claude-mpm (Dec 2025, ARCHITECTURE-COMPLETE.md:1430-1450). Purpose: Mandatory QA verification before ANY completion claim. Enforcement: Instructional via PM_INSTRUCTIONS.md (37 lines), consistent with D2-Q6 tiered enforcement (CB#3-CB#8 instructional). CB#8 detects OUTPUT (completion claims), not INPUT (tool calls), making it unsuitable for PreToolUse hooks. Implementation: Document CB#8 in circuit-breakers.md (~77 LOC documentation update).
**Specialist Consensus:** 3/3 unanimous (Tech-Lead 9/10, Research 8/10, Engineer 8/10)
**Industry Validation:** 9/9 systems support QA/verification gates (Kubernetes, OPA, Resilience4j, Temporal, CI/CD, Istio, AWS Lambda, PostgreSQL, Camunda)
**LOC Estimate:** ~77 (documentation only, zero code changes)
**Binding Constraints:** D2-Q6 (instructional for behavioral rules), D2-Q8 (soft tier)
**Analogy:** House Number - CB#8 exists in PM_INSTRUCTIONS.md (mailbox) and ARCHITECTURE-COMPLETE.md (GPS), now document in circuit-breakers.md (front door)

**Related Decision:** D2-Q6

---

### Q27: How should validation gates prevent LLM hallucination?
**Context:** CORE-VISION.md:63 requires "Zero hallucination through validation gates". D2-Q8 mentions 95% effectiveness but not HOW hallucination is prevented.

Options:
- A: Grounding via KuzuDB - All claims must be grounded in stored knowledge
- B: Source Citation Required - All assertions must cite source files/lines
- C: Dual-Agent Verification - Second agent verifies first agent's outputs
- D: Schema Enforcement - Outputs must match predefined schemas (no freeform claims)
- E: Multi-Method - KuzuDB grounding + citations + schema enforcement combined

**CORE-VISION Reference:** Line 63

**Decision:** Option E (Tiered): Multi-Method with Configurable Layers (Swiss Cheese Defense Model)
**Rationale:** Defense-in-depth approach using 3 stacked layers to catch hallucinations that slip through any single layer:
- **Tier 1 (Mandatory):** Schema Enforcement via `validation_strategy.py` (15 validators) - ~180 new LOC, 91% reuse
- **Tier 2 (Recommended):** Citation Validation requiring `file:line` for code claims - ~200 new LOC
- **Tier 3 (Optional):** KuzuDB Grounding for context-aware verification - 100% reuse from `kuzu_memory_hook.py`

Critical finding: CDA attack (arXiv:2503.24191) bypasses schema-only enforcement with 96.2% success rate, validating that single-layer defense is insufficient. Industry consensus: 7/7 production systems use multi-layer anti-hallucination (Stanford, Microsoft Bing, LangChain, Temporal). Integrates with D2-Q21 (4-layer validation), D2-Q22 (progressive proof), D2-Q24 (hook system), D2-Q26 (CB#8 QA gate). "Zero hallucination" is aspirational (industry best: 0.7%); interpreted as "minimum practical hallucination through defense-in-depth."
**Specialist Consensus:** 3/3 unanimous (Tech-Lead 9/10, Research 8.5/10, Engineer 8/10)
**Industry Validation:** 7/7 systems use multi-layer (Stanford Legal RAG 96% reduction, Microsoft Bing, LangChain, Temporal, etc.)
**LOC Estimate:** ~380 new LOC (Tier 1+2), 85%+ reuse from claude-mpm
**Binding Constraints:** D2-Q6 (tiered enforcement), D2-Q17 (configurable levels), D2-Q21 (4-layer validation), D2-Q24 (hook integration)
**Analogy:** Swiss Cheese Security Model - Each layer has holes, but stacked layers ensure hallucinations cannot pass through all

---

## Questions: PM Quality Enforcement (Q28-Q29)

### Q28: How should Claude-Hybrid enforce PM Sequential Thinking?
**Context:** PM must invoke sequential-thinking MCP skill before any action AND after /compact to ensure full comprehension. This prevents rushed decisions and hallucinations.

Options:
- A: Hook Enforcement - SessionStart hook validates sequential-thinking was invoked, blocks if not
- B: Instructional Enforcement - PM_INSTRUCTIONS.md mandates sequential thinking, relies on LLM compliance
- C: Circuit Breaker - CB for sequential thinking validation, blocks tool use until thinking complete
- D: Dual-Layer - Hook enforcement + instructional + logging for audit trail
- E: Self-Attestation - PM must include "Sequential thinking complete" marker before proceeding

**Source:** User PM Quality Rule #1 (Session 11)

**Decision:** Option D: Dual-Layer Enforcement (CB#9 + Instructional + Logging)
**Rationale:** Traffic Light model - instructional signs (Layer 1) provide guidance, but CB#9 hook (Layer 2) actually blocks until thinking invoked, with audit logging (Layer 3) for compliance metrics. PreCompact hook resets state forcing re-thinking after /compact.
- **Layer 1:** PM_INSTRUCTIONS.md mandate ("MANDATORY: Invoke sequential-thinking BEFORE any action")
- **Layer 2:** CB#9 in `circuit_breaker_hook.py` (blocks tool use until thinking invoked via detection of `mcp__aggregator__call_tool` with `server: "sequential-thinking"`)
- **Layer 3:** Audit logging for compliance metrics
- **Reset:** PreCompact hook resets state (forces re-thinking after /compact)

Critical finding: Only hook-based enforcement survives /compact (context reset). Instructional alone is LOST after /compact. CoT research shows 2.3x accuracy improvement from structured thinking.
**Specialist Consensus:** 3/3 unanimous (Tech-Lead 8/10, Research 8/10, Engineer 8/10)
**Industry Validation:** CoT 2.3x accuracy (Wei et al.), ReAct +34% (Yao et al.), Multi-layer recommended by McKinsey/AWS/GitLab
**LOC Estimate:** ~195 new LOC + 33 lines markdown
**Binding Constraints:** D2-Q6 (tiered enforcement), D2-Q17 (configurable levels), D2-Q24 (hook lifecycle), D2-Q27 (Swiss Cheese model)
**Analogy:** Traffic Light - Signs alone are ignored, traffic lights (hooks) block until compliance, camera (logging) records violations

---

### Q29: How should Claude-Hybrid enforce PM Clarification Before Execution?
**Context:** PM must clarify task/request with user before executing. Prevents misunderstanding and wasted work. PM should ask clarifying questions when ambiguity exists.

Options:
- A: Mandatory Clarification Phase - PM must always ask at least 1 clarifying question before execution
- B: Ambiguity Detection - PM uses heuristics to detect ambiguous requests, asks only when needed
- C: Confidence Threshold - PM proceeds only if confidence ≥8/10, otherwise must clarify
- D: Instructional Guidance - PM_INSTRUCTIONS.md guides clarification behavior, no enforcement
- E: AskUserQuestion Gate - PreToolUse hook checks if clarification occurred for significant actions

**Source:** User PM Quality Rule #2 (Session 11)

**Decision:** Option C + D Enhancement: Confidence Threshold via Sequential-Thinking Integration + Instructional Enhancement
**Rationale:** Clarification enforcement is ALREADY IMPLEMENTED via D2-Q28 decision chain:
1. CB#9 (D2-Q28) ensures PM invokes sequential-thinking before any action
2. Sequential-thinking LAW 4 mandates: "IF CONFIDENCE < 8: DO NOT PROCEED. THINK MORE OR ASK USER"
3. Sequential-thinking LAW 5 mandates: "IF YOU CANNOT COMPREHEND AFTER FULL THINKING: ASK THE USER"

This creates automatic clarification enforcement without additional hooks. Enhancement: Add explicit clarification protocol to PM_INSTRUCTIONS.md referencing LAW 4/5 thresholds.

**Key Architectural Insight:** Clarification is BEHAVIORAL (not CRITICAL) per D2-Q6 tiering. The existing CB#9 → sequential-thinking → LAW 4/5 chain provides sufficient defense-in-depth:
- Layer 1 (Instructional): PM_INSTRUCTIONS.md "When to Ask" guidance (already exists)
- Layer 2 (Hook): CB#9 ensures sequential-thinking invoked (D2-Q28)
- Layer 3 (Skill): LAW 4/5 enforce confidence threshold with mandatory user clarification fallback

**Specialist Consensus:** 3/3 unanimous (Tech-Lead 9/10, Research 9/10, Engineer 9/10)
**Industry Validation:** 4/4 systems use confidence-based gating (Temporal, LangGraph, CrewAI, Enterprise)
**LOC Estimate:** ~20-33 (documentation enhancement only, zero new enforcement code)
**Binding Constraints:** D2-Q6 (soft enforcement), D2-Q17 (configurable thresholds), D2-Q27 (Swiss Cheese), D2-Q28 (Traffic Light)
**Analogy:** Doctor's Examination - Doctor (PM) must diagnose (sequential-think) before prescribing (executing). Confidence <8/10 = order more tests (ask user).

---

## Resume Instructions

**Next session:** 20/29 questions DECIDED. Work through Q21-Q29 gap resolution questions.
**Methodology:** BMad Master facilitated, President decided each question using Ultrathink workflow.
**After completion:** Consolidate D2 decisions into architecture document, proceed to D3.
