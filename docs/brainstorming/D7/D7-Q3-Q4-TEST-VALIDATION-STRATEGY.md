# D7-Q3 and D7-Q4: Tester Agent Validation Strategy

**Document Type:** Test Coverage Analysis & Recommendation
**Questions:** D7-Q3 (MCP Server Spawning Strategy) and D7-Q4 (Aggregator Configuration Management)
**Status:** TESTER AGENT ANALYSIS COMPLETE
**Generated:** 2025-12-11

---

## Executive Summary

This document provides comprehensive test coverage requirements, edge case analysis, complexity estimates, and regression risk assessment for D7-Q3 and D7-Q4. Both questions have critical dependencies on binding constraints from D5-Q8 (Session Boundary Only), D6-Q1 (Configurable exec mode), and D6-Q2 (Complete state death).

**Tester Agent Recommendations:**
- **D7-Q3:** Option D (Lazy + keep-alive) with confidence **7/10**
- **D7-Q4:** Option D (Layered config) with confidence **8/10**

---

## Binding Constraints Validation Matrix

Before analyzing each option, we must validate against these already-decided constraints:

| Constraint | Decision | Implication for D7-Q3/Q4 |
|------------|----------|--------------------------|
| **D5-Q8: Session Boundary Only** | Skills discovered at startup only, restart required for deployment | MCP servers should follow same semantics - no hot-reload |
| **D6-Q1: Configurable exec mode** | Support both exec and subprocess via config | MCP spawning must work in BOTH modes |
| **D6-Q2: Complete state death** | All in-memory state lost at handoff, files only survive | MCP config MUST be file-based, no in-memory persistence across handoff |

---

## D7-Q3: MCP Server Spawning Strategy

### Question Context
Should Claude-Hybrid spawn MCP servers on-demand or pre-warm them?

### Options Under Analysis

| Option | Strategy | Key Characteristic |
|--------|----------|-------------------|
| A | On-demand spawning | Clean handoff, 11.9s first-call delay |
| B | Pre-warming pool | Spawn critical servers at session start |
| C | Hybrid warm-up | Selective warming for fast servers |
| D | Lazy + keep-alive | Spawn on first use, keep running with timeout |

---

### Test Coverage Requirements by Option

#### Option A: On-demand Spawning

**Unit Tests (Simple)**
```
Test ID: D7Q3-A-U01
Description: Verify spawn triggers on first tool call
Scenario: Call mcp__ripgrep__search with no running server
Expected: Server spawns, tool executes, result returned
Complexity: Simple
```

```
Test ID: D7Q3-A-U02
Description: Verify cold start timing measurement
Scenario: Measure time from tool call to first response
Expected: Time recorded in metrics, ~11.9s for code-graph-rag
Complexity: Simple
```

```
Test ID: D7Q3-A-U03
Description: Verify clean process tree after spawn
Scenario: Spawn server, verify PID is child of aggregator
Expected: No orphan processes, clean parent-child relationship
Complexity: Simple
```

**Integration Tests (Medium)**
```
Test ID: D7Q3-A-I01
Description: Multiple concurrent first-call spawns
Scenario: 5 tools from different servers called simultaneously
Expected: 5 servers spawn independently without race conditions
Complexity: Medium
```

```
Test ID: D7Q3-A-I02
Description: Session boundary cleanup
Scenario: Session ends with 3 running MCP servers
Expected: All server processes terminated, no zombies
Complexity: Medium
Binding: D5-Q8 (Session Boundary Only)
```

```
Test ID: D7Q3-A-I03
Description: Handoff compatibility - exec mode
Scenario: Orchestrator spawns server, then exec handoff occurs
Expected: Server survives handoff OR is cleanly restarted
Complexity: Medium
Binding: D6-Q1 (Configurable exec mode)
```

**Edge Cases**
- Server binary missing from PATH
- Server crashes during spawn
- Aggregator crash with spawned servers still running
- Network partition during remote server spawn

**Failure Modes**
1. **Spawn timeout**: Server hangs during initialization
2. **FD leak**: File descriptors not properly closed on spawn failure
3. **Race condition**: Same server requested twice before first spawn completes

**Test Complexity: MEDIUM**
**Regression Risk: LOW** (simplest option, matches Claude-MPM pattern)

