# D6: Process Boundaries & Initialization - Question Set

**Decision:** How does Claude-Hybrid handle process boundaries and initialization?
**Status:** ✅ COMPLETE (18/18 DECIDED)
**Generated:** 2025-12-10 (Updated 2025-12-11 - Removed 4 redundant questions)
**Sources:** Claude-MPM analysis documents (01-EXECUTIVE-SUMMARY.md, 02-ARCHITECTURE-CORE.md, 07-MCP-TICKETING.md)

---

## Redundancy Audit Notes

The following questions were REMOVED due to semantic overlap:
- **Original Q7** (cache invalidation) → Already decided in D5-Q13 (Hash-Based SHA-256)
- **Original Q8** (handoff boundary state) → Already decided in D4-Q9/Q11 (state persistence)
- **Original Q11** (first-call MCP latency) → Conflicts with D5-Q8 (session boundary loading)
- **Current Q7** (MCP spawning timing) → Duplicates D7-Q3 (MCP server spawning strategy) - CONSOLIDATED to D7

---

## Checkpoint Status

| Question | Status | Answer |
|----------|--------|--------|
| Q1 | **DECIDED** | Option C: Configurable mode (exec default, subprocess for debugging) |
| Q2 | **DECIDED** | Option A: Complete state death (files only survive) |
| Q3 | **DECIDED** | Option D: Mixed strategy (security via CLI, bulky via files) |
| Q4 | **DECIDED** | Option C: Configurable mode (PRE-SELECTED by Q1) |
| Q5 | **DECIDED** | Option A: Full deployment (all 6 targets before handoff) |
| Q6 | **DECIDED** | Option A: Multi-section assembly (10 sections via ContentFormatter) |
| Q7 | **DECIDED** | Option A: Single config file (~/.claude.json) |
| Q8 | **DECIDED** | Option A: External server (Claude-MPM pattern) |
| Q9 | **DECIDED** | Option C: State requirement (Stateful in Gateway, stateless native) |
| Q10 | **DECIDED** | Option A: Full 12-phase model (Claude-MPM pattern) |
| Q11 | **DECIDED** | Option A: Synchronous non-blocking (Claude-MPM pattern) |
| Q12 | **DECIDED** | Option A: Match Claude-MPM pattern (PRE-SELECTED by Q10) |
| Q13 | **DECIDED** | HYBRID (A+D): Fail-fast + Checkpoint model |
| Q14 | **DECIDED** | Option A: Explicit config only (Claude-MPM pattern) |
| Q15 | **DECIDED** | Option A: Basic monitoring (health, exit code, logs) |
| Q16 | **DECIDED** | Option A+C: Exit with code + Graceful cleanup |
| Q17 | **DECIDED** | Option A: No dashboard (rely on D6-Q15 basic monitoring) |
| Q18 | **DECIDED** | Option C: Separate execution paths (Slash=EMBODIES, Task=DELEGATES) |

---

## Questions: os.execvpe Handoff Mechanism (Q1-Q4)

### Q1: Should Claude-Hybrid use os.execvpe process replacement like Claude-MPM?
**Context:** Claude-MPM uses `os.execvpe()` at `interactive_session.py:585` to completely replace the orchestrator process with Claude Code. The same PID is retained but all orchestrator state is lost.

Options:
- A: Full process replacement (os.execvpe) - Orchestrator sets up environment, writes files, then completely disappears. Claude Code inherits the same PID with clean state.
- B: Parent-child model (subprocess) - Orchestrator remains as parent process, spawns Claude Code as child. Orchestrator can monitor and manage the child.
- C: Shared process model - Orchestrator and Claude Code run in the same process space, sharing memory and state through direct function calls.
- D: Service mesh model - Both run as separate long-lived services communicating via IPC (sockets, pipes, or message queues).

### Q2: What happens to orchestrator internal implementation state at the handoff boundary?
**Context:** In Claude-MPM, `os.execvpe()` causes all Python state, DI containers, and in-memory data to be destroyed. Only filesystem artifacts survive.
**NOTE:** Workflow state persistence is addressed in D4-Q9 and D4-Q11. This question is specifically about orchestrator implementation state (DI containers, Python objects, in-memory caches).

