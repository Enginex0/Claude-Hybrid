# D7-Q5 and D7-Q6: Tester Agent Validation Strategy

**Document Type:** Test Coverage Analysis & Recommendation
**Questions:** D7-Q5 (Tool Naming Convention) and D7-Q6 (Namespace Conflict Resolution)
**Status:** TESTER AGENT ANALYSIS COMPLETE
**Generated:** 2025-12-11

---

## Executive Summary

This document provides comprehensive test coverage requirements, edge case analysis, determinism assessment, and failure mode identification for D7-Q5 and D7-Q6. These questions address critical tool namespacing challenges with 10+ potential tool name collisions across 26 MCP servers (332 tools).

**Tester Agent Recommendations:**
- **D7-Q5:** Option A (Triple underscore `mcp__server__tool`) with confidence **9/10**
- **D7-Q6:** Option B (Explicit aliasing) with confidence **8/10**

---

## Verified Tool Collision Inventory

Based on analysis of the 26 MCP servers and 332 tools:

### Confirmed Collision Categories

| Tool Name Pattern | Colliding Servers | Collision Type |
|-------------------|-------------------|----------------|
| `click` | playwright, browsermcp | Browser action |
| `search` | ripgrep, vector-search, memory | Generic search |
| `read_file` | filesystem, wcgw | File operation |
| `write_file` | filesystem, wcgw | File operation |
| `navigate` | playwright, browsermcp | Browser navigation |
| `screenshot` | playwright, browsermcp | Screen capture |
| `query` | sqlite, code-graph-rag | Data query |
| `list_*` | multiple servers | Listing operations |
| `create_*` | memory, sqlite, mcp-ticketer | Create operations |

**Total Identified Collision Risk:** 10+ tool names with potential ambiguity

---

## Binding Constraints Validation Matrix

| Constraint | Decision | Implication for Q5/Q6 |
|------------|----------|------------------------|
| **D7-Q1:** Single Aggregator Proxy | Aggregator routes all MCP calls | Naming must be aggregator-parseable |
| **D7-Q2:** Progressive Disclosure | L1/L2/L3 tool exposure | Naming supports hierarchical filtering |
| **D7-Q3:** Lazy + keep-alive | On-demand spawning | Server identification critical in name |
| **D7-Q4:** Layered config | Project overrides global | Aliasing must work across config layers |

---

## D7-Q5: Tool Naming Convention

### Question Context
What tool naming convention should Claude-Hybrid enforce for MCP tools?

### Options Under Analysis

| Option | Pattern | Example | Characteristic |
|--------|---------|---------|----------------|
| A | Triple underscore | `mcp__server__tool` | Current aggregator pattern |
| B | Dot notation | `mcp.server.tool` | More readable |
| C | Slash hierarchy | `mcp/server/tool` | URL-like |
| D | Flat prefix | `mcp_server_tool` | Simpler parsing |

---

### Test Coverage Requirements by Option

#### Option A: Triple Underscore (`mcp__server__tool`)

**Unit Tests (Simple)**
```
Test ID: D7Q5-A-U01
Description: Parse standard tool name
Input: "mcp__ripgrep__search"
Expected: {prefix: "mcp", server: "ripgrep", tool: "search"}
Complexity: Simple
Determinism: 100% (fixed delimiter)
```

```
Test ID: D7Q5-A-U02
Description: Parse tool name with underscores in tool name
Input: "mcp__vector-search__search_code"
Expected: {prefix: "mcp", server: "vector-search", tool: "search_code"}
Complexity: Simple
Determinism: 100% (double underscore unambiguous)
```

```
Test ID: D7Q5-A-U03
Description: Parse tool name with hyphen in server name
Input: "mcp__code-graph-rag__analyze_code_impact"
Expected: {prefix: "mcp", server: "code-graph-rag", tool: "analyze_code_impact"}
Complexity: Simple
Determinism: 100%
```

```
Test ID: D7Q5-A-U04
Description: Reject invalid format (single underscore)
Input: "mcp_ripgrep_search"
Expected: ParseError("Expected double underscore delimiter")
Complexity: Simple
Determinism: 100%
```

