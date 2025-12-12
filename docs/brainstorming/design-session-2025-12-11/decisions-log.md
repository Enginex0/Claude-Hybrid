# Claude-Hybrid Architecture Decisions Log

**Purpose:** Detailed record of all architectural decisions with full rationale.
**Status:** Living document - updated as decisions are made.

---

## Decision Format

Each decision follows this structure:
- **ID:** Unique identifier (D1, D2, etc.)
- **Decision:** What was decided
- **Context:** Why this decision was needed
- **Rationale:** Why this choice over alternatives
- **Alternatives Rejected:** What we didn't do and why
- **Consequences:** What this enables/constrains
- **Date:** When decided

---

## D1: MCP is Data Plane, Not Control Plane

**Decision:** MCP tools cannot control Claude's routing decisions - they can only provide data that Claude interprets.

**Context:** We needed to understand if MCP could be used to control agent routing, workflow execution, and skill selection in Claude-Hybrid.

**Rationale:**
- MCP protocol is fundamentally request-response data exchange
- Claude interprets tool responses - tools cannot force behavior
- There's NO mechanism in MCP to override Claude's reasoning
- 4 specialized agents researched this and confirmed the limitation

**Alternatives Rejected:**
- Attempting to use MCP for control → Would fail silently, Claude would ignore
- Building custom control protocol → Unnecessary complexity, Claude Code already has Task tool

**Consequences:**
- Control logic MUST stay in-process (PM Instructions, Hooks, Circuit Breakers)
- MCP used for services only (data, summaries, memory)
- Advisory Pattern is the optimal influence mechanism

**Date:** 2025-12-11

---

## D2: Control Layer Stays In-Process

**Decision:** Hooks, Circuit Breakers, PM Agent, and Workflow Engine are implemented as in-process Python modules, never as MCPs.

**Context:** Critical path operations need 99.9% reliability. Network dependencies introduce failure modes.

**Rationale:**
- Zero network dependency = zero network failure modes
- In-process = microsecond latency, not millisecond
- No MCP server startup time
- No JSON serialization overhead on hot path
- If hooks fail, security/validation fails - unacceptable risk

**Alternatives Rejected:**
- Hooks via MCP → Network failure = security bypass
- Circuit Breakers via MCP → Network failure = rules ignored
- Hybrid approach → Complexity without benefit

**Consequences:**
- Control layer code lives in Claude-Hybrid Python package
- Can be unit tested directly (no MCP mocking needed)
- ~3,310 LOC for hooks system from claude-mpm (reusable)

**Date:** 2025-12-11

---

## D3: State Lives in Files (Frontmatter SSOT)

**Decision:** Workflow state is stored in frontmatter of workflow files. This is the Single Source of Truth (SSOT). MCP and external systems sync FROM this, never TO.

**Context:** When Claude Code spawns a Task agent via os.execvpe(), the process image is completely replaced. Memory is wiped. Only files survive.

**Rationale:**
- os.execvpe() is Unix physics - processes die, files persist
- Frontmatter is human-readable and git-trackable
- No database dependency for core state
- Resume from any point by reading the file
- Works even if all MCPs are down

**Alternatives Rejected:**
- Database SSOT → Adds dependency, doesn't survive process boundary
- MCP-based state → Network dependency on critical path
- In-memory only → Lost on process death

**Consequences:**
- Frontmatter ALWAYS wins on conflict with external systems
- External systems (Jira, KuzuMemory) are secondary
- State recovery is guaranteed - just read the file

**Date:** 2025-12-11

---

## D4: No MCP Merging - Stay Independent

**Decision:** Existing MCPs (KuzuMemory, Sequential-Thinking, Serena, etc.) remain completely independent. Claude-Hybrid does NOT merge them into a single entity.

**Context:** User was concerned about potential merging of MCPs into claude-mpm or a single mega-MCP.

**Rationale:**
- Each MCP has its own lifecycle and maintainer
- Merging creates coupling and deployment complexity
- Independent MCPs can fail independently (graceful degradation)
- MCP Aggregator already provides single-endpoint access without merging
- Clean architecture = loose coupling

**Alternatives Rejected:**
- Merge all into one MCP → Monolith, single point of failure
- Fork and modify existing MCPs → Maintenance nightmare
- Embed MCP logic into Claude-Hybrid → Violates separation of concerns

**Consequences:**
- KuzuMemory stays KuzuMemory
- Sequential-Thinking stays Sequential-Thinking
- Claude-Hybrid CALLS these when needed
- Claude-Hybrid's own services (TokenCounter, etc.) are in-process Python

**Date:** 2025-12-11

---

## D5: 3-Layer Architecture

**Decision:** Claude-Hybrid uses a strict 3-layer architecture:
- Layer 1: CONTROL (in-process, 99.9% reliable)
- Layer 2: STATE (file-based, survives process death)
- Layer 3: SERVICES (external MCPs, failure-tolerant)

**Context:** Need clear separation of concerns with different reliability requirements.

**Rationale:**
- Each layer has distinct failure characteristics
- Layer 1 failures are catastrophic → maximize reliability
- Layer 2 failures lose state → use most reliable medium (files)
- Layer 3 failures reduce capability → design for graceful degradation
- Clear mental model for developers