---

#### Option B: Pre-warming Pool

**Unit Tests (Simple)**
```
Test ID: D7Q3-B-U01
Description: Pre-warm servers at session start
Scenario: Session initiates with warm_servers: [memory, ripgrep]
Expected: Both servers running before first tool call
Complexity: Simple
```

```
Test ID: D7Q3-B-U02
Description: FD inheritance verification after execvpe
Scenario: Orchestrator pre-warms server, then exec to Claude Code
Expected: Server FDs properly handled (no inheritance conflicts)
Complexity: Medium
Binding: D6-Q2 (Complete state death)
```

**Integration Tests (Complex)**
```
Test ID: D7Q3-B-I01
Description: FD inheritance across process replacement
Scenario: Pre-warm 5 servers, exec handoff, verify no FD leaks
Expected: All pre-warmed servers either re-acquired OR cleanly killed
Complexity: Complex
Critical: This is the known FD inheritance bug in Claude-MPM
```

```
Test ID: D7Q3-B-I02
Description: Pool size management
Scenario: Configure pool_size: 3, request 5 different servers
Expected: Pool rotates correctly, LRU eviction of oldest server
Complexity: Complex
```

```
Test ID: D7Q3-B-I03
Description: Warm server health check
Scenario: Pre-warmed server crashes after warm-up but before use
Expected: System detects dead server, re-spawns on demand
Complexity: Medium
```

**Edge Cases**
- Pre-warm server that was already running from previous session
- Pre-warm list contains non-existent server
- Session start during server spawn (partially warmed state)
- execvpe() inherits warm server FDs causing spawn conflicts

**Failure Modes**
1. **FD inheritance conflict**: Known bug, warm server FDs leak across exec
2. **Resource exhaustion**: Too many pre-warmed servers consume memory
3. **Orphan servers**: Warm servers not killed on session abort
4. **State leakage**: Warm server has stale state from initialization

**Test Complexity: COMPLEX**
**Regression Risk: HIGH** (FD inheritance is a known failure mode)

---

#### Option C: Hybrid Warm-up (Selective)

**Unit Tests (Simple)**
```
Test ID: D7Q3-C-U01
Description: Categorize servers by warm-up eligibility
Scenario: Parse config with fast_warm: [memory, ripgrep], slow_ondemand: [code-graph-rag]
Expected: Correct classification returned
Complexity: Simple
```

```
Test ID: D7Q3-C-U02
Description: Fast server warm-up timing
Scenario: Warm memory and ripgrep at session start
Expected: Both ready in < 2 seconds
Complexity: Simple
```

**Integration Tests (Medium-Complex)**
```
Test ID: D7Q3-C-I01
Description: Mixed spawn lifecycle
Scenario: memory (warm) + code-graph-rag (on-demand) both called
Expected: memory responds immediately, code-graph-rag has cold delay
Complexity: Medium
```

```
Test ID: D7Q3-C-I02
Description: FD inheritance for warm-only servers
Scenario: Only warm fast servers, exec handoff
Expected: No FD conflicts (fast servers have simpler FD usage)
Complexity: Medium
Binding: D6-Q1, D6-Q2
```

```
Test ID: D7Q3-C-I03
Description: Category boundary validation
Scenario: User misconfigures slow server as fast
Expected: Warning logged, falls back to on-demand
Complexity: Medium
```

**Edge Cases**
- Server moves from fast to slow category after update
- Warm server has cold dependency (e.g., memory needs SQLite init)
- Hybrid state during session start failure

**Failure Modes**
1. **Category misclassification**: Fast server actually slow, blocks startup
2. **Partial warm**: Some fast servers warm, others fail
3. **Cross-category dependency**: On-demand server depends on warm server state

**Test Complexity: MEDIUM-HIGH**
**Regression Risk: MEDIUM** (requires careful category management)

---

#### Option D: Lazy + Keep-alive

**Unit Tests (Simple)**
```
Test ID: D7Q3-D-U01
Description: First-use spawn with keep-alive
Scenario: Call ripgrep.search, then wait, call again
Expected: Second call uses running server (no spawn delay)
Complexity: Simple
```