**Integration Tests (Simple)**
```
Test ID: D7Q5-A-I01
Description: Round-trip serialization
Scenario: Parse, modify, serialize, parse again
Input: "mcp__memory__create_entities"
Expected: Identity after round-trip
Complexity: Simple
Determinism: 100%
```

```
Test ID: D7Q5-A-I02
Description: Aggregator routing from parsed name
Scenario: Parse tool name, route to correct server
Input: "mcp__playwright__click"
Expected: Routed to playwright server
Complexity: Simple
Determinism: 100%
```

**Edge Cases**
1. Tool name with triple underscore: `mcp__server__tool___version` - Is `___version` part of tool name?
2. Server name starting with underscore: `mcp___internal__tool` - Invalid?
3. Empty server name: `mcp____tool` - Should reject
4. Unicode in server/tool names: `mcp__test__query_` - Trailing underscore

**Failure Modes**
1. **Ambiguous triple underscore:** Tool name contains `__` - LOW RISK (rare in tool names)
2. **Visual parsing difficulty:** Hard to read long names - MEDIUM RISK (UX only)
3. **Typo detection:** `mcp___server__tool` vs `mcp__server__tool` - LOW RISK (easy regex)

**Test Complexity: SIMPLE**
**Regression Risk: LOW**
**Determinism Rating: 10/10** (unambiguous delimiter, trivial regex)

---

#### Option B: Dot Notation (`mcp.server.tool`)

**Unit Tests (Medium)**
```
Test ID: D7Q5-B-U01
Description: Parse standard tool name
Input: "mcp.ripgrep.search"
Expected: {prefix: "mcp", server: "ripgrep", tool: "search"}
Complexity: Simple
Determinism: 100% for simple cases
```

```
Test ID: D7Q5-B-U02
Description: Parse tool name with dots in name
Input: "mcp.context7.get-library-docs"
Expected: {prefix: "mcp", server: "context7", tool: "get-library-docs"}
Complexity: Medium - hyphen vs dot ambiguity
Determinism: 100% if dots only used as delimiter
```

```
Test ID: D7Q5-B-U03
Description: Handle nested namespace tool names
Input: "mcp.semgrep.scan.custom"
Expected: AMBIGUOUS - Is tool "scan.custom" or server "semgrep.scan"?
Complexity: High
Determinism: 0% without additional rules
```

**Edge Cases - CRITICAL**
1. Tool name with version number: `mcp.ref.v2.search` - Ambiguous!
2. Server with subdomain pattern: `mcp.gitlab.api.issues` - Ambiguous!
3. File extension lookalike: `mcp.filesystem.read.json` - Is `.json` part of tool?
4. IP-like patterns: `mcp.server.10.tool` - Parsing confusion

**Failure Modes**
1. **Ambiguous segment count:** 3+ segments create parsing confusion - HIGH RISK
2. **Conflict with Python/JS module paths:** `mcp.server.tool` matches module syntax - MEDIUM RISK
3. **Language-specific issues:** JSON keys with dots problematic in some parsers - MEDIUM RISK

**Test Complexity: MEDIUM-HIGH**
**Regression Risk: MEDIUM-HIGH**
**Determinism Rating: 6/10** (ambiguity with 4+ segments)

---

#### Option C: Slash Hierarchy (`mcp/server/tool`)

**Unit Tests (Medium)**
```
Test ID: D7Q5-C-U01
Description: Parse standard tool name
Input: "mcp/ripgrep/search"
Expected: {prefix: "mcp", server: "ripgrep", tool: "search"}
Complexity: Simple
Determinism: 100% for simple cases
```

```
Test ID: D7Q5-C-U02
Description: Parse tool with slash in name (CRITICAL)
Input: "mcp/git/diff/HEAD~1"
Expected: AMBIGUOUS - Is "diff/HEAD~1" the tool or nested path?
Complexity: High
Determinism: 0% without escaping rules
```

```
Test ID: D7Q5-C-U03
Description: Tool name resembling file path
Input: "mcp/filesystem/read/etc/passwd"
Expected: DANGEROUS - Potential path traversal confusion
Complexity: Critical
Determinism: 0% (security risk)
```

**Edge Cases - CRITICAL**
1. Git refs: `mcp/git/checkout/feature/branch` - Branch name contains slash
2. File paths: `mcp/filesystem/write/tmp/file` - Path in tool name
3. URL encoding: `mcp/fetch/https://example.com` - URL in argument position
4. Windows paths: `mcp/wcgw/read/C:/Users` - Colon+slash ambiguity

