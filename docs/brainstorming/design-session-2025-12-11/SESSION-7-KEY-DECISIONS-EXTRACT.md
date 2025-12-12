# Session 7: Key Decisions Already Made (D1-D10 Extract)

**Date:** 2025-12-12
**Purpose:** Extract specific decisions from D1-D10 for re-evaluation of approach
**Status:** Reference document for next session

---

## Total Decision Count: 159 Questions Across D1-D10

| Decision Set | Questions | Topic |
|--------------|-----------|-------|
| D1 | 1 | Execution Model |
| D2 | 20 | Enforcement Mechanism |
| D3 | 20 | Multi-Agent Strategy |
| D4 | 20 | State Tracking |
| D5 | 20 | Context Management (Progressive Disclosure) |
| D6 | 18 | Process Boundaries & Initialization |
| D7 | 16 | MCP Integration |
| D8 | 14 | Plugin & Agent Format |
| D9 | 16 | Path Variables & File Structure |
| D10 | 14 | Workflow Engine & Lifecycle |

---

## 1. AGENT TIERING SYSTEMS (Already Decided)

### D3-Q1: Agent Selection Tiering
**Decision:** Option E - Tiered Hybrid Selection
- **TIER 1:** User-Directed (explicit user choice)
- **TIER 2:** Scenario-Based ~80% (pre-configured groups)
- **TIER 3:** Intelligent Scoring ~15% (AI analysis)
- **TIER 4:** Rotation Modifier ~5% (balanced participation)

### D3-Q6: Sub-Agent Invocation Tiering
**Decision:** Option E - Tiered Hybrid Sub-Agent Invocation
- **TIER 1:** User-Directed (explicit invocation)
- **TIER 2:** Orchestrator-Validated for critical operations
- **TIER 3:** Proactive Trigger Matching with guards
- **TIER 4:** Injection Hints (workflow definitions)

### D3-Q7: Agent Role Hierarchy
**Decision:** Option D - Tiered Role-Based Specialization
- **4-tier hierarchy:** Orchestrator > Phase Leads > Role Specialists > Sub-Agents
- **Optimal:** 25-30 total agents (coordination overhead scales quadratically >50)

### D3-Q14: Agent Persona Authority
**Decision:** Option D - Hierarchical Persona Authority
- Role-based tier hierarchy for conflict resolution
- Prevents $47K infinite loop incidents

### D3-Q15: Agent Availability Scope
**Decision:** Option E - Project Configuration with Sensible Defaults
- **TIER 1:** All agents available by default (zero-config)
- **TIER 2:** Optional project config for scoping
- **TIER 3:** Runtime discovery enhancement

### D5-Q6: Skill/Agent Loading Priority
**Decision:** Option A - Project > User > Bundled priority
- Project skills override user override bundled

### D8-Q6: Permission Modes
**Decision:** Option B - Tiered (default/elevated/bypass)
- Maps to Hard/Soft enforcement: default=HARD, elevated=SOFT, bypass=NONE

---

## 2. ORCHESTRATOR/PM DESIGN (Already Decided)

### D1-Q1: Execution Model
**Decision:** Option C - Hybrid Model
- **Layer 1 (Static):** Deploy agents, skills, hooks, MCP config upfront
- **Layer 2 (Runtime):** Orchestrator agent (BMad Master) invokable during session
- Orchestrator IS Claude Code agent, NOT external process

### D2-Q2: Hook Priority Structure
**Decision:** Option C - Orchestrator Semantic Grouping
- **P10:** Initialization (highest priority)
- **P20:** Enforcement
- **P50:** Business logic
- **P80:** Audit
- **P90:** Cleanup

### D2-Q14: Enforcement Engine Architecture
**Decision:** Option D - Scripts Delegate to Orchestrator
- Thin hook scripts proxy to Python RuleEngine
- 89% LOC reduction vs pure external scripts

### D3-Q10: Delegation Structure
**Decision:** Option A - Hierarchical Single-Parent Delegation
- Task tool returns to same parent
- Cross-branch coordination via orchestrator only
- Prevents 41-86.7% failure rate of peer/shared patterns

### D3-Q11: IDE vs Web Orchestration
**Decision:** Option B - Dual Orchestrator Pattern
- BMad Master for IDE (file I/O, manifests, 18 handlers)
- BMad Web Orchestrator for Web (embedded XML, no file I/O)

### D3-Q18: PM Delegation to 92 Agents
**Decision:** Option E - Hierarchical Manifest + Direct Task Invocation
- PM uses categorized manifest for agent discovery
- Task tool for deterministic invocation
- 91% complexity reduction

### D6-Q10: Initialization Model
**Decision:** Option A - Full 12-phase model
- 8 unconditional phases, 4 conditional
- Validated by 1513+ tests

### D6-Q18: Slash Command vs Task Tool
**Decision:** Option C - Separate Execution Paths
- Slash = menus/state/EMBODIES
- Task = stateless/DELEGATES

