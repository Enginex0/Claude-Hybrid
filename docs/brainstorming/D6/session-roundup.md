# D6 Session Roundup

**Decision Area:** Process Boundaries & Initialization
**Status:** ✅ COMPLETE
**Questions:** 18/18 complete (100%)
**Created:** 2025-12-10
**Last Updated:** 2025-12-11

---

## Session 80: 2025-12-11 - Q17 & Q18 DECIDED (D6 COMPLETE! 🎉)

### What We Accomplished

1. **Sequential Thinking Memory Refresh** (20 thoughts) - Full context restoration from session files

2. **D6-Q17 DECIDED: Option A - No dashboard (rely on D6-Q15 basic monitoring)**
   - **5-STEP PATTERN EXECUTED:**
     - Step 1: Parallel Explore deep-dive (claude-mpm dashboard analysis: 8,317 LOC in services/socketio/)
     - Step 2: Report findings (Dashboard fully implemented but contradicts rewrite philosophy)
     - Step 3: Ultrathink synthesis (4 specialists: SPLIT - 2/4 C, 1/4 D, 1/4 B)
     - Step 4: BMad Master recommendation with Movie Theater Lobby analogy
     - Step 5: President approved

   - **Key Finding:** D6-Q15 already provides basic monitoring. Claude-Hybrid is a REWRITE not a merge - importing 8,317 LOC dashboard contradicts CORE-VISION.md "NOT a merge" philosophy.
   - **Specialist Split:** Architect 9/10 C, Coder 9/10 C, Research 8/10 D, Tester 8/10 B
   - **BMad Master Resolution:** Rewrite philosophy takes precedence; dashboard is optional feature with marginal value beyond D6-Q15
   - **Future Enhancement Path:** Option D (OpenTelemetry external integration) if users request
   - **Implementation:** 0 new LOC, $0 TCO

3. **D6-Q18 DECIDED: Option C - Separate execution paths (Slash=EMBODIES/menus/state, Task=DELEGATES/stateless)**
   - **5-STEP PATTERN EXECUTED:**
     - Step 1: Parallel Explore deep-dive (BMAD dual invocation patterns, SDK analysis)
     - Step 2: Report findings (Claude Code SDK does NOT expose invocation method)
     - Step 3: Ultrathink synthesis (4 specialists: 3/4 Option C, 1/4 Option B)
     - Step 4: BMad Master recommendation with Relay Race vs Solo Run analogy
     - Step 5: President approved

   - **Key Finding:** Claude Code SDK does NOT expose invocation method - Option B technically impossible. BMAD already uses TWO distinct patterns across 56 agents.
   - **Constraint Violations:** A=5, B=2, **C=0**, D=3 → Option C is cleanest
   - **Specialist Consensus:** 3/4 Option C (Architect 9/10, Coder 8/10, Tester 8/10), Research favored B (8/10)
   - **Split Resolution:** SDK limitation makes Option B impossible; C formalizes existing pattern
   - **Implementation:** 50-100 new LOC (formalize existing patterns), $1,125-2,250 3-year TCO

4. **D6 COMPLETE!** All 18 process boundaries and initialization questions decided.
   - NO DEVIATIONS THIS SESSION - Pattern compliance maintained
   - Parallel Explore agents for Q17 and Q18 for efficiency
   - Ultrathink deployed via /ultrathink:ultrathink slash command
   - TWO QUESTIONS processed simultaneously as requested by President

---

## Session 79: 2025-12-11 - Q15 & Q16 DECIDED (Subprocess vs Exec Mode COMPLETE)

### What We Accomplished

1. **Sequential Thinking Memory Refresh** (20 thoughts) - Full context restoration from session files