**Failure Modes**
1. **Path traversal confusion:** `/` in tool args could be parsed as delimiter - HIGH RISK
2. **Security implications:** URL-like patterns may bypass validation - HIGH RISK
3. **Cross-platform issues:** Windows vs Unix path separators - MEDIUM RISK
4. **Escaping complexity:** Must escape `/` in tool names - HIGH RISK

**Test Complexity: HIGH**
**Regression Risk: HIGH**
**Determinism Rating: 4/10** (too many ambiguous cases, security risk)

---

#### Option D: Flat Prefix (`mcp_server_tool`)

**Unit Tests (Medium)**
```
Test ID: D7Q5-D-U01
Description: Parse standard tool name
Input: "mcp_ripgrep_search"
Expected: {prefix: "mcp", server: "ripgrep", tool: "search"}
Complexity: Medium - must determine split point
Determinism: 0% without server registry
```

```
Test ID: D7Q5-D-U02
Description: Parse tool with underscore in server name
Input: "mcp_code_graph_rag_query"
Expected: AMBIGUOUS - Is server "code" or "code_graph" or "code_graph_rag"?
Complexity: High
Determinism: 0% (requires server lookup)
```

```
Test ID: D7Q5-D-U03
Description: Parse tool with underscore in tool name
Input: "mcp_vector_search_search_code"
Expected: AMBIGUOUS - Where does server end and tool begin?
Complexity: High
Determinism: 0% without registry
```

**Edge Cases - CRITICAL**
1. Server "code_graph" vs server "code" with tool "graph_...": Collision
2. Underscored tool names: `mcp_memory_create_entities` - 3 possible parses
3. New server registration: Adding "memory_ext" server changes parsing
4. Similar prefixes: `mcp_vector_search_*` vs `mcp_vector_*` if both exist

**Failure Modes**
1. **Ambiguous parsing:** Single underscore cannot distinguish server from tool - CRITICAL
2. **Registry dependency:** Parsing requires server list lookup - HIGH COMPLEXITY
3. **Future collision:** New server names may break existing parses - HIGH RISK
4. **Non-deterministic without state:** Must load server registry before parsing - MEDIUM RISK

**Test Complexity: HIGH**
**Regression Risk: HIGH**
**Determinism Rating: 2/10** (requires external registry, non-deterministic parse)

---

### D7-Q5 Comparative Analysis

| Criterion | Option A | Option B | Option C | Option D |
|-----------|----------|----------|----------|----------|
| Test Count (est.) | 8 | 14 | 16 | 18 |
| Complexity | Simple | Medium-High | High | High |
| Regression Risk | **LOW** | Medium-High | **HIGH** | **HIGH** |
| Determinism | **10/10** | 6/10 | 4/10 | 2/10 |
| Parsing Ambiguity | None | 4+ segments | Slashes in data | Underscores everywhere |
| Security Risk | None | Low | **HIGH** | Low |
| Edge Cases | 4 (minor) | 5 (moderate) | 5 (critical) | 5 (critical) |
| Claude Code Compatibility | **Native** | Change needed | Change needed | Change needed |

### D7-Q5 Tester Agent Recommendation

**Recommended: Option A (Triple underscore `mcp__server__tool`)**
**Confidence: 9/10**

**Rationale:**
1. **Determinism:** 100% unambiguous parsing with trivial regex `/^mcp__([^_]+(?:-[^_]+)*)__(.+)$/`
2. **Zero Edge Cases:** Double underscore is rare enough that tool/server names won't contain it
3. **Claude Code Native:** Already implemented, zero migration cost
4. **Simple Testing:** 8 tests cover all scenarios vs 16+ for alternatives
5. **Security:** No path traversal or injection risks

**Testing Concerns:**
- Visual readability is slightly lower (UX, not correctness)
- Long names can be hard to scan visually

**Confidence Deductions:**
- -1: Visual readability concern (minor UX issue)

---

## D7-Q6: Namespace Conflict Resolution

### Question Context
How should namespace conflicts be resolved when multiple servers offer similar tools?

