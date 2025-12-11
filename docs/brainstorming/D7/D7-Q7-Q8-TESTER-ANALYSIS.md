# D7-Q7 and D7-Q8: Tester Agent Validation Strategy

**Document Type:** Test Coverage Analysis & Recommendation
**Questions:** D7-Q7 (Tool Aliasing) and D7-Q8 (Tool Discovery)
**Status:** TESTER AGENT ANALYSIS COMPLETE
**Generated:** 2025-12-11

---

## Executive Summary

This document provides comprehensive testability analysis for D7-Q7 (Tool Aliasing) and D7-Q8 (Tool Discovery). Analysis includes test scenarios, determinism assessment, validation criteria, and test coverage estimates.

**Critical Context:**
- **9 verified tool name collisions** exist across 26 MCP servers (332 tools)
- **D7-Q5 DECIDED:** Triple underscore pattern (`mcp__server__tool`)
- **D7-Q6 DECIDED:** Priority-based routing with D5-Q18 shorthand

**Tester Agent Recommendations:**
- **D7-Q7:** Option C (Auto-alias unique tools) with confidence **8/10**
- **D7-Q8:** Option B (Summary only, schemas on-demand) with confidence **9/10**

---

## Part 1: D7-Q7 - Tool Aliasing

### Question Context

**Q7:** Should Claude-Hybrid support tool aliasing for frequently-used MCP tools?

**Options:**
- **A:** No aliasing (always use full `mcp__server__tool` pattern)
- **B:** Config-defined aliases (`~/.claude/aliases.json` maps short names to full paths)
- **C:** Auto-aliasing for unique tools (unique names auto-aliased, conflicts require full path)
- **D:** Contextual aliasing (aliases scoped to current task/agent)

### Binding Constraints Analysis

| Prior Decision | Constraint | Impact on Q7 |
|----------------|------------|--------------|
| **D7-Q5** | Triple underscore pattern | Aliases MUST resolve to `mcp__server__tool` format |
| **D7-Q6** | Priority-based routing + D5-Q18 shorthand | Q7 extends this: aliasing for unique tools |
| **D5-Q18** | Shorthand when unambiguous | Option C aligns naturally; Options A/B violate spirit |
| **D7-Q4** | Layered config | Config aliases (Option B) would need layer merge rules |

**Critical Finding:** D7-Q6 already decided "shorthand when unambiguous" via D5-Q18. This makes **Option C the logical continuation** - auto-alias is effectively "shorthand when unambiguous."

---

### Test Coverage by Option

#### Option A: No Aliasing

**Unit Tests (Minimal)**
```
Test ID: D7Q7-A-U01
Description: Verify full name required
Input: "search" (shorthand)
Expected: Error("Use full name: mcp__ripgrep__search")
Complexity: Simple
Determinism: 100%
```

```
Test ID: D7Q7-A-U02
Description: Full name accepted
Input: "mcp__ripgrep__search"
Expected: Routes to ripgrep server
Complexity: Simple
Determinism: 100%
```

**Test Count:** 4 unit tests
**Edge Cases:** None (no aliasing logic to test)
**Coverage Achievability:** 95%+ (trivial logic)

**Failure Modes:**
1. **UX friction:** Users must type 30+ char names - HIGH FRICTION
2. **Documentation bloat:** All examples need full names - LOW RISK

**Determinism Rating: 10/10** (no aliasing = no ambiguity)
**Regression Risk: LOW** (no new code)

**Problem:** Violates D5-Q18 spirit of "shorthand when unambiguous"

---

#### Option B: Config-Defined Aliases

**Unit Tests (Medium)**
```
Test ID: D7Q7-B-U01
Description: Config alias resolution
Config: aliases: {"search": "mcp__ripgrep__search"}
Input: "search"
Expected: Routes to mcp__ripgrep__search
Complexity: Simple
Determinism: 100%
```