```
Test ID: D7Q3-D-U02
Description: Keep-alive timeout expiration
Scenario: Spawn server, wait past keep_alive_timeout
Expected: Server terminated after timeout
Complexity: Simple
```

```
Test ID: D7Q3-D-U03
Description: Keep-alive refresh on activity
Scenario: Spawn server, use it repeatedly within timeout
Expected: Timeout resets on each use, server stays alive
Complexity: Simple
```

**Integration Tests (Medium)**
```
Test ID: D7Q3-D-I01
Description: Session boundary vs keep-alive
Scenario: Server has 10min keep-alive, session ends at 5min
Expected: Server killed at session end regardless of timeout
Complexity: Medium
Binding: D5-Q8 (Session Boundary Only)
```

```
Test ID: D7Q3-D-I02
Description: Multiple server keep-alive management
Scenario: 5 servers spawn, each with different timeouts
Expected: Each managed independently, correct expiration order
Complexity: Medium
```

```
Test ID: D7Q3-D-I03
Description: Keep-alive across exec handoff
Scenario: Server running with keep-alive, exec handoff occurs
Expected: Server continues OR is re-acquired by new process
Complexity: Medium
Binding: D6-Q1, D6-Q2
```

```
Test ID: D7Q3-D-I04
Description: Resource pressure during keep-alive
Scenario: System under memory pressure, servers in keep-alive
Expected: LRU eviction of least-used servers
Complexity: Medium
```

**Edge Cases**
- Keep-alive timer race with session end
- Server crash during keep-alive (health check needed)
- Configuration change to timeout while server running
- Keep-alive server receives update notification

**Failure Modes**
1. **Timeout drift**: Timer inaccuracy causes premature/late expiration
2. **Zombie keep-alive**: Server marked alive but actually dead
3. **Resource leak**: Keep-alive prevents cleanup under pressure
4. **Timer management overhead**: Many timers for many servers

**Test Complexity: MEDIUM**
**Regression Risk: LOW-MEDIUM** (well-understood pattern, no FD inheritance issues)

---

### D7-Q3 Comparative Analysis

| Criterion | Option A | Option B | Option C | Option D |
|-----------|----------|----------|----------|----------|
| Test Count (est.) | 12 | 18 | 15 | 14 |
| Complexity | Medium | Complex | Medium-High | Medium |
| Regression Risk | Low | **HIGH** | Medium | Low-Medium |
| D5-Q8 Compliance | Yes | Risky | Partial | Yes |
| D6-Q1 Compliance | Yes | Risky | Partial | Yes |
| D6-Q2 Compliance | Yes | **NO** | Risky | Yes |
| Edge Cases | 4 | 5 | 4 | 4 |
| Known Bugs | None | FD inheritance | None | None |

### D7-Q3 Tester Agent Recommendation

**Recommended: Option D (Lazy + keep-alive)**
**Confidence: 7/10**

**Rationale:**
1. **Binding Constraint Compliance**: Fully compliant with D5-Q8, D6-Q1, D6-Q2
2. **No FD Inheritance Risk**: Unlike Option B, no pre-warm phase before exec
3. **Better UX than A**: Subsequent calls fast due to keep-alive
4. **Simpler than C**: No category management complexity
5. **Testability**: Well-understood timer patterns, existing test infrastructure

**Testing Concerns:**
- Timer management adds modest complexity
- Health check mechanism needed for zombie detection
- Session boundary interaction requires careful testing

**Confidence Deductions:**
- -2: Timer management is subtle, edge cases in timeout handling
- -1: Need to verify keep-alive works correctly with both exec and subprocess modes

---

## D7-Q4: Aggregator Configuration Management

### Question Context
How should Claude-Hybrid manage aggregator configuration?

### Options Under Analysis

| Option | Strategy | Key Characteristic |
|--------|----------|-------------------|
| A | Static config file | Require restart for changes |
| B | Dynamic runtime config | Add/remove servers without restart |
| C | Project-scoped config | Per-project overrides |
| D | Layered config | Global + project + runtime merged |

---

### Test Coverage Requirements by Option

#### Option A: Static Config File

**Unit Tests (Simple)**
```
Test ID: D7Q4-A-U01
Description: Load config from ~/.claude/mcp-aggregator/config.json
Scenario: Valid config file exists
Expected: All servers loaded, correct timeout values
Complexity: Simple
```