**Alternatives Rejected:**
- Flat architecture → No clear reliability boundaries
- 2-layer (control + everything else) → Conflates state and services
- Microservices everything → Over-engineering for this use case

**Consequences:**
- Every component has a clear layer assignment
- Layer violations are architectural bugs
- New features must specify their layer

**Date:** 2025-12-11

---

## D6: Advisory Pattern for MCP Influence

**Decision:** MCPs can return advisory hints (suggested_agent, suggested_skills, confidence) that Claude CONSIDERS but doesn't blindly follow.

**Context:** Since MCP can't control Claude, we needed an influence mechanism.

**Rationale:**
- Respects MCP's true nature (data provider)
- PM_INSTRUCTIONS.md teaches Claude to consider high-confidence hints
- Expected 70-90% compliance when advisory aligns with context
- Claude maintains final decision authority
- No silent failures - if Claude ignores hint, task still completes

**Alternatives Rejected:**
- Force compliance via prompt injection → Unreliable, hackish
- Ignore MCP for routing entirely → Lose useful intelligence
- Strict rules based on MCP response → Too rigid, context matters

**Consequences:**
- Advisory format standardized: {suggested_agent, suggested_skills, reasoning, confidence}
- PM_INSTRUCTIONS.md includes: "CONSIDER when confidence > 0.7"
- Metrics: track advisory compliance rate

**Date:** 2025-12-11

---

## D7: Graceful Degradation Requirement

**Decision:** Every MCP must pass the test: "If this MCP is unavailable, does Claude-Hybrid still function?"

**Context:** Network services fail. MCPs crash. We need resilience.

**Rationale:**
- Production systems experience failures
- Users shouldn't see errors for non-critical features
- Reduced capability > complete failure
- Forces good architecture (critical path never depends on MCP)

**Alternatives Rejected:**
- Assume MCPs always work → Fragile system
- Retry loops with backoff → Delays user, doesn't solve root cause
- Failover to backup MCPs → Complexity, still a dependency

**Consequences:**
- TokenCounter: API → tiktoken → char estimate (always works)
- DocumentSummarizer: MCP → Claude reads full file (slower but works)
- KuzuMemory: session works, cross-session lost (acceptable)
- Any MCP failing this test → moved to in-process

**Date:** 2025-12-11

---

## D8: Break-Even Gate for New MCPs

**Decision:** Before adding any MCP, calculate: `savings > overhead × 1.5`. If not, embed in system prompt instead.

**Context:** MCP calls have token overhead (~150-500 tokens). Need to ensure net positive.

**Rationale:**
- Prevents token-burning MCPs from creeping in
- Quantitative gate, not subjective
- 1.5x safety margin accounts for variance
- Forces justification for every MCP

**Alternatives Rejected:**
- Add MCPs freely → Token budget bloat
- Subjective "seems useful" → Inconsistent decisions
- No gate, optimize later → Technical debt

**Consequences:**
- Each MCP proposal requires token math
- Low-value MCPs rejected or embedded in prompt
- High-value MCPs (like DocumentSummarizer: 373x ROI) easily pass

**Date:** 2025-12-11

---

## D9: Progressive Disclosure (L1→L2→L3)

**Decision:** Load agent/skill information progressively:
- L1 (ALWAYS): Metadata only (~100 tokens)
- L2 (ON ACTIVATION): Core content (~2,000 tokens)
- L3 (ON DEMAND): Deep references (via Read tool)

**Context:** Loading 50 agents × 2,000 tokens = 100K tokens upfront is wasteful.

**Rationale:**
- 98.7% token reduction (Anthropic validated)
- Load only what's needed
- Matches D5/D7 from original architectural decisions
- Most agents never activated in a session

**Alternatives Rejected:**
- Load everything upfront → Token budget exhausted
- Load nothing, discover on demand → Poor routing decisions
- Binary load/no-load → Misses the metadata optimization

**Consequences:**
- Agent registry stores L1 metadata
- L2 loaded when Claude mentions agent
- L3 loaded only on explicit deep-dive requests

**Date:** 2025-12-11

---

## D10: Session Tracking - File Primary, Kuzu Secondary

**Decision:** Track design session progress using file-based tracker as SSOT, with optional KuzuMemory sync for cross-session search.

**Context:** Long brainstorming sessions need continuity across context limits.

**Rationale:**
- Applies our own Principle 2 ("State Lives in Files")
- Files are transparent, version-controllable, human-readable
- KuzuMemory adds semantic search without being critical
- New Claude session can read file → instant context

**Alternatives Rejected:**
- KuzuMemory only → Opaque, can't manually inspect
- SQLite → Over-engineering for this use case
- Memory MCP only → Less persistent than files

**Consequences:**
- SESSION-TRACKER.md is the resume file
- Update before each /compact or /clear
- Simple one-liner to resume: "Read [path to tracker]"

**Date:** 2025-12-11

---

## Template for New Decisions

```markdown
## DXX: [Decision Title]

**Decision:** [What was decided]

**Context:** [Why this decision was needed]

**Rationale:**
- [Reason 1]
- [Reason 2]

**Alternatives Rejected:**
- [Alternative 1] → [Why rejected]

**Consequences:**
- [What this enables/constrains]

**Date:** YYYY-MM-DD
```

---

*Log maintained by Claude | Total Decisions: 10 (D1-D10) | Total Questions: 162*