```
Test ID: D7Q7-B-U02
Description: Multiple aliases to same tool
Config: aliases: {"find": "mcp__ripgrep__search", "grep": "mcp__ripgrep__search"}
Input: "find"
Expected: Routes to mcp__ripgrep__search
Complexity: Simple
Determinism: 100%
```

```
Test ID: D7Q7-B-U03
Description: Alias override in project config
Global: "search" -> ripgrep
Project: "search" -> vector-search
Input: "search" (in project context)
Expected: Routes to vector-search (per D7-Q4)
Complexity: Medium
Determinism: 100% (D7-Q4 defines precedence)
```

```
Test ID: D7Q7-B-U04
Description: Circular alias detection
Config: aliases: {"a": "b", "b": "a"}
Expected: Validation error at config load
Complexity: Medium
Determinism: 100%
```

```
Test ID: D7Q7-B-U05
Description: Alias to non-existent tool
Config: aliases: {"search": "mcp__invalid__tool"}
Expected: Validation error at config load
Complexity: Simple
Determinism: 100%
```

```
Test ID: D7Q7-B-U06
Description: Alias collision with full tool name
Config: aliases: {"mcp__ripgrep__search": "mcp__other__x"}
Expected: Validation error (cannot alias full names)
Complexity: Medium
Determinism: 100%
```

**Integration Tests (Medium)**
```
Test ID: D7Q7-B-I01
Description: Alias layered config merge
Scenario: Global aliases + project aliases
Expected: Project aliases override global
Complexity: Medium
Binding: D7-Q4
```

```
Test ID: D7Q7-B-I02
Description: Alias validation at startup
Scenario: Invalid alias in config
Expected: Startup fails with clear error
Complexity: Medium
```

**Test Count:** 10-12 tests
**Edge Cases:**
1. Circular aliases
2. Aliases to non-existent tools
3. Case sensitivity
4. Alias collision with full tool names
5. Layer merge conflicts

**Coverage Achievability:** 85-90%

**Failure Modes:**
1. **Config drift:** Manual aliases become stale - MEDIUM RISK
2. **Inconsistency:** Different users have different aliases - MEDIUM RISK
3. **Overhead:** Users must maintain alias configs - MEDIUM FRICTION

**Determinism Rating: 9/10** (config-driven, slight complexity from layering)
**Regression Risk: MEDIUM** (config validation logic needed)

**Problem:** Requires manual configuration; doesn't leverage D7-Q6's auto-shorthand

---

#### Option C: Auto-Aliasing for Unique Tools

**Unit Tests (Medium)**
```
Test ID: D7Q7-C-U01
Description: Auto-alias for unique tool
Scenario: Only ripgrep has "search" tool
Input: "search"
Expected: Routes to mcp__ripgrep__search
Complexity: Medium
Determinism: 100% (collision map is static)
```

```
Test ID: D7Q7-C-U02
Description: No alias for colliding tool
Scenario: Both ripgrep and vector-search have tools with "search" in name
Input: "search"
Expected: Error listing both options (per D7-Q6 priority-based resolution)
Complexity: Medium
Determinism: 100%
```

```
Test ID: D7Q7-C-U03
Description: Collision detection refresh
Scenario: New server adds "search" tool
Expected: Collision map updated, shorthand disabled for "search"
Complexity: High
Determinism: 100% (recompute on schema change)
```

```
Test ID: D7Q7-C-U04
Description: Priority-based resolution for collisions (D7-Q6)
Scenario: "click" collides between playwright/browsermcp, priority=[playwright]
Input: "click"
Expected: Routes to mcp__playwright__click
Complexity: Medium
Determinism: 100%
Binding: D7-Q6
```

```
Test ID: D7Q7-C-U05
Description: Full name always works
Input: "mcp__ripgrep__search" (full name for unique tool)
Expected: Routes to ripgrep (bypass alias)
Complexity: Simple
Determinism: 100%
```