2. **D6-Q15 DECIDED: Option A - Basic monitoring (health, exit code, logs)**
   - **5-STEP PATTERN EXECUTED:**
     - Step 1: Parallel Explore deep-dive (subprocess_launcher_service.py analysis)
     - Step 2: Report findings (~151 LOC monitoring: process.poll(), exit code, WebSocket status)
     - Step 3: Ultrathink synthesis (4 specialists: 4/4 UNANIMOUS)
     - Step 4: BMad Master recommendation with Thermostat Analogy
     - Step 5: President approved

   - **Key Finding:** Claude-MPM subprocess mode implements basic monitoring ONLY. Line 195 explicitly delegates response logging to Claude Code's hook system - subprocess is intentionally BLIND to Claude's internal state.
   - **Options DISQUALIFIED:** B (dashboard dependency on Q17), C (VIOLATES D6-Q14 - runtime detection, CI/CD incompatible), D (overkill for debugging)
   - **Specialist Consensus:** 4/4 UNANIMOUS (Architect 9/10, Research High, Coder High, Tester 9/10)
   - **Industry Validation:** Debug monitoring should NOT include watchdog (conflicts with debugger pauses), auto-restart (masks bugs)
   - **Implementation:** 0 new LOC (100% reuse from claude-mpm), $0 TCO

3. **D6-Q16 DECIDED: Option A+C Hybrid - Exit with code + Graceful cleanup**
   - **5-STEP PATTERN EXECUTED:**
     - Step 1: Parallel Explore deep-dive (finally block termination handling analysis)
     - Step 2: Report findings (cleanup sequence: terminal → PTY → SIGTERM → 2s → SIGKILL → WebSocket)
     - Step 3: Ultrathink synthesis (4 specialists: 4/4 UNANIMOUS)
     - Step 4: BMad Master recommendation with Hotel Checkout Analogy
     - Step 5: President approved

   - **Key Finding:** Claude-MPM implements A+C hybrid: exit code logged/propagated (Option A), then exhaustive cleanup (Option C). Option B (restart) would MASK BUGS during debugging - explicitly rejected by research.
   - **Options DISQUALIFIED:** B (VIOLATES D6-Q1 - masks bugs), D (VIOLATES D6-Q14 - requires TTY, CI/CD incompatible)
   - **Specialist Consensus:** 4/4 UNANIMOUS (Architect 9/10, Research High, Coder High, Tester 9/10)
   - **Industry Validation:** SIGTERM → 10s grace → SIGKILL is universal standard (systemd, Docker, K8s, supervisord)
   - **Implementation:** 0 new LOC (100% reuse from claude-mpm), $0 TCO

4. **Subprocess vs Exec Mode Decision Group COMPLETE (Q14-Q16)** - Fifth question group finished!
   - NO DEVIATIONS THIS SESSION - Pattern compliance maintained
   - Parallel Explore agents for Q15 and Q16 for efficiency
   - Ultrathink via /ultrathink:ultrathink slash command (4 specialists)
   - TWO QUESTIONS processed simultaneously as requested by President
   - Both decisions: 0 LOC, $0 TCO - existing implementation is optimal

---

## Session 78: 2025-12-11 - Q13 & Q14 DECIDED (Init Lifecycle COMPLETE + Subprocess Mode 1/3)

### What We Accomplished

1. **Sequential Thinking Memory Refresh** (20 thoughts) - Full context restoration from session files

2. **D6-Q13 DECIDED: HYBRID (Option A + D) - Fail-fast + Checkpoint model**
   - **5-STEP PATTERN EXECUTED:**
     - Step 1: Parallel Explore deep-dive (cli/__init__.py:51-127 failure handling analysis)
     - Step 2: Report findings (Three-tier pattern: unconditional fail-fast, sub-phase non-blocking, implicit checkpoints)
     - Step 3: Ultrathink synthesis (4 specialists: 4/4 UNANIMOUS)
     - Step 4: BMad Master recommendation with Airport Security analogy
     - Step 5: President approved

   - **Key Finding:** Claude-MPM implements three-tier failure handling: (1) Unconditional phases 1-4,6-8,12 fail-fast, (2) Background sub-phases non-blocking per Q11, (3) Phase boundaries serve as implicit checkpoints
   - **Option DISQUALIFIED:** C (Rollback) - ZERO industry adoption; B alone - 4096 combinatorial states
   - **Specialist Consensus:** 4/4 UNANIMOUS (Architect 9/10, Research 9/10, Coder 8/10, Tester 9/10)
   - **Industry Validation:** systemd, Docker, Kubernetes ALL use fail-fast + checkpoint patterns
   - **Implementation:** 85 impl + 215 test = 300 LOC, 80% reuse, $3,420 3-year TCO