```
Test ID: D7Q4-A-U02
Description: Config file validation
Scenario: Config has invalid server entry
Expected: Validation error with clear message
Complexity: Simple
```

```
Test ID: D7Q4-A-U03
Description: Config file not found
Scenario: ~/.claude/mcp-aggregator/config.json missing
Expected: Use bundled defaults, log warning
Complexity: Simple
```

**Integration Tests (Simple)**
```
Test ID: D7Q4-A-I01
Description: Session start loads config once
Scenario: Start session, modify config file mid-session
Expected: Changes NOT reflected until restart
Complexity: Simple
Binding: D5-Q8 (Session Boundary Only)
```

```
Test ID: D7Q4-A-I02
Description: Config survives exec handoff
Scenario: Config loaded by orchestrator, exec handoff
Expected: Claude Code reads same config from disk
Complexity: Simple
Binding: D6-Q2 (Complete state death)
```

**Edge Cases**
- Config file permissions error
- Config file corrupted mid-read
- Unicode in server names/paths
- Very large config (100+ servers)

**Failure Modes**
1. **Stale config**: User forgets to restart after change
2. **File lock**: Config file locked by another process
3. **Partial write**: Config file truncated during write

**Test Complexity: SIMPLE**
**Regression Risk: LOW** (simplest option, well-understood pattern)

---

#### Option B: Dynamic Runtime Config

**Unit Tests (Medium)**
```
Test ID: D7Q4-B-U01
Description: Add server at runtime
Scenario: Call aggregator.add_server({name: "new-server", ...})
Expected: Server immediately available for tool calls
Complexity: Medium
```

```
Test ID: D7Q4-B-U02
Description: Remove server at runtime
Scenario: Call aggregator.remove_server("ripgrep") while in use
Expected: Graceful shutdown, pending calls complete or error
Complexity: Medium
```

```
Test ID: D7Q4-B-U03
Description: Update server config at runtime
Scenario: Call aggregator.update_server("memory", {timeout: 300})
Expected: New timeout applies to subsequent calls
Complexity: Medium
```

**Integration Tests (Complex)**
```
Test ID: D7Q4-B-I01
Description: Runtime changes vs session boundary
Scenario: Add server at runtime, session restarts
Expected: Runtime changes NOT persisted (or explicit save needed)
Complexity: Complex
Binding: D5-Q8 (Session Boundary Only) - POTENTIAL CONFLICT
```

```
Test ID: D7Q4-B-I02
Description: Concurrent runtime modification
Scenario: Two tasks simultaneously add/remove servers
Expected: No race conditions, consistent final state
Complexity: Complex
```

```
Test ID: D7Q4-B-I03
Description: Runtime config and exec handoff
Scenario: Runtime config changes, then exec handoff
Expected: Runtime state LOST (not on disk)
Complexity: Complex
Binding: D6-Q2 (Complete state death) - CONFLICT
```

**Edge Cases**
- Add server that already exists
- Remove server with active connections
- Update server during tool execution
- Circular dependency in runtime additions

**Failure Modes**
1. **State loss at handoff**: Runtime config not persisted
2. **Race conditions**: Concurrent modifications corrupt state
3. **Memory pressure**: Runtime additions never cleaned up
4. **Inconsistent state**: Partial modification on error

**Test Complexity: COMPLEX**
**Regression Risk: HIGH** (conflicts with D6-Q2 binding constraint)

---

#### Option C: Project-scoped Config

**Unit Tests (Simple)**
```
Test ID: D7Q4-C-U01
Description: Load project config from .claude.json
Scenario: Project directory contains .claude.json with MCP overrides
Expected: Project config merged with global, project takes precedence
Complexity: Simple
```

```
Test ID: D7Q4-C-U02
Description: Project config not found
Scenario: No .claude.json in project or parents
Expected: Fall back to global config only
Complexity: Simple
```

```
Test ID: D7Q4-C-U03
Description: Project config validation
Scenario: .claude.json has invalid MCP server entry
Expected: Validation error, project config rejected
Complexity: Simple
```