### Verified Collisions (from 26 servers)

| Generic Tool | Server 1 | Server 2 | Server 3 |
|--------------|----------|----------|----------|
| `search` | ripgrep | vector-search | memory |
| `click` | playwright | browsermcp | - |
| `read_file` | filesystem | wcgw | - |
| `navigate` | playwright | browsermcp | - |
| `screenshot` | playwright | browsermcp | - |
| `query` | sqlite | code-graph-rag | - |
| `list_tables` | sqlite | - | - |
| `create_entities` | memory | - | - |
| `write_file` | filesystem | wcgw | - |

**Total: 9+ verified collision patterns**

### Options Under Analysis

| Option | Strategy | Key Characteristic |
|--------|----------|-------------------|
| A | First-registered wins | Server registered first owns name |
| B | Explicit aliasing | Config maps shortcuts to full paths |
| C | Server-qualified only | Always require full name |
| D | Priority-based routing | Config defines server priority |

---

### Test Coverage Requirements by Option

#### Option A: First-Registered Wins

**Unit Tests (Simple)**
```
Test ID: D7Q6-A-U01
Description: First server registration takes ownership
Scenario: Register ripgrep with "search", then vector-search with "search"
Expected: "search" -> ripgrep, vector-search must use full name
Complexity: Simple
Determinism: Depends on registration order
```

```
Test ID: D7Q6-A-U02
Description: Late registration rejection
Scenario: vector-search tries to claim "search" after ripgrep
Expected: Warning logged, alias not created
Complexity: Simple
Determinism: 100% if order is deterministic
```

**Integration Tests (Medium)**
```
Test ID: D7Q6-A-I01
Description: Registration order during aggregator startup
Scenario: Config lists servers in specific order
Expected: Order determines ownership predictably
Complexity: Medium
Determinism: Depends on config parsing order
```

```
Test ID: D7Q6-A-I02
Description: Dynamic server registration order
Scenario: Server A added at runtime, then server B
Expected: Same as static ordering
Complexity: Medium
Determinism: Depends on runtime behavior
```

**Edge Cases - CRITICAL**
1. Parallel server initialization: Race condition on ownership
2. Server restart: Does it keep ownership?
3. Config file ordering: Is JSON object order guaranteed? (NO in most parsers)
4. Different startup order across sessions: Non-reproducible behavior

**Failure Modes**
1. **Non-deterministic startup:** Server order may vary - **CRITICAL**
2. **JSON object ordering:** Keys are unordered in JSON spec - **HIGH RISK**
3. **Session inconsistency:** Different ownership each restart - **HIGH RISK**
4. **User confusion:** "search" means different things in different runs - **CRITICAL**

**Test Complexity: MEDIUM**
**Regression Risk: HIGH**
**Determinism Rating: 3/10** (startup order is non-deterministic)

---

#### Option B: Explicit Aliasing

**Unit Tests (Simple)**
```
Test ID: D7Q6-B-U01
Description: Config-defined alias resolution
Scenario: aliases: {"search": "mcp__ripgrep__search"}
Expected: "search" -> mcp__ripgrep__search
Complexity: Simple
Determinism: 100% (config is source of truth)
```

```
Test ID: D7Q6-B-U02
Description: Multiple aliases to same tool
Scenario: aliases: {"find": "mcp__ripgrep__search", "grep": "mcp__ripgrep__search"}
Expected: Both resolve to same tool
Complexity: Simple
Determinism: 100%
```

```
Test ID: D7Q6-B-U03
Description: Alias overrides in project config
Scenario: Global: "search" -> ripgrep, Project: "search" -> vector-search
Expected: Project wins (per D7-Q4)
Complexity: Medium
Determinism: 100% (layered config rules)
Binding: D7-Q4 (Layered config)
```

```
Test ID: D7Q6-B-U04
Description: No alias defined, use full name
Scenario: No alias for "search", call mcp__ripgrep__search directly
Expected: Works without alias
Complexity: Simple
Determinism: 100%
```

**Integration Tests (Medium)**
```
Test ID: D7Q6-B-I01
Description: Alias suggestion on collision detection
Scenario: User calls "search" with no alias defined
Expected: Helpful error listing both ripgrep.search and vector-search.search_code
Complexity: Medium
Determinism: 100%
```