3. **D6-Q14 DECIDED: Option A - Explicit config only (Claude-MPM pattern)**
   - **5-STEP PATTERN EXECUTED:**
     - Step 1: Parallel Explore deep-dive (interactive_session.py:202 mode selection analysis)
     - Step 2: Report findings (Pure explicit config, STRONGLY CONSTRAINED by Q1, not strictly pre-selected)
     - Step 3: Ultrathink synthesis (4 specialists: 4/4 UNANIMOUS)
     - Step 4: BMad Master recommendation with Light Switch analogy
     - Step 5: President approved

   - **Key Finding:** Q14 is STRONGLY CONSTRAINED by D6-Q1's "Configurable mode" decision - Option A is the natural implementation
   - **Options DISQUALIFIED:** B (12-Factor antipattern), C (undefined conflict), D (complex decision tree)
   - **Specialist Consensus:** 4/4 UNANIMOUS (Architect 8/10, Research 10/10, Coder 9/10, Tester 9/10)
   - **Industry Validation:** 12-Factor App explicitly labels environment-based auto-detection an antipattern
   - **Implementation:** 30 impl + 65 test = 95 LOC, 95% reuse, $1,128 3-year TCO

4. **12-Phase Initialization Lifecycle Group COMPLETE (Q10-Q13)** - Fourth question group finished!
   - **Subprocess vs Exec Mode Group Started** - Q14 decided, Q15-Q16 remaining
   - NO DEVIATIONS THIS SESSION - Pattern compliance maintained
   - Parallel Explore agents for Q13 and Q14 for efficiency
   - Ultrathink via /ultrathink:ultrathink slash command (4 specialists)
   - TWO QUESTIONS processed simultaneously as requested by President

---

## Session 77: 2025-12-11 - Q11 & Q12 DECIDED (Init Lifecycle 3/4)

### What We Accomplished

1. **Sequential Thinking Memory Refresh** (20 thoughts) - Full context restoration from session files

2. **D6-Q11 DECIDED: Option A - Synchronous non-blocking (Claude-MPM pattern)**
   - **5-STEP PATTERN EXECUTED:**
     - Step 1: Parallel Explore deep-dive (cli/startup.py:632-650 analysis)
     - Step 2: Report findings (9 sub-phases sequential, 27 try-except blocks, daemon thread leak detected)
     - Step 3: Ultrathink synthesis (4 specialists: 4/4 favor A-based approach)
     - Step 4: BMad Master recommendation with Assembly Line analogy
     - Step 5: President approved

   - **Key Finding:** cli/startup.py runs 9 sub-phases synchronously with try-except per phase. Daemon thread leak at lines 1034-1037 and 874-875 must be fixed.
   - **Option DISQUALIFIED:** D - VIOLATES D6-Q2 (state death) and D5-Q8 (session boundary loading)
   - **Specialist Consensus:** 4/4 favor A (Architect 9/10, Research 9/10, Coder 9/10, Tester 9/10)
   - **Industry Validation:** kubeadm, npm, setuptools all use sequential with graceful degradation
   - **Implementation:** 18-22 new LOC (thread fix), ~100% reuse, $495 3-year TCO