### D10-Q1: Workflow Executor
**Decision:** Option D - Hybrid Executor Pattern
- Universal structure + pluggable handlers
- 39% reuse (~330 LOC from BMAD)

### D10-Q6: Sub-Agent Hint Injection
**Decision:** Option D - Registry-Driven Injection
- Registry defines injection points (WHAT)
- Orchestrator manages selection (WHEN)
- `enhance_agent_prompt` pattern

---

## 3. PROCESS & STATE (Already Decided)

### D6-Q1: Process Handoff
**Decision:** Option C - Configurable mode
- Exec default (production), subprocess for debugging
- `os.execvpe()` for process replacement

### D6-Q2: State at Handoff
**Decision:** Option A - Complete State Death
- All in-memory state lost at handoff
- Only files on disk survive

### D6-Q3: CLI Construction
**Decision:** Option D - Mixed Strategy
- Security via CLI (`--dangerously-skip-permissions`)
- Bulky via files (`--system-prompt-file` for 152KB prompt)
- Optional via environment

### D6-Q5: Pre-Handoff Deployment
**Decision:** Option A - Full Deployment (6 targets, 1.49MB)
- `~/.claude.json` (89KB)
- `~/.claude/settings.json` (1.9KB)
- `PM_INSTRUCTIONS.md` (~152KB)
- `~/.claude/agents/*.md` (1.1MB)
- `~/.claude/skills/` (356KB)
- `~/.claude/output-styles/` (<1KB)

### D6-Q6: System Prompt Assembly
**Decision:** Option A - Multi-section assembly (10 sections)
1. PM_INSTRUCTIONS
2. Custom
3. WORKFLOW
4. MEMORY
5. PM Memories
6. Agent Memories
7. Capabilities (dynamic)
8. Temporal Context (dynamic)
9. BASE_PM
10. Output Style

### D4-Q6 & D4-Q8: State Authority
**Decision:** Frontmatter SSOT
- Frontmatter = Single Source of Truth
- Tickets = Projection layer only
- One-way sync: frontmatter → tickets

---

## 4. IMPLEMENTATION PHASES (Already Decided)

### D2-Q1 & D2-Q15: Lifecycle Phases
**Decision:** 4-Phase Lifecycle
- **Phase 1:** SessionStart (init)
- **Phase 2:** PreToolUse (enforce)
- **Phase 3:** PreCompact (persist)
- **Phase 4:** Stop (complete)
- Industry validation: 9/9 production systems

### D4-Q5: Session Resumption
**Decision:** Option E - 3-Tier Resumption
- **Tier 1:** Frontmatter <5ms (95% of cases)
- **Tier 2:** Checkpoint files <50ms (fallback)
- **Tier 3:** Orchestrator awareness <500ms (complex)

### D9-Q8: Variable Resolution
**Decision:** Option C - Two-Phase Resolution
- **Phase 1 (Static):** System+Framework vars via hooks at SessionStart
- **Phase 2 (Dynamic):** Project+Runtime vars during workflow

### D10-Q10 & D10-Q11: Path Files
**Decision:** Template-Based Generation + Standalone Path Files
- `method-greenfield.yaml`, `method-brownfield.yaml`
- `enterprise-greenfield.yaml`, `enterprise-brownfield.yaml`
- Atomic creation from Handlebars template

---

## 5. AGENT REBUILD (Already Decided)

### D12: Unified Agent Template v3.0
- All 87 agents rebuilt with unified template
- 2,000-3,000 tokens per agent
- 10 agent_types defined

### D13: Agent Routing
- L1 frontmatter aggregation from agent .md files
- Agent files ARE the registry (SSOT)
- `extract_l1_metadata.py` → `agent-index.yaml`

### D14: Agent Builder Workflow
- 6-step facilitated workflow
- Collaborative discovery COMPULSORY
- Quality through thoroughness > speed

### D8-Q14: Backward Compatibility
**Decision:** Option D - Hybrid backward-compatible
- Both `trigger` and `triggers` supported
- Zero breaking changes for migration

---

## 6. MCP INTEGRATION (Already Decided)

### D7: MCP Integration (16 questions)
- Single Aggregator proxy pattern
- 26 servers, 332 tools
- Progressive disclosure for tool scale
- Session-scoped pooling with lazy initialization

### D6-Q8: MCP Gateway
**Decision:** Option A - External Server
- Gateway spawns AFTER os.execvpe()
- Cannot be internal (dies at handoff)

---

## WHAT'S NOT DECIDED (True Gaps)

1. **Agent Classification for 87 agents** - Which agents fit Tier 1/2/3?
2. **Rebuild Prioritization** - Which agents first?
3. **Session 6 architectural concerns** - Delivery mechanism clarification (RESOLVED in Session 7)

---

*Extract compiled Session 7 | 2025-12-12*
