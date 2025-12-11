# D1: Execution Model - Question Set

**Decision:** What execution model should Claude-Hybrid use?
**Status:** ✅ COMPLETE (1/1 DECIDED)
**Generated:** 2025-12-07 (Updated 2025-12-11)
**Sources:** CORE-VISION.md, ARCHITECTURAL-DECISIONS.md

---

## Checkpoint Status

| Question | Status | Answer |
|----------|--------|--------|
| Q1 | **DECIDED** | Option C: Hybrid Model (Config Deployer + Runtime Orchestrator) |

---

## Questions: Execution Model Selection (Q1)

### Q1: Should Claude-Hybrid use Config Deployer, Runtime Orchestrator, or Hybrid Model?
**Context:** Three architectural patterns for Claude-Hybrid initialization and runtime control:
1. **Config Deployer pattern** - Upfront configuration deployment, no runtime orchestration. Once deployed, Claude Code runs independently.
2. **Runtime Orchestrator pattern** - Continuous runtime control via an external orchestrator process monitoring and managing Claude Code execution.
3. **Hybrid Model** - Combines upfront configuration with optional runtime orchestration. Orchestrator is a Claude Code agent (BMad Master), not an external process.

Options:
- A: Pure Config Deployer - Deploy all configuration, agents, skills, hooks, MCP config upfront. No runtime orchestration. Simple, lightweight, but less flexible control.
- B: Pure Runtime Orchestrator - External orchestrator process continuously monitors and controls Claude Code. Maximum control but more complex, higher overhead, potential single point of failure.
- C: Hybrid Model - Combine Config Deployer upfront deployment with optional Runtime Orchestrator as Claude Code agent. User can invoke/dismiss orchestrator as needed. Balances simplicity with flexible control. Leverages Claude Code's native agent model.
- D: Dynamic switching - Start with Config Deployer, allow runtime upgrade to Orchestrator if needed. Complex state transition management but maximum flexibility.

**Decision Rationale:**
The Hybrid Model (Option C) was chosen because it:
- Combines upfront configuration (project-specific tailoring) with runtime orchestration (continuous control)
- Implements orchestrator as Claude Code agent (BMad Master), not external process - native to the platform
- Maintains the "know every wire" principle while providing flexibility
- Allows user to invoke/dismiss orchestrator as needed
- Reduces complexity compared to pure external orchestrator patterns
- Better leverages Claude Code's native multi-agent capabilities

**Architectural Pattern:**
- **Layer 1 (Static):** Deploy agents, skills, hooks, MCP config upfront
- **Layer 2 (Runtime):** Orchestrator agent (BMad Master) invokable during session
- **Process Model:** Orchestrator is Claude Code agent, NOT external process
- **Control Model:** User can invoke/dismiss orchestrator as needed

**Binding Constraints:**
- D2 (Enforcement Mechanism) depends on this execution model choice
- D3 (Multi-Agent Strategy) depends on enforcement mechanism
- D4 (State Tracking) depends on agent model

---

## Resume Instructions

**Next session:** This decision is complete. Move to D2 (Enforcement Mechanism).
**Methodology:** BMad Master facilitates, President decides each question.
**After completion:** Ensure ARCHITECTURAL-DECISIONS.md reflects D1 decision.