Options:
- A: Complete state death (Claude-MPM pattern) - All in-memory state is lost at handoff. Only files on disk survive. Claude Code starts fresh and reads what it needs from filesystem.
- B: State serialization - Before handoff, orchestrator serializes critical state to a file (JSON/pickle). Post-handoff process reads and reconstructs state.
- C: Shared memory region - Allocate shared memory before fork/exec that both processes can access for state transfer.
- D: State server - Run a separate lightweight service that holds state, both orchestrator and Claude Code can query it.

### Q3: How should the command line be constructed for Claude Code handoff?
**Context:** Claude-MPM builds: `["claude", "--dangerously-skip-permissions", "--system-prompt-file", ".claude-mpm/PM_INSTRUCTIONS.md", "--agents", agents_json]`

Options:
- A: Minimal CLI args (Claude-MPM pattern) - Pass only essential flags: permission mode, system prompt file, and agents JSON. All other config via files.
- B: Comprehensive CLI args - Pass maximum configuration via command line to reduce filesystem dependencies and enable stateless operation.
- C: Environment variables - Use environment variables for configuration instead of CLI args, allowing clean command lines and easy debugging.
- D: Mixed strategy - Critical security flags via CLI (cannot be overridden), optional config via environment, bulky data via files.

### Q4: Should Claude-Hybrid support both exec and subprocess modes?
**Context:** Claude-MPM has both `_launch_exec_mode()` and `_launch_subprocess_mode()` at `interactive_session.py:188`. Subprocess mode allows debugging/monitoring.

Options:
- A: Exec mode only - Always use process replacement for production simplicity. No monitoring capability from orchestrator after handoff.
- B: Subprocess mode only - Always maintain parent-child relationship. Orchestrator can monitor stdout/stderr and manage child lifecycle.
- C: Configurable mode (Claude-MPM pattern) - Support both modes via config (`launch_method: subprocess|exec`). Default to exec for production, subprocess for debugging.
- D: Auto-detection - Automatically choose mode based on environment (exec in production, subprocess in development/CI).

---

## Questions: Pre/Post-Handoff File Contracts (Q5-Q6)

### Q5: What files must be written BEFORE the handoff boundary?
**Context:** Claude-MPM writes these before execvpe: `~/.claude/settings.json` (hooks), `~/.claude.json` (MCP), `.claude-mpm/PM_INSTRUCTIONS.md` (system prompt), `~/.claude/agents/*.md`, `~/.claude/skills/*.md`

Options:
- A: Full deployment (Claude-MPM pattern) - Deploy all assets before handoff: settings, MCP config, system prompt, agents, skills, output styles. Claude Code reads everything from disk.
- B: Minimal deployment - Deploy only system prompt and essential config. Claude Code uses its native defaults for agents/skills/MCP.
- C: Lazy deployment - Deploy only config references before handoff. Claude Code triggers deployment of agents/skills on first use.
- D: Atomic deployment - Create a complete deployment package (tarball/directory) that Claude Code unpacks atomically, ensuring consistency.

### Q6: How should the system prompt file be assembled?
**Context:** Claude-MPM assembles 10 sections totaling ~46KB via `FrameworkLoader -> InstructionLoader -> ContentFormatter -> InstructionCacheService`

Options:
- A: Multi-section assembly (Claude-MPM pattern) - Assemble from multiple sources: core PM rules, custom instructions, workflow, memory, agent memories, capabilities, temporal context, base PM, output style.
- B: Single template with placeholders - Use one master template with {{placeholder}} substitutions. Simpler pipeline, easier to debug.
- C: Modular includes - Write multiple smaller files, use a manifest that tells Claude Code which files to load in which order.
- D: Dynamic generation - Generate system prompt on-the-fly during handoff based on current session state, project config, and user preferences.

---

## Questions: MCP Gateway Configuration (Q7-Q9)

**NOTE:** MCP server spawning timing (on-demand vs pre-warm) is addressed in D7-Q3.

### Q7: How should MCP server configuration be passed across the handoff?
**Context:** Claude-MPM writes MCP config to `~/.claude.json` which Claude Code reads to spawn servers as stdio subprocesses.

