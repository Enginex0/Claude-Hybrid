# D7: MCP Integration - Question Set

**Decision:** How does Claude-Hybrid integrate MCP servers and tools?
**Status:** PENDING (0/16 DECIDED)
**Generated:** 2025-12-10 (Updated 2025-12-11 - Removed 6 redundant questions)
**Sources:** Claude Code architecture (04-MCP-INTEGRATION.md), Claude-MPM analysis (07-MCP-TICKETING.md)

---

## Redundancy Audit Notes

The following questions were REMOVED due to semantic overlap with D2-D5:
- **Original Q10** (crash handling) → D2-Q5 decided Circuit-Breaker + Graceful Degradation applies system-wide
- **Original Q13** (schema caching) → D5-Q12/Q13/Q14 established hash-based caching architecture
- **Original Q14** (cache invalidation timing) → D5-Q13 decided hash-based invalidation with SHA-256
- **Original Q17** (hook interception) → D2-Q1/Q11 decided PreToolUse for all tool enforcement
- **Original Q19** (error integration) → D2-Q9/Q10 decided unified exception hierarchy + separate error recovery
- **Original Q20** (category enforcement) → D2-Q8/Q17/Q19 tiered enforcement (hard/soft) applies

---

## Checkpoint Status

| Question | Status | Answer |
|----------|--------|--------|
| Q1 | PENDING | - |
| Q2 | PENDING | - |
| Q3 | PENDING | - |
| Q4 | PENDING | - |
| Q5 | PENDING | - |
| Q6 | PENDING | - |
| Q7 | PENDING | - |
| Q8 | PENDING | - |
| Q9 | PENDING | - |
| Q10 | PENDING | - |
| Q11 | PENDING | - |
| Q12 | PENDING | - |
| Q13 | PENDING | - |
| Q14 | PENDING | - |
| Q15 | PENDING | - |
| Q16 | PENDING | - |

---

## Questions: MCP Aggregator Architecture (Q1-Q4)

### Q1: What aggregator architecture pattern should Claude-Hybrid use for MCP servers?
Options:
- A: Single aggregator proxy (Claude Code pattern: one aggregator spawns/routes to 26+ servers via stdio)
- B: Direct MCP connections (Claude-Hybrid connects directly to each MCP server without aggregator layer)
- C: Hybrid gateway (MPM-style internal gateway for custom tools + aggregator for external servers)
- D: Federated aggregators (multiple aggregator instances for different server categories: code analysis, browser, productivity)

### Q2: How should Claude-Hybrid handle the 26-server / 332-tool scale from the aggregator?
**NOTE:** D5-Q7 decided progressive disclosure for context management. This question applies that principle to MCP tools specifically.

Options:
- A: Full exposure (expose all 332 tools with unified namespace, let LLM discover and use as needed)
- B: Curated subset (pre-select essential tools, hide rarely-used ones to reduce context/confusion)
- C: Progressive disclosure (expose tools on-demand when specific capabilities are requested)
- D: Category-based activation (enable server categories like "code-analysis" or "browser" per task type)

### Q3: Should Claude-Hybrid spawn MCP servers on-demand or pre-warm them?
**NOTE:** D5-Q8 established session-boundary loading semantics. This question addresses MCP server process lifecycle specifically.

Options:
- A: On-demand spawning (Claude-MPM pattern: clean handoff, accept 11.9s first-call delay for vector-search)
- B: Pre-warming pool (spawn critical servers at session start, risk FD inheritance conflicts on execvpe)
- C: Hybrid warm-up (pre-warm fast servers like memory/ripgrep, on-demand for slow ones like code-graph-rag)
- D: Lazy initialization with keep-alive (spawn on first use, keep running for session duration with timeout)

### Q4: How should Claude-Hybrid manage aggregator configuration?
Options:
- A: Static config file (MPM pattern: ~/.claude/mcp-aggregator/config.json, require restart for changes)
- B: Dynamic runtime config (allow adding/removing servers without restart via control commands)
- C: Project-scoped config (.claude.json per project overrides global config for project-specific servers)
- D: Layered config (global defaults + project overrides + runtime modifications, merged at startup)