**Integration Tests (Medium)**
```
Test ID: D7Q4-C-I01
Description: Project precedence over global
Scenario: Global: timeout=120, Project: timeout=60 for same server
Expected: 60s timeout used
Complexity: Medium
```

```
Test ID: D7Q4-C-I02
Description: Project-specific server additions
Scenario: Project adds custom-project-server not in global
Expected: Server available only in this project context
Complexity: Medium
```

```
Test ID: D7Q4-C-I03
Description: Project config and session boundary
Scenario: Change .claude.json mid-session
Expected: Changes NOT applied until restart
Complexity: Medium
Binding: D5-Q8 (Session Boundary Only)
```

```
Test ID: D7Q4-C-I04
Description: Project config survives exec handoff
Scenario: Project config loaded, exec handoff
Expected: Claude Code reads same .claude.json from disk
Complexity: Medium
Binding: D6-Q2 (Complete state death)
```

**Edge Cases**
- Nested projects with conflicting configs
- Project config in parent directory
- Project moves to different directory mid-session
- Symlinked project directories

**Failure Modes**
1. **Wrong project detection**: Config loaded from wrong project
2. **Stale project cache**: Project config cached, doesn't reflect changes
3. **Path resolution**: Relative paths in project config

**Test Complexity: MEDIUM**
**Regression Risk: MEDIUM** (project detection can be tricky)

---

#### Option D: Layered Config (Global + Project + Runtime)

**Unit Tests (Medium)**
```
Test ID: D7Q4-D-U01
Description: Three-layer merge order
Scenario: Global, project, and runtime all define same server
Expected: Runtime > Project > Global precedence
Complexity: Medium
```

```
Test ID: D7Q4-D-U02
Description: Partial layer override
Scenario: Global defines 10 servers, project overrides 2
Expected: 10 servers total, 2 with project overrides
Complexity: Medium
```

```
Test ID: D7Q4-D-U03
Description: Empty layer handling
Scenario: No project config, no runtime changes
Expected: Global config used exclusively
Complexity: Simple
```

**Integration Tests (Medium)**
```
Test ID: D7Q4-D-I01
Description: Layer merge at session start
Scenario: Session starts with all 3 layers populated
Expected: Merged config computed once at startup
Complexity: Medium
Binding: D5-Q8 (Session Boundary Only)
```

```
Test ID: D7Q4-D-I02
Description: Runtime layer and persistence
Scenario: Runtime modification made, should it persist?
Expected: Runtime is ephemeral, only global/project persisted
Complexity: Medium
```

```
Test ID: D7Q4-D-I03
Description: Layered config and exec handoff
Scenario: Merged config in memory, exec handoff occurs
Expected: Claude Code re-merges from files (global + project)
Complexity: Medium
Binding: D6-Q2 (Complete state death)
```

```
Test ID: D7Q4-D-I04
Description: Layer conflict reporting
Scenario: Project config conflicts with global in non-obvious way
Expected: Warning logged about override
Complexity: Medium
```

**Edge Cases**
- Circular references across layers
- Layer defines server that conflicts with built-in
- Deep merge vs shallow merge semantics
- Array handling in config merge (append vs replace)

**Failure Modes**
1. **Merge ambiguity**: Unclear which layer "wins"
2. **Stale merge**: Merged config not refreshed
3. **Memory overhead**: Keeping all layers in memory
4. **Debug difficulty**: Hard to trace final value source

**Test Complexity: MEDIUM**
**Regression Risk: LOW-MEDIUM** (well-understood pattern if runtime is ephemeral)

---

### D7-Q4 Comparative Analysis

| Criterion | Option A | Option B | Option C | Option D |
|-----------|----------|----------|----------|----------|
| Test Count (est.) | 8 | 15 | 12 | 14 |
| Complexity | Simple | Complex | Medium | Medium |
| Regression Risk | Low | **HIGH** | Medium | Low-Medium |
| D5-Q8 Compliance | Yes | **NO** | Yes | Yes |
| D6-Q1 Compliance | Yes | Yes | Yes | Yes |
| D6-Q2 Compliance | Yes | **NO** | Yes | Yes (if runtime ephemeral) |
| Flexibility | Low | High | Medium | High |
| Edge Cases | 4 | 5 | 4 | 4 |