Options:
- A: Single config file (Claude-MPM pattern) - Write all MCP server configs to ~/.claude.json. Claude Code's native MCP client handles spawning.
- B: Per-server config files - Write separate config files per MCP server. Allows selective server loading and easier debugging.
- C: Embedded in system prompt - Include MCP server list in the system prompt so Claude knows what tools are available without config files.
- D: Discovery-based - Write minimal config, let Claude Code discover available MCP servers through a registry or directory scan.

### Q8: Should Claude-Hybrid's MCP Gateway be an internal tool or external server?
**Context:** Claude-MPM has 9 implemented internal tools (7 registered) in its MCP Gateway that runs AFTER handoff.

Options:
- A: External server (Claude-MPM pattern) - MCP Gateway is a separate process spawned by Claude Code via stdio protocol, listed in ~/.claude.json.
- B: Internal tools only - No separate gateway process. Implement tools directly in Claude Code's native tool system where possible.
- C: Hybrid model - Core tools (echo, calculator) are internal. Complex tools (document_summarizer, kuzu_memory) are external servers.
- D: Plugin architecture - MCP Gateway is optional. Users can enable/disable gateway features via config, falling back to simpler tools.

### Q9: What criteria determine which tools go in the MCP Gateway vs native?
**Context:** Trade-off between external MCP servers (isolation, language flexibility) and native tools (performance, simpler debugging).

Options:
- A: Complexity threshold - Simple tools (echo, calculator) are native. Complex tools requiring external deps go in MCP Gateway.
- B: Language requirement - Python-only tools in MCP Gateway. Pure JS/TS tools implemented natively in Claude Code.
- C: State requirement - Stateful tools (memory, database) in MCP Gateway. Stateless tools implemented natively.
- D: Performance requirement - Latency-sensitive tools are native. Batch/background tools can be in MCP Gateway.

---

## Questions: 12-Phase Initialization Lifecycle + 9 Background Sub-Phases (Q10-Q13)

### Q10: Should Claude-Hybrid follow Claude-MPM's 12-phase initialization model?
**Context:** Claude-MPM has 12 main phases: early_environment, create_parser, preprocess_args, parse_args, handle_missing_config, setup_configure_env, setup_mcp_logging, ensure_directories, run_background_services, display_banner, ensure_run_attributes, execute_command. 8 are unconditional.

Options:
- A: Full 12-phase model (Claude-MPM pattern) - Replicate all phases for compatibility and proven lifecycle management.
- B: Simplified 6-phase model - Consolidate into: parse_args, validate_config, setup_environment, deploy_assets, setup_hooks, execute_handoff.
- C: Pipeline model - Define phases as composable pipeline stages that can be reordered, skipped, or extended via config.
- D: Event-driven model - Replace fixed phases with an event system where components register for lifecycle events they care about.

### Q11: How should the 9 background sub-phases be handled?
**Context:** Claude-MPM's Phase 9 (`run_background_services`) contains 9 sub-tasks: project registry, MCP auto-config, MCP gateway verify, update check, remote agents sync, remote skills sync, bundled skills deploy, runtime skills discover, output style deploy. These run synchronously but are non-blocking (failures don't crash startup).

Options:
- A: Synchronous non-blocking (Claude-MPM pattern) - Run all 9 sub-phases sequentially but catch errors to prevent startup failure.
- B: True async execution - Run sub-phases concurrently using asyncio/threads. Faster startup but more complex error handling.
- C: Required vs optional separation - Mark some sub-phases as required (fail startup if they fail), others as optional (log and continue).
- D: Lazy initialization - Skip sub-phases during startup, run them on-demand when their functionality is first needed.

### Q12: Which initialization phases should be unconditional vs conditional?
**Context:** Claude-MPM has 8 unconditional phases (1-4, 6-8, 12) and 4 conditional phases (5: handle_missing_config, 9: background_services, 10: banner, 11: ensure_run_attributes).

Options:
- A: Match Claude-MPM pattern - Same 8 unconditional phases for proven reliability. Conditional phases depend on same triggers.
- B: Maximize unconditional - Make more phases unconditional to ensure consistent behavior. Only truly optional features remain conditional.
- C: Config-driven conditionality - All phases are potentially conditional based on explicit config flags. Maximum flexibility.
- D: Environment-driven conditionality - Phases are conditional based on environment (CI skips banner, production skips debug setup).