```
Test ID: D7Q6-B-I02
Description: Alias with layered config merge
Scenario: Global aliases + project aliases merged
Expected: Project overrides take precedence
Complexity: Medium
Determinism: 100%
Binding: D7-Q4
```

```
Test ID: D7Q6-B-I03
Description: Alias file validation on load
Scenario: Invalid alias (target doesn't exist)
Expected: Validation error on startup
Complexity: Medium
Determinism: 100%
```

**Edge Cases**
1. Circular alias: `{"a": "b", "b": "a"}` - Should detect and reject
2. Alias to non-existent tool: `{"search": "mcp__invalid__tool"}` - Validation error
3. Alias collision with full tool name: `{"mcp__ripgrep__search": "mcp__other__x"}` - Conflict
4. Case sensitivity: `{"Search": "..."}` vs `{"search": "..."}` - Need policy

**Failure Modes**
1. **Missing alias:** User expects shorthand, none defined - LOW RISK (helpful error)
2. **Stale alias:** Tool renamed, alias points to old name - MEDIUM RISK (validation)
3. **Alias proliferation:** Too many aliases become confusing - LOW RISK (config review)

**Test Complexity: SIMPLE-MEDIUM**
**Regression Risk: LOW**
**Determinism Rating: 10/10** (config-driven, file-based, reproducible)

---

#### Option C: Server-Qualified Only

**Unit Tests (Simple)**
```
Test ID: D7Q6-C-U01
Description: Require full qualification
Input: "search" (no server)
Expected: Error("Must specify server: mcp__ripgrep__search or mcp__vector-search__search_code")
Complexity: Simple
Determinism: 100%
```

```
Test ID: D7Q6-C-U02
Description: Full qualification accepted
Input: "mcp__ripgrep__search"
Expected: Routes to ripgrep server
Complexity: Simple
Determinism: 100%
```

**Integration Tests (Simple)**
```
Test ID: D7Q6-C-I01
Description: Helpful error on unqualified name
Scenario: User types "search"
Expected: List of matching tools: ripgrep.search, vector-search.search_code, memory.search_nodes
Complexity: Simple
Determinism: 100%
```

**Edge Cases**
1. Single-server tool (no collision): Still require full name? - Policy decision
2. User muscle memory: Frequent errors for common operations
3. Documentation complexity: All examples must use full names

**Failure Modes**
1. **UX friction:** Always typing long names - HIGH FRICTION
2. **Verbosity:** 30+ character tool names for every call - MEDIUM FRICTION
3. **Documentation bloat:** Examples become unwieldy - LOW RISK

**Test Complexity: SIMPLE**
**Regression Risk: LOW**
**Determinism Rating: 10/10** (no ambiguity possible)

---

#### Option D: Priority-Based Routing

**Unit Tests (Medium)**
```
Test ID: D7Q6-D-U01
Description: Priority list for collision
Scenario: priority: ["ripgrep", "vector-search"], call "search"
Expected: Routes to ripgrep (higher priority)
Complexity: Medium
Determinism: 100% if config present
```

```
Test ID: D7Q6-D-U02
Description: No priority config
Scenario: No priority defined, call "search"
Expected: Error (no default priority)
Complexity: Medium
Determinism: 100% (fail-closed)
```

```
Test ID: D7Q6-D-U03
Description: Priority list missing server
Scenario: priority: ["ripgrep"], but memory also has "search"
Expected: memory.search not reachable via shorthand
Complexity: Medium
Determinism: 100%
```

**Integration Tests (Medium-Complex)**
```
Test ID: D7Q6-D-I01
Description: Project-scoped priority override
Scenario: Global: ripgrep first, Project: vector-search first
Expected: Project priority wins
Complexity: Medium
Determinism: 100%
Binding: D7-Q4
```

```
Test ID: D7Q6-D-I02
Description: Priority with layered config
Scenario: Global priority + project priority merged
Expected: Project takes full precedence (not merge)
Complexity: Complex
Determinism: Depends on merge semantics
```

**Edge Cases - MODERATE**
1. Priority list reordering: User may not realize "search" now means different tool
2. Empty priority list: Fallback behavior undefined
3. Priority for non-colliding tools: Over-specification
4. Tool removed from server: Priority points to missing tool

