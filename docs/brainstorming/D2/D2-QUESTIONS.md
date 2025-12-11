# D2: Enforcement Mechanism - Question Set

**Decision:** How should Claude-Hybrid enforce workflow rules and circuit breakers?
**Status:** ✅ COMPLETE (20/20 DECIDED)
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

## Resume Instructions

**Next session:** All 20 questions DECIDED. Update ARCHITECTURAL-DECISIONS.md with D2 enforcement decisions.
**Methodology:** BMad Master facilitated, President decided each question using Ultrathink workflow.
**After completion:** Consolidate D2 decisions into architecture document, proceed to D3.