**Integration Tests (Medium-Complex)**
```
Test ID: D7Q7-C-I01
Description: Collision map generation at startup
Scenario: Load all 26 servers, 332 tools
Expected: 9+ collisions detected, collision map accurate
Complexity: Complex
Determinism: 100% (static schema analysis)
```

```
Test ID: D7Q7-C-I02
Description: D7-Q6 priority integration
Scenario: Collision detected, priority config exists
Expected: Priority server wins, others require full name
Complexity: Medium
Determinism: 100%
Binding: D7-Q6
```

```
Test ID: D7Q7-C-I03
Description: Schema change invalidates collision map
Scenario: Server adds new tool during session
Expected: Warning logged, collision map remains until session restart
Complexity: High
Binding: D5-Q8 (session boundary), D6-Q2 (state death)
```

```
Test ID: D7Q7-C-I04
Description: Helpful error for ambiguous shorthand
Input: "search" (no priority defined, collision exists)
Expected: Error listing: mcp__ripgrep__search, mcp__vector-search__search_code, mcp__memory__search_nodes
Complexity: Medium
```

**Test Count:** 12-15 tests
**Edge Cases:**
1. Partial name match: "search" vs "search_code" vs "search_nodes"
2. Case sensitivity: "Search" vs "search"
3. Underscore in tool names: "search_code" auto-alias rules
4. New server registration mid-session
5. Server removal mid-session

**Coverage Achievability:** 85-90%

**Failure Modes:**
1. **Stale collision map:** Server changes not detected - LOW RISK (session boundary)
2. **Partial match ambiguity:** "search" matches multiple patterns - MEDIUM RISK (need exact match rule)
3. **User expectation:** Users expect aliases that aren't auto-generated - LOW RISK (helpful errors)

**Determinism Rating: 9/10** (collision map is deterministic from schema)
**Regression Risk: MEDIUM** (collision detection logic needs testing)

**Strength:** Natural extension of D7-Q6, no config overhead, deterministic

---

#### Option D: Contextual Aliasing (Agent-Scoped)

**Unit Tests (Complex)**
```
Test ID: D7Q7-D-U01
Description: Agent-specific alias
Scenario: Research agent: "search" -> vector-search; Engineer agent: "search" -> ripgrep
Input: "search" (Research agent context)
Expected: Routes to mcp__vector-search__search_code
Complexity: High
Determinism: Depends on agent context detection
```

```
Test ID: D7Q7-D-U02
Description: Context transition during session
Scenario: Switch from Research to Engineer agent
Expected: "search" meaning changes
Complexity: High
Determinism: 70% (context boundary detection)
```

```
Test ID: D7Q7-D-U03
Description: No agent context (direct call)
Input: "search" (no agent active)
Expected: Error or fallback behavior (undefined)
Complexity: High
Determinism: 50% (fallback policy unclear)
```

**Integration Tests (Complex)**
```
Test ID: D7Q7-D-I01
Description: Agent context propagation
Scenario: PM delegates to Research, tool call should use Research aliases
Expected: Research aliases active during delegation
Complexity: Very High
Binding: D2 (delegation model)
```

```
Test ID: D7Q7-D-I02
Description: Nested delegation alias handling
Scenario: PM -> Research -> sub-task
Expected: Alias context maintained through chain
Complexity: Very High
```

**Test Count:** 15-20 tests
**Edge Cases:**
1. Agent context undefined
2. Context transition mid-operation
3. Nested delegation context inheritance
4. Agent without alias config
5. Conflicting agent aliases

**Coverage Achievability:** 60-75% (contextual logic is complex)

**Failure Modes:**
1. **Context ambiguity:** When is context active? - HIGH RISK
2. **Debugging difficulty:** "search" means different things - HIGH RISK
3. **Non-reproducible bugs:** Same input, different output based on context - CRITICAL
4. **Testing complexity:** Must mock entire agent context - HIGH OVERHEAD