**Failure Modes**
1. **Silent behavior change:** Priority reorder changes tool without user noticing - MEDIUM RISK
2. **Config complexity:** Must maintain priority lists per collision - MEDIUM RISK
3. **Missing priority:** Fails open or closed? - Policy decision
4. **Merge confusion:** How do project priorities merge with global? - MEDIUM RISK

**Test Complexity: MEDIUM**
**Regression Risk: MEDIUM**
**Determinism Rating: 8/10** (deterministic if config complete, but merge semantics unclear)

---

### D7-Q6 Comparative Analysis

| Criterion | Option A | Option B | Option C | Option D |
|-----------|----------|----------|----------|----------|
| Test Count (est.) | 10 | 12 | 6 | 12 |
| Complexity | Medium | Simple-Medium | Simple | Medium |
| Regression Risk | **HIGH** | **LOW** | LOW | MEDIUM |
| Determinism | **3/10** | **10/10** | **10/10** | 8/10 |
| UX Friction | Medium | Low | **HIGH** | Low |
| Config Complexity | Low | Medium | None | Medium |
| Reproducibility | **POOR** | **EXCELLENT** | EXCELLENT | Good |
| D7-Q4 Compliance | Unclear | **NATURAL** | N/A | Needs merge rules |

### D7-Q6 Tester Agent Recommendation

**Recommended: Option B (Explicit aliasing)**
**Confidence: 8/10**

**Rationale:**
1. **100% Determinism:** Config file is single source of truth, reproducible across sessions
2. **User Control:** Users define their own shortcuts explicitly
3. **Layered Config Natural Fit:** Aliases integrate naturally with D7-Q4 layered config
4. **Graceful Degradation:** Without alias, full name still works
5. **Helpful Errors:** Can list all matching tools when alias not defined
6. **Zero Startup Race Conditions:** No timing-dependent behavior

**Design Requirements for Implementation:**
1. Aliases MUST be validated at config load time (target exists)
2. Circular alias detection MUST be implemented
3. Alias collision with full tool names MUST be rejected
4. Helpful error messages MUST list alternatives when shorthand fails

**Testing Concerns:**
- Must validate alias targets exist
- Circular alias detection needed
- Case sensitivity policy needed

**Confidence Deductions:**
- -1: Alias validation complexity (solvable)
- -1: Need to define case sensitivity policy

---

## Critical Test Cases Summary

### D7-Q5: Tool Naming Convention (Top 5)

| Test ID | Description | Critical Reason |
|---------|-------------|-----------------|
| D7Q5-A-U02 | Tool name with underscores | Proves unambiguous parsing |
| D7Q5-A-U03 | Server name with hyphens | Proves hyphen handling |
| D7Q5-A-I02 | Aggregator routing | Integration correctness |
| D7Q5-A-EC1 | Triple underscore in tool | Edge case boundary |
| D7Q5-A-SEC | Security validation | No injection possible |

### D7-Q6: Namespace Conflict Resolution (Top 5)

| Test ID | Description | Critical Reason |
|---------|-------------|-----------------|
| D7Q6-B-U03 | Layered config override | D7-Q4 integration |
| D7Q6-B-I01 | Helpful collision error | UX requirement |
| D7Q6-B-I03 | Alias validation | Prevent runtime errors |
| D7Q6-B-EC1 | Circular alias detection | Prevent infinite loops |
| D7Q6-B-EC2 | Alias-to-full-name collision | Namespace integrity |

---

## Risk Assessment

### Lowest Failure Risk Rankings

**D7-Q5:**
1. **Option A (9/10):** Trivial parsing, zero ambiguity, native pattern
2. **Option B (6/10):** Dot ambiguity with nested namespaces
3. **Option D (3/10):** Requires registry lookup, non-deterministic
4. **Option C (2/10):** Security risk with path traversal patterns

**D7-Q6:**
1. **Option B (9/10):** Config-driven, fully deterministic, user-controlled
2. **Option C (8/10):** Simple but high UX friction
3. **Option D (6/10):** Deterministic but merge semantics unclear
4. **Option A (3/10):** Startup order non-determinism is critical failure

---

## Determinism Ratings Summary