3. **D6-Q12 DECIDED: Option A - Match Claude-MPM pattern (PRE-SELECTED by D6-Q10)**
   - **5-STEP PATTERN EXECUTED:**
     - Step 1: Parallel Explore deep-dive (phase trigger conditions at cli/__init__.py)
     - Step 2: Report findings (D6-Q10 explicitly states "8 unconditional, 4 conditional")
     - Step 3: Ultrathink synthesis (4 specialists: 4/4 UNANIMOUS)
     - Step 4: BMad Master confirmation - binding constraint satisfaction (Relay Race analogy)
     - Step 5: President approved

   - **Key Finding:** D6-Q10 PRE-SELECTS Option A - decision explicitly states "8 unconditional, 4 conditional"
   - **Phase Classification:** Unconditional (1-4, 6-8, 12), Conditional (5, 9, 10, 11)
   - **Specialist Consensus:** 4/4 UNANIMOUS (Architect 9/10, Research 9/10, Coder 10/10, Tester 9/10)
   - **Implementation:** 0 new LOC (100% reuse), $45-90 TCO

4. **Initialization Lifecycle Group 3/4 Complete** - Only Q13 remains!
   - NO DEVIATIONS THIS SESSION - Pattern compliance maintained
   - Parallel Explore agents for Q11 and Q12 for efficiency
   - Ultrathink via /ultrathink:ultrathink slash command (4 specialists)
   - TWO QUESTIONS processed simultaneously as requested by President

---

## Session 76: 2025-12-11 - Q9 & Q10 DECIDED (MCP Gateway Config COMPLETE)

### What We Accomplished

1. **Sequential Thinking Memory Refresh** (20 thoughts) - Full context restoration

2. **D6-Q9 DECIDED: Option C - State requirement (Stateful in Gateway, stateless native)**
   - 3/4 consensus (Architect 9/10, Research 8/10, Tester 9/10), Coder favored A (6/10)
   - Key: Binary decision rule "Does tool need persistent state?" aligns with D6-Q2
   - LOC: ~225 new, $1,665 3-year TCO

3. **D6-Q10 DECIDED: Option A - Full 12-phase model (Claude-MPM pattern)**
   - 4/4 UNANIMOUS (Architect 8/10, Research 8/10, Coder 9/10, Tester 9/10)
   - Key: 12 phases (8 unconditional, 4 conditional), 1513+ tests validate
   - LOC: ~2,600 (85% reuse), $15,810 3-year TCO

4. **MCP Gateway Configuration Group COMPLETE (Q7-Q9)**

---

## Session 75: 2025-12-11 - Q7 & Q8 DECIDED (MCP Gateway Config 2/3)

### What We Accomplished

1. **D6-Q7 DECIDED: Option A - Single config file (~/.claude.json)**
   - 4/4 unanimous - Claude Code ONLY supports ~/.claude.json
   - LOC: 0 additional (100% reuse), $0 TCO

2. **D6-Q8 DECIDED: Option A - External server (Claude-MPM pattern)**
   - 4/4 effective consensus - Gateway spawns AFTER os.execvpe()
   - LOC: 0 additional (100% reuse), $0 TCO

---

## Session 74: 2025-12-11 - Q5 & Q6 DECIDED (File Contracts Group COMPLETE)

### What We Accomplished

1. **Sequential Thinking Memory Refresh** (20 thoughts) - Full context restoration from session files