**Determinism Rating: 4/10** (context-dependent, hard to reproduce)
**Regression Risk: HIGH** (complex state management)

**Problem:** Too much hidden state, debugging nightmare, test complexity explosion

---

### D7-Q7 Comparative Analysis

| Criterion | Option A | Option B | Option C | Option D |
|-----------|----------|----------|----------|----------|
| Test Count | 4 | 10-12 | 12-15 | 15-20 |
| Test Complexity | Simple | Medium | Medium | **HIGH** |
| Coverage Achievability | 95%+ | 85-90% | 85-90% | **60-75%** |
| Regression Risk | LOW | MEDIUM | MEDIUM | **HIGH** |
| Determinism | 10/10 | 9/10 | **9/10** | **4/10** |
| D5-Q18 Compliance | **VIOLATES** | Partial | **FULL** | Unclear |
| D7-Q6 Integration | N/A | Manual | **NATURAL** | Complex |
| UX Friction | **HIGH** | Medium | **LOW** | Medium |
| Config Overhead | None | **HIGH** | None | Medium |

### D7-Q7 Recommendation

**Recommended: Option C (Auto-aliasing for unique tools)**
**Confidence: 8/10**

**Rationale:**
1. **D5-Q18 Compliant:** "Shorthand when unambiguous" is exactly auto-aliasing
2. **D7-Q6 Natural Extension:** Priority-based routing handles collisions
3. **Zero Config Overhead:** Works automatically, no user setup
4. **Deterministic:** Collision map computed from static schema
5. **Good UX:** Unique tools get shortcuts, collisions get helpful errors

**Test Strategy for Option C:**
1. **Collision Detection Tests:** Verify all 9 known collisions detected
2. **Auto-Alias Resolution Tests:** Unique tools resolve correctly
3. **Priority Integration Tests:** D7-Q6 priority routing works for collisions
4. **Error Message Tests:** Ambiguous calls produce helpful suggestions
5. **Edge Case Tests:** Partial matches, case sensitivity, special characters

**Confidence Deductions:**
- -1: Partial match ambiguity needs clear rules ("search" vs "search_code")
- -1: Schema change handling during session needs clarity

---

## Part 2: D7-Q8 - Tool Discovery

### Question Context

**Q8:** How should tool discovery expose MCP capabilities to Claude?

**Options:**
- **A:** Full tool list at session start (list_servers + get_tools for all)
- **B:** Summary only (server names + tool counts, schemas on-demand)
- **C:** Category-based discovery (tools grouped by function)
- **D:** Intent-based discovery (Claude describes need, system recommends)

### Binding Constraints Analysis

| Prior Decision | Constraint | Impact on Q8 |
|----------------|------------|--------------|
| **D7-Q2** | Progressive Disclosure (L1/L2/L3) | MANDATES progressive loading, NOT full upfront |
| **D5-Q7** | Progressive disclosure for context | Aligns with Option B/C, rules out Option A |
| **D5-Q9** | Manifest-based selective loading | Schema-on-demand pattern established |
| **D7-Q1** | Single aggregator | Discovery goes through aggregator |

**Critical Finding:** D7-Q2 already decided L1/L2/L3 progressive disclosure. Option A (full list) **VIOLATES** this binding constraint.

---

### Test Coverage by Option

#### Option A: Full Tool List at Session Start

**Unit Tests (Simple)**
```
Test ID: D7Q8-A-U01
Description: Load all tool schemas at startup
Expected: 332 tool schemas loaded
Complexity: Simple
Determinism: 100%
```

```
Test ID: D7Q8-A-U02
Description: Token budget consumed
Expected: ~325K tokens (per D7-Q2 analysis)
Complexity: Simple
Determinism: 100%
```

**Integration Tests (Simple)**
```
Test ID: D7Q8-A-I01
Description: Startup latency
Expected: 5-10 seconds loading all schemas
Complexity: Simple
```

**Test Count:** 4-6 tests
**Coverage Achievability:** 95%+ (simple logic)