| Question | Option | Rating | Key Factor |
|----------|--------|--------|------------|
| Q5 | A | 10/10 | Fixed delimiter, trivial regex |
| Q5 | B | 6/10 | Ambiguous with 4+ segments |
| Q5 | C | 4/10 | Slashes in data cause ambiguity |
| Q5 | D | 2/10 | Requires registry lookup |
| Q6 | A | 3/10 | Startup order non-deterministic |
| Q6 | B | 10/10 | Config is source of truth |
| Q6 | C | 10/10 | No ambiguity possible |
| Q6 | D | 8/10 | Deterministic if merge rules clear |

---

## Test Infrastructure Requirements

### Required Test Fixtures

1. **Mock MCP Server Registry** - Simulate 26 servers with tool manifests
2. **Config Generator** - Create alias configs programmatically
3. **Collision Detector** - Identify tool name overlaps
4. **Parser Test Harness** - Test all naming patterns
5. **Round-Trip Validator** - Serialize/deserialize consistency

### Test Categories and Execution Strategy

| Category | Test Count | Execution Time | Run Frequency |
|----------|------------|----------------|---------------|
| Q5 Unit Tests | ~10 | < 30 sec | Every commit |
| Q5 Edge Cases | ~5 | < 30 sec | Every commit |
| Q6 Unit Tests | ~12 | < 30 sec | Every commit |
| Q6 Integration Tests | ~6 | 1-2 min | Every PR |
| Cross-Q5/Q6 Tests | ~4 | 1 min | Every PR |

### Suggested Test File Structure

```
tests/
  unit/
    mcp/
      test_tool_naming.py              # D7-Q5 parsing tests
      test_namespace_resolution.py     # D7-Q6 alias tests
  integration/
    mcp/
      test_tool_routing.py             # End-to-end routing
      test_alias_layered_config.py     # D7-Q4/Q6 integration
  fixtures/
    mock_server_registry.py
    alias_config_generator.py
```

---

## Cross-Question Test Matrix

Tests that validate both Q5 and Q6 decisions together:

```
Test ID: D7-CROSS-Q5Q6-01
Description: Alias uses full naming pattern
Scenario: aliases: {"search": "mcp__ripgrep__search"}
Expected: Alias value follows triple-underscore pattern
Complexity: Simple
Binding: Q5-A, Q6-B
```

```
Test ID: D7-CROSS-Q5Q6-02
Description: Parsing disambiguates collisions
Scenario: "mcp__playwright__click" vs "mcp__browsermcp__click"
Expected: Both parse correctly, no collision without alias
Complexity: Simple
Binding: Q5-A, Q6-B
```

```
Test ID: D7-CROSS-Q5Q6-03
Description: Alias validation uses correct parser
Scenario: aliases: {"click": "mcp.playwright.click"} (wrong pattern)
Expected: Validation error (alias target must use triple underscore)
Complexity: Medium
Binding: Q5-A, Q6-B
```

```
Test ID: D7-CROSS-Q5Q6-04
Description: Full name bypass with no alias
Scenario: No "click" alias defined, call "mcp__playwright__click" directly
Expected: Works correctly, no alias needed for full name
Complexity: Simple
Binding: Q5-A, Q6-B
```

---

## Summary

### D7-Q5: Tool Naming Convention
- **Recommendation:** Option A (Triple underscore `mcp__server__tool`)
- **Confidence:** 9/10
- **Test Complexity:** Simple (8 tests estimated)
- **Regression Risk:** LOW
- **Determinism:** 10/10
- **Key Strength:** 100% unambiguous parsing, Claude Code native

### D7-Q6: Namespace Conflict Resolution
- **Recommendation:** Option B (Explicit aliasing)
- **Confidence:** 8/10
- **Test Complexity:** Simple-Medium (12 tests estimated)
- **Regression Risk:** LOW
- **Determinism:** 10/10
- **Key Strength:** User-controlled, reproducible, D7-Q4 compatible

### Combined Implementation Notes

Both recommendations work synergistically:
- Triple underscore provides unambiguous full names
- Aliases provide user-friendly shortcuts to full names
- Layered config (D7-Q4) allows project-specific aliases
- Helpful errors list all options when shorthand fails
- No startup order dependencies, no race conditions

---

*Document generated by Tester Agent for BMad Decision Framework*
