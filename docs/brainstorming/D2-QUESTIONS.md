# D2: Enforcement Mechanism - Question Set

**Decision:** How does Claude-Hybrid enforce rules?
**Status:** PENDING
**Generated:** 2025-12-07 (Session 5)
**Sources:** 4 documents analyzed by subagents

---

## Checkpoint Status

| Question | Status | Answer |
|----------|--------|--------|
| Q1 | **DECIDED** | **Option E: Hybrid-Optimized (SessionStart + PreToolUse + Stop)** |
| Q2 | **DECIDED** | **Option C: Orchestrator Semantic Grouping (P10/P20/P50/P80/P90 internal)** |
| Q3 | **DECIDED** | **Option B: Block/Allow/Modify Schema (decision + reason + updatedInput + systemMessage)** |
| Q4 | **DECIDED** | **Option C: Hybrid Approach (CC for blocking, MPM for complex rules)** |
| Q5 | **DECIDED** | **Option C+D: Circuit-Breaker with Graceful Degradation** |
| Q6 | **DECIDED** | **Option D: Hook-enforced for critical (CB#1,2,6) + State-tracked (CB#4) + Instructions (CB#3,5,7) + Monitoring** |
| Q7 | **DECIDED** | **Option F: Extended D2-Q3 Schema + Translator Compliance (add 'ask', use D2-Q4 translator layer)** |
| Q8 | **DECIDED** | **Option D+C: Two-Tier System with Monitoring (Hard/Soft classification + violation persistence for measurability)** |
| Q9 | **DECIDED** | **Option D+B: Separate + Logging + Selective Hooks Influence (A foundation, D observability ~100 LOC, B opt-in ~200 LOC)** |
| Q10 | **DECIDED** | **Option B: Unified Exception Hierarchy (single source of truth, 95% testable, universal industry pattern)** |
| Q11 | **DECIDED** | **Option E (Synthesized): SessionStart + PreToolUse + Stop for enforcement (confirms D2-Q1, industry-validated pattern)** |
| Q12 | **DECIDED** | **Option D: Combined Approach (reason for hard blocks, additionalContext for soft warnings)** |
| Q13 | **DECIDED** | **Option D: Layered (broad baseline `*` + specific exceptions `Edit|Write|MultiEdit`, `Grep|Glob`)** |
| Q14 | **DECIDED** | **Option D: Scripts Delegate to Orchestrator (thin proxy → Python RuleEngine, 89% LOC reduction, industry-validated)** |
| Q15 | **DECIDED** | **Option E (Modified): 4-Phase Lifecycle (SessionStart init + PreToolUse enforce + PreCompact persist + Stop complete), 9/9 industry systems validated, 95% testable** |
| Q16 | **DECIDED** | **Option D: Hybrid Enforcement (mandates for LLM compliance + hooks for critical sequences), 6/6 industry systems validated, ~320 LOC** |
| Q17 | **DECIDED** | **Option D: Configurable Enforcement Levels (per-checkpoint config, tiered HARD/SOFT, ~300 LOC, 6/6 industry systems)** |
| Q18 | **DECIDED** | **Option D: Dual-Layer Enforcement (Schema at load + Hook at invocation, ~300 LOC, 6/6 industry systems)** |
| Q19 | PENDING | - |
| Q20 | PENDING | - |

---

## Questions from Claude-MPM 06-MEMORY-HOOKS.md

### Q1: Which hook events should be used for enforcement in Claude-Hybrid?
Options:
- A: PreToolUse only (the only event that can block actions)
- B: PreToolUse + UserPromptSubmit (both can block and modify)
- C: Full hook event coverage (use all 8 events: blocking where possible, logging/monitoring for non-blocking events)
- D: Selective enforcement (PreToolUse for critical rules, PostToolUse for audit/compliance tracking)

### Q2: How should hook priority be structured for enforcement rules?
Options:
- A: Early priority (P10) for enforcement hooks to block before any other processing occurs
- B: Mid-range priority (P20-P50) to allow initialization hooks to run first but enforce before business logic
- C: Tiered priority system (critical enforcement at P10, standard rules at P40-60, audit at P80+)
- D: Match existing MPM pattern (P20 for pre-processing, P80-89 for post-processing validation)

### Q3: What response schema should enforcement hooks return?
Options:
- A: Binary block/continue only (simple enforcement with message for blocked actions)
- B: Block/continue with tool_input modification (allow enforcement hooks to sanitize/modify inputs)
- C: Extended schema with severity levels (block, warn-and-continue, log-only, continue)
- D: Follow existing MPM schema exactly (action + optional message + optional tool_input modification)

### Q4: How should enforcement integrate with the two parallel hook systems?
Options:
- A: Claude Code External only (use native ~/.claude/settings.json hooks for enforcement)
- B: MPM Internal only (Python BaseHook classes for enforcement logic)
- C: Hybrid approach (Claude Code External for critical blocking, MPM Internal for complex rule evaluation)
- D: Unified system (consolidate into single enforcement layer that abstracts both systems)

### Q5: How should enforcement handle edge cases and failure modes?
Options:
- A: Fail-closed (any enforcement hook error results in blocking the action)
- B: Fail-open with logging (enforcement errors allow action but log for audit)
- C: Circuit-breaker pattern (follow CB#1/CB#2 pattern with PreToolUse enforcement)
- D: Graceful degradation (primary enforcement with fallback to instructional rules if hooks fail)

---

## Questions from Claude-MPM 09-ERROR-HANDLING.md

### Q6: Should Claude-Hybrid enforce circuit breakers via hooks or instructions?
Options:
- A: Hook-enforced for all 7 circuit breakers (guarantees blocking, no LLM compliance dependency)
- B: Hybrid like Claude-MPM: Hook-enforced for CB#1 (implementation) and CB#2 (investigation), instructional for CB#3-CB#7
- C: Instructional only (simpler, relies on LLM compliance, easier to modify rules)
- D: Hook-enforced for critical violations only, with fallback to instructional for edge cases

### Q7: What should the hook blocking mechanism return when a violation is detected?
Options:
- A: Return `{"action": "block", "message": "..."}` immediately (prevents tool execution)
- B: Return `{"action": "warn", "message": "..."}` to allow continuation with logged warning
- C: Hybrid approach: Block for critical rules, warn for non-critical rules
- D: Return `{"action": "escalate"}` to trigger human intervention before proceeding

### Q8: How should Claude-Hybrid handle the effectiveness gap between hook-enforced (95%) and instructional (unknown) circuit breakers?
Options:
- A: Accept the gap - instructional rules are sufficient for less critical violations
- B: Migrate all instructional circuit breakers to hook-enforced (full programmatic enforcement)
- C: Add monitoring/logging for instructional violations to measure effectiveness and iterate
- D: Implement a two-tier system: hard blocks (hooks) for workflow violations, soft blocks (instructions) for style/convention rules

### Q9: How should error recovery strategies integrate with enforcement mechanisms?
Options:
- A: Error strategies (IGNORE, RETRY, ESCALATE, etc.) are caller-determined only, independent of enforcement hooks
- B: Enforcement hooks should influence error strategy selection (e.g., blocked actions trigger ESCALATE)
- C: Create a unified enforcement-error framework where hooks and error handling share decision logic
- D: Keep them separate but add hook-triggered error logging for blocked actions

### Q10: Should Claude-Hybrid address the duplicate exception class problem as part of enforcement design?
Options:
- A: No - treat exception hierarchy as separate from enforcement mechanism design
- B: Yes - create unified exception hierarchy to enable consistent enforcement responses
- C: Use namespace prefixes to enable targeted enforcement
- D: Define enforcement-specific exceptions that wrap underlying errors

---

## Questions from Claude Code 06-HOOK-SYSTEM.md

### Q11: Which hook events should Claude-Hybrid use for enforcement?
Options:
- A: Only use blocking hooks (PreToolUse, UserPromptSubmit) for hard enforcement since they can actually prevent actions
- B: Use all 8 hooks for different enforcement layers - blocking hooks for hard rules, non-blocking hooks for soft guidance via context injection
- C: Rely primarily on non-blocking hooks with context injection (systemMessage) since they can inject workflow reminders without blocking
- D: Focus on PreToolUse for tool-level enforcement and SessionStart for workflow initialization/reminders

### Q12: How should rule violations be communicated back to Claude?
Options:
- A: Use JSON block response with "reason" field - provides structured explanation that appears in Claude's context
- B: Use plain text stdout injection - simpler implementation, text gets injected into context directly
- C: Use systemMessage JSON response - allows adding context without blocking, suitable for warnings
- D: Combine approaches: block with reason for hard violations, systemMessage for soft warnings/guidance

### Q13: How granular should enforcement be at the tool level?
Options:
- A: Use broad matchers ("*" or "Tool:Bash") for general policy enforcement across all tools
- B: Use specific tool matchers ("Tool:Read", "Tool:Write", "Tool:Bash") with different enforcement rules per tool
- C: Use pattern-based matchers (file patterns, command patterns) for fine-grained enforcement based on context
- D: Layer matchers - broad policies for baseline rules, specific matchers for exceptions and overrides

### Q14: Should enforcement rely on external scripts or be built into the orchestrator?
Options:
- A: External scripts only - hooks execute shell commands allowing flexible, customizable enforcement logic
- B: Orchestrator-embedded enforcement - the orchestrator agent applies rules directly without external hook scripts
- C: Hybrid approach - orchestrator enforces core rules instructionally, hooks provide additional enforcement layer for critical operations
- D: Hook scripts that call the orchestrator - scripts delegate decisions back to an enforcement agent for consistent rule interpretation

### Q15: What enforcement pattern should be used for multi-step workflows?
Options:
- A: SessionStart injects full workflow requirements as context, relying on LLM compliance throughout
- B: PreToolUse validates each step against workflow state, blocking out-of-sequence operations
- C: SubagentStop hook enforces workflow completion requirements before allowing subagent results to propagate
- D: Combine SessionStart (workflow initialization) + PreToolUse (step validation) + PreCompact (state preservation) for complete workflow enforcement

---

## Questions from BMAD 02-ARCHITECTURE-CORE.md

### Q16: How should Claude-Hybrid enforce workflow step ordering?
Options:
- A: Mandate-based enforcement - Embed critical mandates in XML/YAML that the LLM reads and self-enforces
- B: Structural enforcement - Use numbered steps with explicit ordering rules that the orchestrator validates
- C: Hook-enforced sequencing - Implement pre/post hooks that programmatically block out-of-order execution attempts
- D: Hybrid enforcement - Mandate declarations for LLM compliance + optional hooks for critical sequences

### Q17: What enforcement model should govern user interaction checkpoints?
Options:
- A: Instructional enforcement - Rely on LLM following rules like "NEVER proceed until user indicates"
- B: Mode-conditional bypass - Allow enforcement to be overridden by mode flags (Normal mode: full interaction; YOLO mode: skip confirmations)
- C: Hook-enforced pauses - Programmatically block workflow continuation until explicit user acknowledgment is received
- D: Configurable enforcement levels - Let users/projects define which checkpoints are hook-enforced vs. instructional

### Q18: How should menu handler routing be enforced?
Options:
- A: Instructional routing - Define handler types in config and trust the orchestrator LLM to route correctly
- B: Hook-enforced routing - Implement programmatic handler resolution that validates trigger-to-handler mapping before execution
- C: Schema-validated routing - Use YAML/XML schema validation to ensure handler definitions are valid, but rely on LLM for runtime routing
- D: Dual-layer enforcement - Schema validation at load time + hook validation at invocation time

### Q19: Should critical_actions (agent activation rules) be hook-enforced or instructional?
Options:
- A: Pure instructional - List critical_actions in agent YAML and trust the LLM to execute them on activation
- B: Hook-enforced activation - Programmatically execute critical_actions before agent persona becomes available, guaranteeing execution
- C: Validated instructional - LLM executes critical_actions, but a hook validates that required state exists before proceeding
- D: Tiered criticality - Some actions are hook-enforced (config loading), others are instructional (communication style)

### Q20: How should variable resolution cascade be enforced?
Options:
- A: Instructional cascade - Document the resolution order and trust LLM to follow it
- B: Programmatic resolver - Hook-based variable resolution that guarantees cascade order and validates all references before workflow execution
- C: Hybrid resolution - System/Path variables resolved by hooks (deterministic), Config/User variables resolved by LLM with fallback prompts
- D: Validation-only enforcement - LLM resolves variables, but a post-resolution hook validates all required variables are populated before proceeding

---

## Resume Instructions

**Next session:** Read this file, continue from first PENDING question.
**Methodology:** BMad Master facilitates, President decides each question.
**After completion:** Update ARCHITECTURAL-DECISIONS.md with D2 decision.