**Failure Modes:**
1. **Token budget violation:** 325K tokens exceeds context limits - **CRITICAL**
2. **Startup latency:** 5-10 second delay unacceptable - HIGH FRICTION
3. **Schema staleness:** All schemas cached, changes not detected - MEDIUM RISK

**Determinism Rating: 10/10** (load everything = simple)
**Regression Risk: LOW** (no complex logic)

**DISQUALIFICATION:** Violates D7-Q2 binding constraint (progressive disclosure) and D5-Q7 (context efficiency)

---

#### Option B: Summary Only (Schemas On-Demand)

**Unit Tests (Medium)**
```
Test ID: D7Q8-B-U01
Description: L1 discovery (server names only)
Call: get_tools(detail="name")
Expected: 26 server names, ~200 tokens
Complexity: Simple
Determinism: 100%
```

```
Test ID: D7Q8-B-U02
Description: L2 discovery (summary with counts)
Call: get_tools(detail="summary")
Expected: Server names + tool counts + descriptions, ~6.6K tokens
Complexity: Simple
Determinism: 100%
```

```
Test ID: D7Q8-B-U03
Description: L3 discovery (full schema on-demand)
Call: get_tools(server="ripgrep", detail="full")
Expected: Full schema for ripgrep tools only
Complexity: Simple
Determinism: 100%
```

```
Test ID: D7Q8-B-U04
Description: Token budget verification
Scenario: L1 + selective L3 for 3 servers
Expected: < 20K tokens total
Complexity: Medium
Determinism: 100%
```

**Integration Tests (Medium)**
```
Test ID: D7Q8-B-I01
Description: On-demand schema fetch latency
Scenario: Request full schema for unused server
Expected: < 500ms fetch time
Complexity: Medium
```

```
Test ID: D7Q8-B-I02
Description: Schema caching after first fetch
Scenario: Request same schema twice in session
Expected: Second request uses cache
Complexity: Medium
Binding: D5-Q12/Q13/Q14 (hash-based caching)
```

```
Test ID: D7Q8-B-I03
Description: Stale schema detection
Scenario: Server schema changes, hash differs
Expected: Cache invalidated, fresh fetch
Complexity: Medium
Binding: D5-Q13 (SHA-256 invalidation)
```

```
Test ID: D7Q8-B-I04
Description: Discovery flow end-to-end
Scenario: Claude needs search capability
Flow: L1 -> identify ripgrep -> L3 for ripgrep
Expected: Correct schema, minimal token usage
Complexity: Medium
```

**Test Count:** 10-14 tests
**Edge Cases:**
1. Server unavailable during L3 fetch
2. Schema larger than expected (> 10K tokens)
3. Concurrent L3 requests for same server
4. L3 request for non-existent server

**Coverage Achievability:** 90%+

**Failure Modes:**
1. **Incomplete discovery:** Claude doesn't know server has relevant tool - MEDIUM RISK (L2 summaries help)
2. **Fetch latency:** On-demand fetch adds latency - LOW RISK (< 500ms)
3. **Cache coherence:** Stale cache serves old schema - LOW RISK (hash-based invalidation)

**Determinism Rating: 10/10** (L1/L2/L3 levels are well-defined)
**Regression Risk: LOW** (existing aggregator already supports this)

**Strength:** Already implemented per D7-Q2, proven token savings (97.96%)

---

#### Option C: Category-Based Discovery

**Unit Tests (Medium)**
```
Test ID: D7Q8-C-U01
Description: Category mapping
Expected: Tools grouped by function: search, memory, browser, etc.
Complexity: Medium
Determinism: 100% if mapping is static
```

```
Test ID: D7Q8-C-U02
Description: Category-level discovery
Call: get_tools(category="search")
Expected: ripgrep, vector-search, memory search tools
Complexity: Medium
```