2. **D6-Q5 DECIDED: Option A - Full deployment (Claude-MPM pattern)**
   - **5-STEP PATTERN EXECUTED:**
     - Step 1: Parallel Explore deep-dive (DOCS_FIRST_THEN_CODE)
     - Step 2: Report findings (6 file targets, 1.49 MB total, 4,234 LOC exists)
     - Step 3: Ultrathink synthesis (4 specialists: 4/4 unanimous)
     - Step 4: BMad Master recommendation with Moving Day analogy
     - Step 5: President approved

   - **Key Finding:** 6 files deployed pre-handoff: ~/.claude.json (89KB), ~/.claude/settings.json (1.9KB), PM_INSTRUCTIONS.md (~152KB), agents/*.md (1.1MB), skills/ (356KB), output-styles/ (<1KB)
   - **Options DISQUALIFIED:** B (violates D5-Q9), C (violates D6-Q2 - no orchestrator survives post-exec)
   - **Specialist Consensus:** 4/4 unanimous (Architect 9/10, Research 9/10, Coder 9/10, Tester 8/10)
   - **Industry Validation:** Docker, Kubernetes, systemd all use full pre-deployment pattern
   - **Implementation:** 50-80 new LOC, 95% reuse from claude-mpm, $3,000-4,500 3-year TCO

3. **D6-Q6 DECIDED: Option A - Multi-section assembly (Claude-MPM pattern)**
   - **5-STEP PATTERN EXECUTED:**
     - Step 1: Parallel Explore deep-dive (ContentFormatter 10-section analysis)
     - Step 2: Report findings (10 sections, SHA-256 cache, 1,200 LOC exists)
     - Step 3: Ultrathink synthesis (4 specialists: 4/4 unanimous)
     - Step 4: BMad Master recommendation with Recipe Assembly analogy
     - Step 5: President approved

   - **Key Finding:** 10-section assembly order: PM_INSTRUCTIONS → Custom → WORKFLOW → MEMORY → PM Memories → Agent Memories → Capabilities (dynamic) → Temporal Context (dynamic) → BASE_PM → Output Style
   - **Option DISQUALIFIED:** D (violates D5-Q13 - hash-based invalidation requires cached content)
   - **Split Resolution:** Research favored C (explicit manifest) but A's InstructionLoader provides implicit manifest
   - **Specialist Consensus:** 4/4 unanimous (Architect 9/10, Research 8/10, Coder 9/10, Tester 9/10)
   - **Implementation:** 30-50 new LOC, 98% reuse from claude-mpm, $1,350-2,250 3-year TCO

4. **Pre/Post-Handoff File Contracts Group COMPLETE (Q5-Q6)** - Second question group finished!
   - NO DEVIATIONS THIS SESSION - Pattern compliance maintained
   - Parallel Explore agents for Q5 and Q6 for efficiency
   - Ultrathink via /ultrathink:ultrathink slash command (4 specialists)
   - TWO QUESTIONS processed simultaneously as requested by President

---

## Session 73: 2025-12-11 - Q3 & Q4 DECIDED (os.execvpe Group COMPLETE)

### What We Accomplished

1. **Sequential Thinking Memory Refresh** (20 thoughts) - Full context restoration from session files

2. **D6-Q3 DECIDED: Option D - Mixed strategy (security via CLI, optional via env, bulky via files)**
   - **5-STEP PATTERN EXECUTED:**
     - Step 1: Parallel Explore deep-dive (DOCS_FIRST_THEN_CODE)
     - Step 2: Report findings (claude-mpm builds cmd with explicit --dangerously-skip-permissions, --system-prompt-file)
     - Step 3: Ultrathink synthesis (4 specialists: 4/4 unanimous)
     - Step 4: BMad Master recommendation with ARG_MAX analysis
     - Step 5: President approved

   - **Key Finding:** 152KB PM_INSTRUCTIONS.md exceeds Linux ARG_MAX (128KB) by 19.1% - file-based is REQUIRED, not optional
   - **Specialist Consensus:** 4/4 unanimous (Architect 9/10, Research 9/10, Coder 9/10, Tester 9/10)
   - **Industry Validation:** systemd, supervisord, Kubernetes all use mixed strategy pattern
   - **Implementation:** 520 LOC, 85-90% reuse from claude-mpm, $4,035 3-year TCO

3. **D6-Q4 DECIDED: Option C - Configurable mode (PRE-SELECTED by D6-Q1)**
   - **5-STEP PATTERN EXECUTED:**
     - Step 1: Parallel Explore deep-dive (verified Q1 pre-selection)
     - Step 2: Report findings (Q1 "Configurable mode (exec default, subprocess for debugging)" = Q4 Option C)
     - Step 3: Ultrathink synthesis (4 specialists: 4/4 unanimous confirm pre-selection)
     - Step 4: BMad Master confirmation - binding constraint satisfaction
     - Step 5: President approved

   - **Key Finding:** D6-Q1's decision text is SEMANTICALLY IDENTICAL to Q4 Option C - this is constraint satisfaction, not new decision
   - **Specialist Consensus:** 4/4 unanimous (Architect 10/10, Research 8/10, Coder 8/10, Tester 10/10)
   - **Implementation:** 415 LOC, 85-90% reuse from claude-mpm, $4,215 3-year TCO

4. **os.execvpe Handoff Mechanism Group COMPLETE (Q1-Q4)** - First question group finished!
   - NO DEVIATIONS THIS SESSION - Pattern compliance maintained
   - Parallel Explore agents for Q3 and Q4 for efficiency
   - Ultrathink via /ultrathink:ultrathink slash command (4 specialists)
   - TWO QUESTIONS processed simultaneously as requested by President

---

## Session 72: 2025-12-11 - D6 STARTED (Q1 & Q2 DECIDED)

### What We Accomplished

1. **Sequential Thinking Memory Refresh** (20 thoughts) - Full context restoration from session files

2. **D6-Q1 DECIDED: Option C - Configurable mode (exec default, subprocess for debugging)**
   - **5-STEP PATTERN EXECUTED:**
     - Step 1: Parallel Explore deep-dive (DOCS_FIRST_THEN_CODE)
     - Step 2: Report findings (claude-mpm interactive_session.py:188 shows config-based mode selection)
     - Step 3: Ultrathink synthesis (4 specialists: 4/4 unanimous)
     - Step 4: BMad Master recommendation with Relay Race analogy
     - Step 5: President approved

   - **Key Finding:** claude-mpm has both modes at interactive_session.py - exec default (line 585), subprocess opt-in (line 588-592)
   - **Specialist Consensus:** 4/4 unanimous (Explore 9.5/10, Coder 9/10, Tester 9/10, Research 9/10, Architect 9/10)
   - **Industry Validation:** Docker, systemd, Kubernetes use exec for single-handoff; Temporal, Prefect use subprocess for worker pools
   - **Implementation:** 40-50 LOC, 65% reuse from claude-mpm, $7,200 3-year TCO

3. **D6-Q2 DECIDED: Option A - Complete state death (files only survive)**
   - **5-STEP PATTERN EXECUTED:**
     - Step 1: Parallel Explore deep-dive (DI container analysis)
     - Step 2: Report findings (3 DI containers die, ~11.4MB files survive)
     - Step 3: Ultrathink synthesis (4 specialists: 4/4 unified)
     - Step 4: BMad Master recommendation with Moving Houses analogy
     - Step 5: President approved

   - **Key Finding:** os.execvpe replaces process memory - this is physics, not a design choice
   - **Specialist Consensus:** 4/4 unified (different terminology, same outcome)
   - **Binding Constraints:** D4-Q9/Q11 (file-based state) pre-selects this
   - **Implementation:** 0 additional LOC (current implementation), $0 TCO

4. **D6 Progress: 2/18** - First two questions of os.execvpe Handoff Mechanism group decided.
   - NO DEVIATIONS THIS SESSION - Pattern compliance maintained
   - Parallel Explore agents for Q1 and Q2 for efficiency
   - Ultrathink via /ultrathink:ultrathink slash command (4 specialists)
   - TWO QUESTIONS processed simultaneously as requested by President

---

## Current Progress

| Question | Status | Answer |
|----------|--------|--------|
| Q1: os.execvpe handoff | **DECIDED** | Option C: Configurable mode (exec default, subprocess for debugging) |
| Q2: Internal state at handoff | **DECIDED** | Option A: Complete state death (files only survive) |
| Q3: CLI construction | **DECIDED** | Option D: Mixed strategy (security via CLI, bulky via files) |
| Q4: Dual mode support | **DECIDED** | Option C: Configurable mode (PRE-SELECTED by Q1) |
| Q5: Pre-handoff files | **DECIDED** | Option A: Full deployment (all 6 targets before handoff) |
| Q6: System prompt assembly | **DECIDED** | Option A: Multi-section assembly (10 sections via ContentFormatter) |
| Q7: MCP config passing | **DECIDED** | Option A: Single config file (~/.claude.json) |
| Q8: MCP Gateway internal/external | **DECIDED** | Option A: External server (Claude-MPM pattern) |
| Q9: MCP tool criteria | **DECIDED** | Option C: State requirement (Stateful in Gateway, stateless native) |
| Q10: 12-phase initialization | **DECIDED** | Option A: Full 12-phase model (Claude-MPM pattern) |
| Q11: 9 background sub-phases | **DECIDED** | Option A: Synchronous non-blocking (Claude-MPM pattern) |
| Q12: Unconditional vs conditional | **DECIDED** | Option A: Match Claude-MPM (PRE-SELECTED by Q10) |
| Q13: Initialization failures | **DECIDED** | HYBRID (A+D): Fail-fast + Checkpoint model |
| Q14: Mode selection criteria | **DECIDED** | Option A: Explicit config only (Claude-MPM pattern) |
| Q15: Subprocess monitoring | **DECIDED** | Option A: Basic monitoring (health, exit code, logs) |
| Q16: Child termination handling | **DECIDED** | Option A+C: Exit with code + Graceful cleanup |
| Q17: Observability dashboard | **DECIDED** | Option A: No dashboard (rely on D6-Q15 basic monitoring) |
| Q18: Slash vs Task invocation | **DECIDED** | Option C: Separate execution paths (Slash=EMBODIES, Task=DELEGATES) |

---

## Question Groups Progress

| Group | Questions | Completed | Status |
|-------|-----------|-----------|--------|
| os.execvpe Handoff Mechanism | Q1-Q4 | 4/4 | **COMPLETE** |
| Pre/Post-Handoff File Contracts | Q5-Q6 | 2/2 | **COMPLETE** |
| MCP Gateway Configuration | Q7-Q9 | 3/3 | **COMPLETE** |
| 12-Phase Initialization Lifecycle | Q10-Q13 | 4/4 | **COMPLETE** |
| Subprocess vs Exec Mode Decision | Q14-Q16 | 3/3 | **COMPLETE** |
| Gap Analysis Additions | Q17-Q18 | 2/2 | **COMPLETE** |

---

## Key Technical Context

### The Handoff Boundary

```
BEFORE os.execvpe():
- Orchestrator process running (PID: X)
- All Python state in memory
- DI containers populated
- Files written to disk

                os.execvpe()
                     |
                     v

AFTER os.execvpe():
- SAME PID: X (process replaced, not forked!)
- All orchestrator state GONE
- Claude Code binary now executing
- Reads files orchestrator wrote to disk
```

### Critical File Locations

| Pre-Handoff (Written) | Post-Handoff (Read) |
|-----------------------|---------------------|
| ~/.claude/settings.json | Hook registration |
| ~/.claude.json | MCP server spawn config |
| .claude-mpm/PM_INSTRUCTIONS.md | System prompt |
| ~/.claude/agents/*.md | Agent discovery |
| ~/.claude/skills/*.md | Skill discovery |

---

## Resume Instructions

1. Read this file for context
2. Read D6-QUESTIONS.md - continue from Q5
3. **MANDATORY PATTERN for every question:**
   - Step 1: Deploy Explore subagent (DOCS_FIRST_THEN_CODE)
   - Step 2: Report findings explicitly
   - Step 3: Trigger /ultrathink:ultrathink for 4-specialist synthesis
   - Step 4: BMad Master recommendation with evidence
   - Step 5: President decides
4. Update state.json after each decision

---

## Binding Constraints from D1-D5

| Constraint | Source | Impact on D6 |
|------------|--------|--------------|
| File-based state persistence | D4-Q9/Q11 | PRE-SELECTS Q2 Option A |
| Session boundary loading | D5-Q8 | Aligns with exec mode |
| Crash handling patterns | D2-Q5 | Process death = clean boundary |
| Hash-based caching | D5-Q12/Q13 | Cache survives as files |