### Q13: How should initialization failures be handled?
**Context:** Claude-MPM's non-blocking sub-phases can fail without crashing. But what about critical phase failures?

Options:
- A: Fail-fast for critical phases - Any failure in unconditional phases (1-4, 6-8, 12) terminates startup immediately with clear error message.
- B: Graceful degradation - Attempt to continue with reduced functionality when possible. Log failures but only fail if truly unrecoverable.
- C: Rollback model - If a phase fails, attempt to undo previous phases' changes before terminating to leave clean state.
- D: Checkpoint model - After each successful phase, save checkpoint. On failure, report which phase failed and what succeeded.

---

## Questions: Subprocess vs Exec Mode Decision (Q14-Q16)

### Q14: What criteria should determine subprocess vs exec mode selection?
**Context:** Claude-MPM uses config `launch_method` at `interactive_session.py:188`. Subprocess keeps MPM alive as parent; exec replaces MPM entirely.

Options:
- A: Explicit config only (Claude-MPM pattern) - User sets `launch_method: subprocess|exec` in config file. No automatic detection.
- B: Environment detection - Auto-detect: subprocess in development/CI (for debugging), exec in production (for clean handoff).
- C: Feature requirements - If monitoring/logging features are requested, use subprocess. Otherwise default to exec.
- D: Hybrid auto-select - Default to exec, but auto-switch to subprocess if debugging flags are present or if running under a debugger.

### Q15: What monitoring capabilities should subprocess mode provide?
**Context:** Subprocess mode allows MPM to remain as parent and monitor Claude Code child process.

Options:
- A: Basic monitoring - Process health (alive/dead), exit code capture, basic stdout/stderr logging.
- B: Event forwarding - Capture and forward hook events from Claude Code to external systems (dashboard, logging infrastructure).
- C: Interactive debugging - Allow debugger attachment, breakpoint setting, and live inspection of Claude Code state.
- D: Full observability - Process metrics (CPU, memory), event forwarding, stdout/stderr capture, and ability to inject signals/commands.

### Q16: How should subprocess mode handle child process termination?
**Context:** When Claude Code child exits, what should the parent orchestrator do?

Options:
- A: Exit with child's exit code - Parent immediately exits with same exit code as child. Clean propagation.
- B: Restart on failure - If child exits with error, attempt to restart it (with backoff). Exit if restart fails N times.
- C: Graceful cleanup - On child exit, parent performs cleanup (remove temp files, close connections) then exits.
- D: Interactive continuation - On child exit, parent prompts user for action: restart, debug, or quit.

---

## Questions: Gap Analysis Additions (Q17-Q18)

### Q17: Should Claude-Hybrid provide a real-time observability dashboard?
**Context:** Claude-MPM includes an aiohttp dashboard on port 8765 with Socket.IO (primary) + HTTP fallback for monitoring multi-agent operations in real-time.

Options:
- A: No dashboard - Rely on log files and CLI output for observability. Simpler architecture, no additional dependencies.
- B: Basic web dashboard - Lightweight HTTP server with static HTML showing agent status, recent events, and errors.
- C: Full real-time dashboard - Socket.IO/WebSocket for live updates, React-based UI with Events, Activity, and Files tabs.
- D: External integration only - Emit events to external observability platforms (DataDog, Prometheus) rather than built-in dashboard.

### Q18: How should Claude-Hybrid distinguish slash command invocation from Task tool invocation?
**Context:** Personal BMAD documents TWO parallel systems: Slash Commands (user EMBODIES persona, PERSISTENT state, menu access) vs Task Tool (orchestrator DELEGATES, STATELESS, fresh context). This is a fundamental execution model distinction.

Options:
- A: Unified execution model - No distinction; both slash commands and Task tool use same execution path and state handling.
- B: Invocation-aware context - Track invocation method in agent context; agent behavior adapts based on whether invoked via slash or Task.
- C: Separate execution paths - Slash commands maintain session state and menus; Task tool always gets fresh context with no menu access.
- D: Configuration-driven distinction - Agent frontmatter specifies which invocation methods are supported and their behavior differences.

---

## Resume Instructions

**Next session:** Read this file, continue from first PENDING question.
**Methodology:** BMad Master facilitates, President decides each question.
**After completion:** Update ARCHITECTURAL-DECISIONS.md with D6 decision.