```
Test ID: D7Q8-C-U03
Description: Tool in multiple categories
Scenario: "semantic_search" is both "search" and "code-analysis"
Expected: Appears in both category queries
Complexity: Medium
```

```
Test ID: D7Q8-C-U04
Description: Unknown category request
Call: get_tools(category="unknown")
Expected: Empty result or error
Complexity: Simple
```

**Integration Tests (Medium-Complex)**
```
Test ID: D7Q8-C-I01
Description: Category maintenance as servers added
Scenario: New server with new capability
Expected: Category mapping updated
Complexity: High
```

```
Test ID: D7Q8-C-I02
Description: Category hierarchy navigation
Flow: "search" -> "semantic-search" -> vector-search tools
Expected: Progressive narrowing works
Complexity: High
```

**Test Count:** 10-14 tests
**Edge Cases:**
1. Tool doesn't fit any category
2. New category needed for new server
3. Category granularity: too broad vs too narrow
4. Multi-category tools

**Coverage Achievability:** 75-85%

**Failure Modes:**
1. **Categorization drift:** New tools miscategorized - MEDIUM RISK
2. **Category explosion:** Too many categories become confusing - MEDIUM RISK
3. **Maintenance overhead:** Manual category assignment - HIGH OVERHEAD
4. **Incomplete mapping:** Tool missed from relevant category - MEDIUM RISK

**Determinism Rating: 7/10** (category mapping is subjective)
**Regression Risk: MEDIUM** (category maintenance is ongoing)

**Problem:** Category mapping is subjective, requires ongoing maintenance

---

#### Option D: Intent-Based Discovery

**Unit Tests (Complex)**
```
Test ID: D7Q8-D-U01
Description: Intent parsing
Input: "I need to search code"
Expected: Recommends ripgrep, vector-search
Complexity: High
Determinism: 50-70% (LLM-dependent)
```

```
Test ID: D7Q8-D-U02
Description: Ambiguous intent
Input: "I need to find something"
Expected: Asks clarifying question or lists options
Complexity: High
Determinism: 30-50% (interpretation varies)
```

```
Test ID: D7Q8-D-U03
Description: Intent with no matching tools
Input: "I need to translate Klingon"
Expected: "No matching tools found"
Complexity: Medium
Determinism: 80% (clear negative case)
```

**Integration Tests (Complex)**
```
Test ID: D7Q8-D-I01
Description: Intent recommendation accuracy
Scenario: 100 intent queries with known correct answers
Expected: 80%+ accuracy
Complexity: Very High
Determinism: Variable (LLM-dependent)
```

```
Test ID: D7Q8-D-I02
Description: Intent refinement loop
Flow: Vague intent -> clarification -> refined recommendation
Expected: Converges to correct tool
Complexity: Very High
```

**Test Count:** 10-15 tests
**Edge Cases:**
1. Ambiguous intent (multiple valid interpretations)
2. Intent with typos
3. Intent in non-English language
4. Compound intent (multiple needs in one query)
5. Intent that changes mid-conversation

**Coverage Achievability:** 60-75% (non-deterministic behavior)

**Failure Modes:**
1. **Recommendation accuracy:** Wrong tool recommended - **MEDIUM-HIGH RISK**
2. **Non-reproducible:** Same query, different recommendations - **CRITICAL for testing**
3. **Latency:** Intent processing adds delay - MEDIUM RISK
4. **Prompt engineering:** Intent parser needs tuning - HIGH OVERHEAD

**Determinism Rating: 4/10** (LLM-based, non-deterministic)
**Regression Risk: HIGH** (hard to test, hard to maintain)

**Problem:** Non-deterministic behavior makes testing very difficult

---

### D7-Q8 Comparative Analysis