---

## Questions: Tool Namespacing Patterns (Q5-Q8)

### Q5: What tool naming convention should Claude-Hybrid enforce for MCP tools?
Options:
- A: Triple underscore pattern (mcp__server__tool - current aggregator pattern for clear namespace separation)
- B: Dot notation (mcp.server.tool - more readable but potential parsing ambiguity)
- C: Slash hierarchy (mcp/server/tool - URL-like, easy to filter by prefix)
- D: Flat with prefix (mcp_server_tool - simpler parsing, potential collision with underscored tool names)

### Q6: How should namespace conflicts be resolved when multiple servers offer similar tools?
Options:
- A: First-registered wins (server registered first owns the tool name, later registrations rejected)
- B: Explicit aliasing (require explicit aliases in config: "search" -> "ripgrep.search" vs "vector-search.search_code")
- C: Server-qualified only (always require full server.tool name, never allow shorthand)
- D: Priority-based routing (config defines server priority order, highest priority server handles ambiguous calls)

### Q7: Should Claude-Hybrid support tool aliasing for frequently-used MCP tools?
Options:
- A: No aliasing (always use full mcp__server__tool pattern for consistency and traceability)
- B: Config-defined aliases (allow ~/.claude/aliases.json to map short names to full tool paths)
- C: Auto-aliasing for unique tools (tools with unique names auto-aliased, conflicts require full path)
- D: Contextual aliasing (aliases scoped to current task/agent, e.g., "search" means different tools for different agents)

### Q8: How should tool discovery expose MCP capabilities to Claude?
**NOTE:** D5-Q9 decided manifest-based selective loading. This extends that pattern to MCP tool presentation.

Options:
- A: Full tool list at session start (list_servers + get_tools for all, high initial context cost)
- B: Summary only (server names + tool counts, full schemas fetched on-demand)
- C: Category-based discovery (tools grouped by function: "search", "memory", "browser", etc.)
- D: Intent-based discovery (Claude describes need, system recommends appropriate tools)

---

## Questions: Server Timeout Configuration and Lifecycle (Q9-Q12)

### Q9: What timeout strategy should Claude-Hybrid use for MCP server operations?
Options:
- A: Server-specific timeouts (code-graph-rag: 60min, vector-search: 10min, default: 2min - current pattern)
- B: Operation-type timeouts (indexing: 60min, search: 5min, CRUD: 30s - regardless of server)
- C: Adaptive timeouts (start with default, extend dynamically if operation shows progress)
- D: User-configurable timeouts (project config specifies timeout per server/operation type)

### Q10: What process lifecycle model should MCP servers follow?
Options:
- A: Per-call spawning (spawn server for each tool call, clean but slow)
- B: Session-scoped pooling (servers live for Claude session duration, managed by aggregator)
- C: Project-scoped persistence (servers persist across sessions for same project, faster warm starts)
- D: Background daemon (long-running MCP servers independent of Claude sessions, system service model)

### Q11: How should Claude-Hybrid manage stdio communication with MCP servers?
Options:
- A: Direct stdio pipes (aggregator spawns servers with stdin/stdout pipes, JSON-RPC over stdio)
- B: Unix socket abstraction (stdio wrapped in socket for better multiplexing and buffering)
- C: HTTP transport option (allow servers to expose HTTP endpoints as alternative to stdio)
- D: Mixed transport (stdio for local servers, HTTP/SSE for remote/cloud servers)

### Q12: How should Claude-Hybrid handle tool capability discovery for unknown servers?
Options:
- A: Strict registration (servers must be in config.json, unknown servers rejected)
- B: Dynamic discovery (allow runtime server registration via aggregator commands)
- C: Plugin model (servers self-register with capability manifest, aggregator validates)
- D: Sandbox discovery (new servers run in restricted mode until explicitly trusted)

---

## Questions: MCP Metadata and Hooks (Q13-Q14)

