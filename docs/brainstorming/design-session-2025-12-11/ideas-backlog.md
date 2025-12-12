# Claude-Hybrid Ideas Backlog

**Purpose:** Capture raw ideas, questions, and explorations for the brainstorming session.
**Status:** Living document - add ideas freely, refine later.

---

## How to Use This File

1. **Add ideas freely** - No judgment, capture everything
2. **Tag with priority** - [HIGH], [MEDIUM], [LOW], or [EXPLORE]
3. **Move to decisions-log.md** when idea becomes confirmed decision
4. **Archive** ideas that are rejected (don't delete, move to bottom)

---

## President's Questions Queue

*Add your questions here - we'll work through them together*

### Pending Questions

1. [ ] ...
2. [ ] ...
3. [ ] ...

### Answered Questions

*Move questions here after discussion with link to decision*

- (none yet)

---

## Raw Ideas to Explore

### Architecture Ideas

- [DECIDED] Unified Agent Template v3.0 → See D12 in decisions-log.md
- [DECIDED] Agent Routing via L1 Aggregation → See D13 in decisions-log.md
- [DECIDED] Unified-Agent-Builder Workflow → See D14 in decisions-log.md
- [CRITICAL] **REVIEW D1-D14** with new claude-mpm architecture understanding (Session 6 finding)
- [CRITICAL] Clarify Orchestrator-master delivery mechanism (NOT --append-system-prompt)
- [BLOCKED] Agent tiering strategy for 87-agent rebuild (blocked by D1-D14 review)

### Implementation Ideas

- [HIGH] Start Tier 1 agent rebuilds as proof-of-concept
- [MEDIUM] Create agent template linter/validator tool
- [EXPLORE] Automated migration script BMAD → Unified

### Optimization Ideas

- [EXPLORE] Token counting for rebuilt agents to validate budget targets

### Integration Ideas

- [EXPLORE] PM routing validation with rebuilt agents

---

## Questions from Previous Sessions

*Captured from the architecture plan*

1. **Tech Stack Decision:** Python (claude-mpm style) or hybrid with Node.js?
   - Status: [PENDING]

2. **MCP Gateway:** Port existing from claude-mpm or fresh implementation?
   - Status: [PENDING]

3. **Priority:** Start with MCP foundation or Control Layer?
   - Status: [PENDING]

4. **Advisory Pattern:** Exact format for routing hints?
   - Status: [PENDING]

5. **Testing Strategy:** Port claude-mpm's 1513+ tests?
   - Status: [PENDING]

---

## Potential Challenges to Address

*Things that might be tricky*

1. **os.execvpe() state handoff** - How exactly does frontmatter get passed to new process?
2. **Hook execution timing** - PreToolUse must be fast (<10ms)
3. **Circuit Breaker ordering** - CB#1-CB#8 priority?
4. **Token counting accuracy** - What if Anthropic API is slow?
5. **Cross-session context** - What's essential to persist in KuzuMemory?

**NEW FROM SESSION 6 INVESTIGATION:**

6. **Orchestrator delivery mechanism** - claude-mpm uses --append-system-prompt (wrapper pattern), but Claude-Hybrid is in-process. How do we deliver orchestrator instructions?
7. **--agents flag limitation** - 50K char limit means ~40 agents max. D13's file-based approach is better for 87 agents.
8. **Wrapper vs In-Process architecture** - claude-mpm patterns can't be directly copied because Claude-Hybrid is NOT a wrapper.
9. **D1-D14 alignment check** - Do existing decisions account for the actual claude-mpm architecture?

---

## Inspiration / References

*Links, examples, patterns to consider*

- claude-mpm MCP Gateway: `/home/president/bmad-systems/claude-mpm/src/claude_mpm/services/mcp_gateway/`
- BMAD workflows: `/home/president/bmad-systems/.bmad/`
- D1-D10 session roundups: `/home/president/bmad-systems/Claude-Hybrid/docs/brainstorming/`

---

## Archived Ideas (Rejected/Superseded)

*Don't delete ideas - move them here with reason*

- (none yet)

---

## Quick Capture

*Dump quick thoughts here, organize later*

```
[Timestamp] [Idea]
```

---

*Backlog maintained by President + Claude*