| Criterion | Option A | Option B | Option C | Option D |
|-----------|----------|----------|----------|----------|
| Test Count | 4-6 | 10-14 | 10-14 | 10-15 |
| Test Complexity | Simple | Medium | Medium-High | **HIGH** |
| Coverage Achievability | 95%+ | **90%+** | 75-85% | **60-75%** |
| Regression Risk | LOW | **LOW** | MEDIUM | **HIGH** |
| Determinism | 10/10 | **10/10** | 7/10 | **4/10** |
| D7-Q2 Compliance | **VIOLATES** | **FULL** | Partial | Partial |
| Token Efficiency | **FAILS** | **97.96%** | ~90% | Variable |
| Implementation | 0 LOC | **0 LOC** | ~500 LOC | ~1000 LOC |

### D7-Q8 Recommendation

**Recommended: Option B (Summary only, schemas on-demand)**
**Confidence: 9/10**

**Rationale:**
1. **D7-Q2 Binding:** Already decided L1/L2/L3 progressive disclosure
2. **Already Implemented:** Aggregator `get_tools(detail=name|summary|full)` exists
3. **Proven Token Savings:** 97.96% reduction (6.6K vs 325K tokens)
4. **100% Deterministic:** Well-defined levels, reproducible behavior
5. **Low Regression Risk:** Existing implementation, just needs tests

**Test Strategy for Option B:**
1. **Token Budget Tests:** Verify L1/L2/L3 stay within limits
2. **Schema Freshness Tests:** Hash-based invalidation works (D5-Q13)
3. **On-Demand Latency Tests:** L3 fetch < 500ms
4. **Cache Coherence Tests:** Stale schemas detected and refreshed
5. **End-to-End Discovery Tests:** Claude finds relevant tools efficiently

**Confidence Deductions:**
- -1: Need to verify L3 fetch latency under load

---

## Critical Test Scenarios Summary

### D7-Q7: Tool Aliasing - Top 5 Critical Tests

| Test ID | Scenario | Risk Mitigated | Priority |
|---------|----------|----------------|----------|
| D7Q7-C-U01 | Auto-alias unique tool | Unique tools get shortcuts | P0 |
| D7Q7-C-I01 | Collision map generation | All 9 collisions detected | P0 |
| D7Q7-C-U04 | Priority-based collision | D7-Q6 integration verified | P0 |
| D7Q7-C-I04 | Helpful error for ambiguous | User gets clear guidance | P1 |
| D7Q7-C-U02 | No alias for collision | Collisions require full path | P1 |

### D7-Q8: Tool Discovery - Top 5 Critical Tests

| Test ID | Scenario | Risk Mitigated | Priority |
|---------|----------|----------------|----------|
| D7Q8-B-U04 | Token budget verification | Context window not exceeded | P0 |
| D7Q8-B-I03 | Stale schema detection | Hash invalidation works | P0 |
| D7Q8-B-U01 | L1 discovery | Server list loads correctly | P0 |
| D7Q8-B-I04 | Discovery flow E2E | Complete workflow works | P1 |
| D7Q8-B-I01 | On-demand latency | L3 fetch acceptable (<500ms) | P1 |

---

## Test Coverage Estimates

### D7-Q7 (Option C): Auto-Aliasing

| Test Category | Count | Complexity | Coverage |
|---------------|-------|------------|----------|
| Unit Tests | 8 | Medium | 85% |
| Integration Tests | 5 | Medium-High | 80% |
| Edge Cases | 4 | Medium | 75% |
| **Total** | **17** | **Medium** | **83%** |

### D7-Q8 (Option B): Summary Only

| Test Category | Count | Complexity | Coverage |
|---------------|-------|------------|----------|
| Unit Tests | 6 | Simple-Medium | 95% |
| Integration Tests | 5 | Medium | 90% |
| Edge Cases | 3 | Medium | 85% |
| **Total** | **14** | **Medium** | **90%** |

---

## Determinism Ratings Summary