### Q13: What metadata should be cached alongside tool schemas?
Options:
- A: Schema only (tool name, parameters, returns - minimal footprint)
- B: Schema + examples (include usage examples for LLM context)
- C: Schema + performance hints (typical latency, resource usage, recommended batch size)
- D: Full capability profile (schema + examples + performance + dependencies + compatibility matrix)

### Q14: Should hooks be able to redirect MCP tool calls to alternative servers?
**NOTE:** D2-Q3 allows input modification via updatedInput. This question clarifies if redirection counts as input modification.

Options:
- A: No redirection (tool calls go to specified server only, hooks can only block/modify params)
- B: Fallback redirection (if primary server fails, hook can redirect to configured fallback)
- C: Policy-based routing (hooks can route based on rules: "search" -> ripgrep for fast, vector-search for semantic)
- D: Full routing control (hooks can redirect any call to any server, maximum flexibility)

---

## Questions: Gap Analysis Additions (Q15-Q16)

### Q15: How should Claude-Hybrid configure per-server MCP timeouts?
**Context:** MCP servers have vastly different operation times: code-graph-rag needs 60 min for large codebase indexing, vector-search needs 10 min for embedding generation, while standard operations complete in 2 min.

Options:
- A: Server-specific timeouts in config - Each server entry in config.json specifies its timeout value. Most flexible but requires per-server configuration.
- B: Operation-type timeouts - Define timeout by operation category (indexing: 60min, search: 5min, CRUD: 30s) regardless of which server performs it.
- C: Tiered defaults with override - Define 3 tiers (fast/medium/slow) with default assignments; servers can override in their config.
- D: Adaptive timeouts - Start with conservative default, automatically extend if server reports progress or partial results.

### Q16: How should Claude-Hybrid select between dual vector search systems?
**Context:** Claude-MPM runs TWO vector systems simultaneously: code-graph-rag (70MB SQLite, graph-based analysis) and mcp-vector-search (370MB ChromaDB, semantic embeddings). They serve different purposes.

Options:
- A: Automatic selection by query type - System analyzes query intent and routes to appropriate backend (graph for dependencies, semantic for concepts).
- B: Explicit tool selection - Expose both as separate tools; user/agent explicitly chooses which to invoke based on need.
- C: Primary with fallback - Designate one as primary (e.g., semantic); fall back to other if primary returns insufficient results.
- D: Unified facade - Single "search" tool that queries both backends and merges/ranks results before returning.

---

## Resume Instructions

**Next session:** Read this file, continue from first PENDING question.
**Methodology:** BMad Master facilitates, President decides each question.
**After completion:** Update ARCHITECTURAL-DECISIONS.md with D7 decision.

---

## Technical Reference

### Current MCP Architecture (from source documents)

```
26 MCP Servers, 332 Tools via Aggregator

Timeouts:
- code-graph-rag: 60 min (large codebase indexing)
- vector-search: 10 min (embedding generation)
- default: 2 min (standard operations)

Tool Naming: mcp__<server>__<tool>
Examples:
- mcp__sequential-thinking__sequentialthinking
- mcp__playwright__click
- mcp__memory__create_entities

Configuration: ~/.claude/mcp-aggregator/config.json
Cache Directory: ~/.claude/mcp-aggregator/servers/
```

### Server Categories

| Category | Servers | Tools |
|----------|---------|-------|
| Code Analysis | 6 | 97 |
| Browser & Web | 5 | 40 |
| File & Git | 3 | 73 |
| Database & Memory | 3 | 20 |
| IDE Integration | 2 | 17 |
| Testing & Security | 3 | 9 |
| Productivity | 4 | 76 |

### Key Architectural Decisions (from Claude-MPM)

1. **Warm-up disabled** - FD inheritance conflicts with execvpe()
2. **On-demand spawning** - Accept 11.9s first-call delay
3. **Two vector systems** - code-graph-rag (70MB SQLite) + mcp-vector-search (370MB ChromaDB)
4. **CRUD-only ticketing** - No workflow logic in mcp-ticketer, classification by LLM