### D7-Q4 Tester Agent Recommendation

**Recommended: Option D (Layered config)**
**Confidence: 8/10**

**Rationale:**
1. **Binding Constraint Compliance**: Fully compliant if runtime layer is ephemeral
2. **Flexibility**: Project-scoped overrides enable per-project customization
3. **Simplicity at Boundaries**: At exec handoff, only file-based layers persist
4. **User Experience**: Users can customize per-project without global changes
5. **Testability**: Config merging is deterministic and well-understood

**Design Constraint for Compliance:**
- Runtime layer MUST be ephemeral (not persisted to disk automatically)
- At session start, merge happens from files only (global + project)
- Runtime changes apply within session but are lost at restart

**Testing Concerns:**
- Merge precedence must be clearly documented and tested
- Array handling in config needs explicit semantics (replace vs append)
- Conflict reporting useful for debugging

**Confidence Deductions:**
- -1: Merge semantics need careful documentation
- -1: Runtime layer ephemeral constraint must be enforced

---

## Cross-Question Test Matrix

Tests that validate both decisions together:

```
Test ID: D7-CROSS-01
Description: Layered config with lazy keep-alive
Scenario: Project config sets keep_alive_timeout: 300 for ripgrep
Expected: Project override applies to lazy-spawned server
Complexity: Medium
```

```
Test ID: D7-CROSS-02
Description: Session boundary cleanup with layered config
Scenario: Session ends with runtime config changes and keep-alive servers
Expected: Both runtime config AND servers cleaned up
Complexity: Medium
Binding: D5-Q8, D6-Q2
```

```
Test ID: D7-CROSS-03
Description: Exec handoff with both decisions
Scenario: Orchestrator: layered config loaded, 2 servers in keep-alive, exec to Claude Code
Expected: Claude Code re-reads config from files, servers re-acquired or respawned
Complexity: Complex
Binding: D6-Q1, D6-Q2
```

---

## Test Infrastructure Requirements

### Required Test Fixtures

1. **Mock MCP Server** - Configurable spawn time, crash on demand
2. **Config File Generator** - Create valid/invalid configs programmatically
3. **Process Monitor** - Track spawned processes, detect orphans/zombies
4. **Timer Mock** - Control time for keep-alive timeout testing
5. **Session Simulator** - Trigger session start/end/handoff events

### Test Categories and Execution Strategy

| Category | Test Count | Execution Time | Run Frequency |
|----------|------------|----------------|---------------|
| Unit Tests | ~25 | < 1 min | Every commit |
| Integration Tests | ~18 | 5-10 min | Every PR |
| Cross-Question Tests | ~5 | 2-3 min | Every PR |
| Edge Case Tests | ~15 | 3-5 min | Every PR |
| E2E Tests | ~5 | 10-15 min | Nightly |

### Suggested Test File Structure

```
tests/
  integration/
    mcp/
      test_mcp_spawning_strategies.py      # D7-Q3 tests
      test_mcp_config_management.py        # D7-Q4 tests
      test_mcp_cross_decision.py           # Cross-question tests
      conftest.py                          # Shared fixtures
      fixtures/
        mock_mcp_server.py
        config_generator.py
```

---

## Summary

### D7-Q3: MCP Server Spawning Strategy
- **Recommendation:** Option D (Lazy + keep-alive)
- **Confidence:** 7/10
- **Test Complexity:** Medium (14 tests estimated)
- **Regression Risk:** Low-Medium
- **Key Concern:** Timer management and health checks

### D7-Q4: Aggregator Configuration Management
- **Recommendation:** Option D (Layered config)
- **Confidence:** 8/10
- **Test Complexity:** Medium (14 tests estimated)
- **Regression Risk:** Low-Medium
- **Key Constraint:** Runtime layer must be ephemeral for D6-Q2 compliance

### Combined Implementation Notes

Both recommended options (D7-Q3-D and D7-Q4-D) work well together:
- Layered config specifies timeouts and server categories
- Lazy spawning reads from merged config at spawn time
- Keep-alive uses timeout from final merged config
- Session end cleans both runtime config AND spawned servers
- Exec handoff re-reads files and re-spawns as needed (no state transfer)

---

*Document generated by Tester Agent for BMad Decision Framework*