| Question | Option | Rating | Key Factor |
|----------|--------|--------|------------|
| **Q7** | A | 10/10 | No aliasing = no ambiguity |
| **Q7** | B | 9/10 | Config-driven, slight layer complexity |
| **Q7** | **C** | **9/10** | **Collision map deterministic from schema** |
| **Q7** | D | 4/10 | Context-dependent, hard to reproduce |
| **Q8** | A | 10/10 | Load everything (but VIOLATES D7-Q2) |
| **Q8** | **B** | **10/10** | **Well-defined L1/L2/L3 levels** |
| **Q8** | C | 7/10 | Category mapping subjective |
| **Q8** | D | 4/10 | LLM-based, non-deterministic |

---

## Validation Criteria for Correctness

### D7-Q7: Auto-Aliasing Correctness

1. **Collision Detection Accuracy:** All 9+ known collisions must be detected
   - browser_click (playwright, browsermcp)
   - read_file (filesystem, wcgw)
   - write_file (filesystem, wcgw)
   - navigate (playwright, browsermcp)
   - screenshot (playwright, browsermcp)
   - query (sqlite, code-graph-rag)
   - search variants (ripgrep, vector-search, memory)
   - click (playwright, browsermcp)
   - create_* variants (memory, sqlite, mcp-ticketer)

2. **Resolution Determinism:** Same input MUST produce same output
3. **Priority Compliance:** D7-Q6 priority routing must be respected
4. **Error Quality:** Ambiguous calls must list all options

### D7-Q8: Discovery Correctness

1. **Token Budget:** L1 < 500 tokens, L2 < 10K tokens per session start
2. **Schema Freshness:** Hash change triggers refresh within session boundaries
3. **Latency:** L3 on-demand fetch < 500ms
4. **Completeness:** All 26 servers, 332 tools discoverable through L1->L2->L3

---

## Risk Assessment

### D7-Q7 Option C Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Partial match ambiguity | Medium | Medium | Define exact-match-only rule |
| Schema change mid-session | Low | Low | D5-Q8 session boundary protects |
| New collision undetected | Low | Medium | Recompute collision map on schema refresh |

### D7-Q8 Option B Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| L3 fetch timeout | Low | Medium | 30s timeout with graceful degradation |
| Stale schema used | Low | Low | Hash-based invalidation (D5-Q13) |
| Server unavailable | Medium | Medium | Retry + fallback to cached schema |

---

## Final Recommendations

### D7-Q7: Tool Aliasing

**Recommendation:** Option C (Auto-aliasing for unique tools)
**Confidence:** 8/10

**Implementation Requirements:**
1. Collision map computed at session start from all server schemas
2. Unique tools auto-aliased (shorthand allowed)
3. Colliding tools require full path OR D7-Q6 priority routing
4. Helpful error messages list all options for ambiguous calls

### D7-Q8: Tool Discovery

**Recommendation:** Option B (Summary only, schemas on-demand)
**Confidence:** 9/10

**Implementation Requirements:**
1. L1/L2/L3 levels already exist in aggregator - verify tests
2. Token budget tests to ensure compliance
3. Hash-based cache invalidation (D5-Q13) integration tests
4. On-demand latency verification

---

## Test Infrastructure Requirements

### Required Test Fixtures

1. **Mock MCP Server Registry** - 26 servers, 332 tools with known collisions
2. **Collision Map Generator** - Compute expected collisions from fixtures
3. **Token Counter** - Verify token budgets at each level
4. **Schema Version Generator** - Create schema variants for staleness tests

### Test File Structure

```
tests/
  unit/
    mcp/
      test_tool_aliasing.py           # D7-Q7 auto-alias tests
      test_tool_discovery.py          # D7-Q8 L1/L2/L3 tests
      test_collision_detection.py     # 9 collision verification
  integration/
    mcp/
      test_alias_resolution.py        # E2E alias -> full name
      test_discovery_flow.py          # L1 -> L2 -> L3 workflow
      test_token_budget.py            # Budget verification
  fixtures/
    mock_server_registry.py
    collision_fixtures.py
    schema_generators.py
```

---

*Document generated by Tester Agent for BMad Decision Framework*
