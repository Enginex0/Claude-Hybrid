# D3: Multi-Agent Strategy - Question Set

**Decision:** How should Claude-Hybrid implement multi-agent collaboration and orchestration?
**Status:** ✅ COMPLETE (20/20 DECIDED)
**Generated:** 2025-12-08 (Updated 2025-12-09)
**Sources:** bmad-analysis/10-PARTY-MODE.md, bmad-analysis/13-SUB-AGENTS-SYSTEM.md, bmad-analysis/04-AGENTS-SYSTEM.md, claude-mpm-complete-analysis/05-AGENTS-SKILLS.md

---

## Checkpoint Status

| Question | Status | Answer |
|----------|--------|--------|
| Q1 | **DECIDED** | Option E (Synthesized): Tiered Hybrid Selection (TIER 1: User-Directed, TIER 2: Scenario-Based ~80%, TIER 3: Intelligent Scoring ~15%, TIER 4: Rotation Modifier ~5%) |
| Q2 | **DECIDED** | Option D (Synthesized): Contextual Hybrid Cross-Talk (Mode-based: A for brainstorm, C for implementation, B for structured tasks, ~1420 LOC) |
| Q3 | **DECIDED** | Option E (Synthesized): State-Managed with Mode-Tiered Mechanisms (D foundation + A triggers + C task completion, ~220 LOC) |
| Q4 | **DECIDED** | Option D: Exploration vs Execution (Party Mode for exploration/divergent thinking, Sequential Delegation for execution/deliverables, ~120 LOC) |
| Q5 | **DECIDED** | Option D: Hybrid State Management (Tier 1: Working Memory/Conversation, Tier 2: Session State/Frontmatter, Tier 3: Persistent State/Tickets, ~240 LOC net new) |
| Q6 | **DECIDED** | Option E (Synthesized): Tiered Hybrid Sub-Agent Invocation (TIER 1: User-Directed, TIER 2: Orchestrator-Validated for critical, TIER 3: Proactive Trigger Matching with guards, TIER 4: Injection Hints, ~400-500 LOC) |
| Q7 | **DECIDED** | Option D (Synthesized): Tiered Role-Based Specialization (4-tier hierarchy: Orchestrator, Phase Leads, Role Specialists, Sub-Agents, ~25-30 agents total, ~550 LOC net new) |
| Q8 | **DECIDED** | Option E (Synthesized): Tiered Output Architecture (TIER 1: Complete message primary 90-95%, TIER 2: File artifacts conditional 5-10%, TIER 3: JSON metadata supplementary, ~290 LOC net new) |
| Q9 | **DECIDED** | Option C: Hybrid Installation with Priority Resolution (Project > User > System, ~520 LOC net new with 400 LOC reuse, $18.5K 3-year TCO lowest) |
| Q10 | **DECIDED** | Option A: Hierarchical Single-Parent Delegation (Task tool returns to same parent, cross-branch via Orchestrator, ~280 LOC net new, $22K 3-year TCO lowest) |
| Q11 | **DECIDED** | Option B: Dual Orchestrator Pattern (BMad Master for IDE + BMad Web Orchestrator for Web, 185 LOC actual, 100% BMAD reuse, $10 3-year TCO) |
| Q12 | **DECIDED** | Option C: Hybrid with User Override (Orchestrator suggests agent based on task, user can accept/override/invoke explicitly, ~128 LOC net new, $47K 3-year TCO) |
| Q13 | **DECIDED** | Option C: Agent Manifest-Driven Selection (dynamically select 2-3 relevant agents based on task domain via manifest, ~380-480 LOC net new, 55-65% BMAD reuse, $25-35K 3-year TCO) |
| Q14 | **DECIDED** | Option D: Hierarchical Persona Authority (role-based tier hierarchy for conflict resolution, ~450 LOC total, ~200 LOC net new, 55% reuse from D3-Q1/Q2, $7.5K 3-year TCO) |
| Q15 | **DECIDED** | Option E (Synthesized): Project Configuration with Sensible Defaults (TIER 1: All agents available by default, TIER 2: Optional project config for scoping, TIER 3: Runtime discovery enhancement, ~350 LOC net new, $25K 3-year TCO) |
| Q16 | **DECIDED** | Option A: Filename Stem Matching (Claude Code native - subagent_type matches filename stem, O(1) lookup, 0 LOC net new, $1.8K 3-year TCO) |
| Q17 | **DECIDED** | Option B: Project Highest Priority (Project > Remote > User > System - extends D3-Q9, 50-80 LOC net new, $1.5K 3-year TCO) |
| Q18 | **DECIDED** | Option E (Synthesized): Hierarchical Manifest + Direct Task Invocation (PM uses categorized manifest for discovery, Task tool for deterministic invocation, ~220 LOC net new, 90% reuse, $30K 3-year TCO) |
| Q19 | **DECIDED** | Option E: Tiered Registry with Agent Scoping (B+D+A: Registry-based assignment + Project>User>System priority + agent_types filtering, ~55 LOC net new, 80% reuse, $11K 3-year TCO). FUTURE ENHANCEMENT: Option F (Progressive Disclosure per Anthropic pattern) planned for Phase 2. |
| Q20 | **DECIDED** | Option D: Session Boundary Only (Claude Code native behavior - agents loaded at session start, new agents available next session. Workaround: /agents command for interactive creation. 0 LOC - already implemented by Claude Code) |

---

## Questions: Party Mode (Parallel) Multi-Agent Collaboration (Q1-Q5)

### Q1: Agent Selection for Parallel Collaboration
**Context:** How should agents be selected for Party Mode parallel collaboration sessions?

Options:
- A: User-directed only - User explicitly selects which agents join the collaboration. Simple and predictable but requires user to know which agents are best for task.
- B: Scenario-based selection - Define collaboration scenarios (brainstorm, debug, design, code review) with pre-configured agent groups for each.
- C: Intelligent agent scoring - System analyzes task requirements and automatically scores/selects most relevant agents using NLP/embeddings.
- D: Rotation-based participation - Rotate agents to ensure balanced participation and prevent same agents dominating all sessions.
- E: Tiered Hybrid Selection - Combine multiple strategies in priority tiers: User-Directed > Scenario-Based > Intelligent Scoring > Rotation.

### Q2: Cross-Talk Structure Between Agents
**Context:** How should agents communicate during parallel Party Mode collaboration?

Options:
- A: Natural discourse - Agents discuss freely like humans in a meeting, building on each other's ideas organically.
- B: Sequential response model - Agents respond in turns, each building on previous responses in structured order.
- C: Bounded interaction - Each agent gets limited turns (2-3 responses max) to prevent runaway discussions.
- D: Contextual Hybrid Cross-Talk - Adapt communication style based on collaboration mode: Natural for brainstorming, Bounded for implementation, Sequential for structured tasks.

### Q3: Parallel Agent Discussion Termination
**Context:** How does the system determine when parallel agent discussion should end?

Options:
- A: Explicit trigger words - User or agents use keywords like "CONSENSUS", "COMPLETE", "EXIT" to signal termination.
- B: Round-based limits - Discussion automatically ends after N rounds of agent responses.
- C: Task completion detection - System detects when agents have addressed all aspects of the task and consensus is reached.
- D: State machine management - Track discussion state (Init -> Active -> Exit) with party_active flag and explicit state transitions.
- E: State-Managed with Mode-Tiered Mechanisms - State machine foundation with explicit triggers for user control and automatic task completion detection.

### Q4: Party Mode vs Sequential Delegation Usage
**Context:** When should the system use Party Mode (parallel) vs Sequential Delegation?

Options:
- A: Task complexity threshold - Use Party Mode for complex/ambiguous tasks, Sequential Delegation for straightforward tasks.
- B: User preference - Let user choose mode via explicit command or config flag.
- C: Phase-based selection - Use Party Mode during planning/design phases, Sequential Delegation during implementation.
- D: Exploration vs Execution - Party Mode for exploration and divergent thinking, Sequential Delegation for execution and deliverables.

### Q5: Agent State and Context Management
**Context:** How should agent state and context be managed during and between collaboration sessions?

Options:
- A: Stateless agents - Each session starts fresh with no memory of previous interactions. Simple but limits continuity.
- B: Session-scoped memory - Agents remember context within current session but forget between sessions.
- C: Persistent agent memory - Agents maintain memory across sessions, stored in files or database.
- D: Hybrid State Management - Three tiers: Working Memory (conversation), Session State (YAML frontmatter), Persistent State (tickets).

---

## Questions: Sub-Agent System Design (Q6-Q10)

### Q6: Sub-Agent Invocation Decision Process
**Context:** Who decides when to invoke a sub-agent and how?

Options:
- A: User-directed only - User explicitly invokes sub-agents via commands. Full control but requires knowledge of available sub-agents.
- B: Orchestrator-directed - Main orchestrator analyzes task and delegates to appropriate sub-agents automatically.
- C: Agent proactive invocation - Individual agents can invoke sub-agents when they detect need for specialized help.
- D: Workflow injection hints - Workflow definitions specify which sub-agents should be invoked at specific steps.
- E: Tiered Hybrid Sub-Agent Invocation - Four-tier hierarchy: User-Directed > Orchestrator-Validated > Proactive Trigger Matching > Injection Hints.

### Q7: Sub-Agent Specialization Granularity
**Context:** How specialized should sub-agents be? How many should exist?

Options:
- A: Fine-grained specialization - Many highly specialized sub-agents (40-60+), each focused on narrow domain.
- B: Coarse-grained specialization - Fewer broadly capable sub-agents (10-20), each handling wider domain.
- C: Single-tier flat structure - All sub-agents are peers with similar capability levels.
- D: Tiered Role-Based Specialization - Four-tier hierarchy: Orchestrator > Phase Leads > Role Specialists > Sub-Agents (25-30 total).

### Q8: Sub-Agent Output Return Format
**Context:** How should sub-agents return results to their invoker?

Options:
- A: Complete message response - Sub-agent returns full response as message text, immediately integrated into conversation.
- B: File-based handoff - Sub-agent writes results to files, invoker reads files to get results.
- C: Structured JSON response - Sub-agent returns JSON object with status, result, metadata for programmatic processing.
- D: Hybrid output model - Sub-agent can return both message and file artifacts based on task requirements.
- E: Tiered Output Architecture - Complete message primary (90-95%), File artifacts conditional (5-10%), JSON metadata supplementary.

### Q9: Sub-Agent Definition Installation Locations
**Context:** Where should sub-agent definitions be installed and discovered?

Options:
- A: Project-level only - Sub-agents defined in project's .claude/agents/ directory. Project-specific but requires duplication.
- B: User-level only - Sub-agents in ~/.claude/agents/ shared across all projects. Reusable but not project-customizable.
- C: Hybrid Installation with Priority Resolution - Three tiers: Project > User > System with priority override pattern.
- D: Remote registry - Sub-agents stored in cloud registry, downloaded on-demand. Centralized updates but requires network.

### Q10: Main Agent to Sub-Agent Delegation Structure
**Context:** How should delegation between main agents and sub-agents be structured?

Options:
- A: Hierarchical Single-Parent Delegation - Task tool returns to same parent, cross-branch coordination via orchestrator only.
- B: Peer-to-peer delegation - Any agent can directly invoke any other agent as peer without hierarchy.
- C: Shared sub-agent pool - Multiple main agents can invoke same sub-agent concurrently, sub-agent manages multiple contexts.
- D: Dynamic graph delegation - Delegation structure adapts based on task, forming dynamic directed graph of dependencies.

---

## Questions: Agent Orchestration and Transformation (Q11-Q15)

### Q11: IDE vs Web Environment Orchestration
**Context:** Should Claude-Hybrid use the same orchestrator for IDE and Web environments?

Options:
- A: Unified orchestrator - Single orchestrator works across both IDE and Web with environment detection.
- B: Dual Orchestrator Pattern - Separate orchestrators: BMad Master for IDE, BMad Web Orchestrator for Web.
- C: Environment adapters - Single core orchestrator with pluggable adapters for IDE vs Web differences.
- D: Web-only orchestration - Focus on Web environment initially, add IDE support later.

### Q12: Explicit vs Implicit Agent Transformation
**Context:** Should agent selection be explicit or implicit during task execution?

Options:
- A: Explicit agent selection - User always explicitly chooses which agent to use for each task.
- B: Implicit transformation - System automatically switches between agents based on task analysis without user awareness.
- C: Hybrid with User Override - Orchestrator suggests agent based on task, user can accept/override/invoke explicitly.
- D: Context-aware transformation - Agent transformation happens automatically in workflows, explicitly for user commands.

### Q13: Party Mode Multi-Agent Collaboration Mechanism
**Context:** How should multiple agents be selected and coordinated for Party Mode?

Options:
- A: All-agents participation - Load all available agents into Party Mode discussion.
- B: User selects participants - User explicitly chooses which 2-4 agents join Party Mode.
- C: Agent Manifest-Driven Selection - Dynamically select 2-3 relevant agents based on task domain via manifest.
- D: Adaptive group sizing - System determines optimal number of agents (2-5) based on task complexity.

### Q14: Agent Persona Influence on Collaboration
**Context:** How should agent personas affect multi-agent collaboration dynamics?

Options:
- A: Persona-neutral collaboration - Agents collaborate without persona influencing behavior or authority.
- B: Persona-driven expertise weighting - Agent personas determine whose input carries more weight in specific domains.
- C: Persona-based deference patterns - Agents defer to each other based on persona hierarchy in conflict situations.
- D: Hierarchical Persona Authority - Role-based tier hierarchy for conflict resolution with clear authority levels.

### Q15: Specialized Agent Availability Scope
**Context:** Should all specialized agents always be available or should availability be scoped?

Options:
- A: All agents always available - Every agent accessible from any context at any time.
- B: Phase-restricted availability - Certain agents only available during specific workflow phases.
- C: Dynamic availability based on context - Agent availability adapts based on project type, current task, user preferences.
- D: Project configuration scoping - Project config explicitly defines which agents are available.
- E: Project Configuration with Sensible Defaults - All agents available by default, optional project config for scoping.

---

## Questions: Agent Integration and Lifecycle (Q16-Q20)

### Q16: Task Tool Agent Matching Mechanism
**Context:** How should the Task tool's subagent_type parameter match to actual agent definitions?

Options:
- A: Filename Stem Matching - Claude Code native: subagent_type matches agent filename stem (O(1) lookup).
- B: Fuzzy name matching - System matches subagent_type using fuzzy string matching against agent names.
- C: Keyword/tag matching - Agents tagged with keywords, Task tool matches based on task requirements to tags.
- D: Semantic embedding matching - Use embeddings to match task description to most semantically similar agent.

### Q17: Agent Discovery Tier Precedence
**Context:** When agents exist in multiple tiers (project/user/system), which takes precedence?

Options:
- A: System highest priority - System agents override user and project agents (safeguards).
- B: Project Highest Priority - Project > Remote > User > System (extends D3-Q9 pattern).
- C: Merge all tiers - Combine agents from all tiers into single pool with no precedence.
- D: User choice of precedence - Config setting allows user to specify precedence order.

### Q18: PM Delegation to 92 Specialized Agents
**Context:** How should the PM agent (orchestrator) efficiently delegate to 92+ specialized agents?

Options:
- A: Direct routing table - PM maintains mapping of task patterns to specific agents (deterministic).
- B: Hierarchical categories - Organize 92 agents into categories (10-15), PM routes to category then to specific agent.
- C: Intelligent task classification - PM uses NLP to classify task, then routes to best-matching agent from pool.
- D: Registry-based discovery - PM queries agent registry with task requirements, registry returns best matches.
- E: Hierarchical Manifest + Direct Task Invocation - PM uses categorized manifest for discovery, Task tool for invocation.

### Q19: Skill Loading Scope for Collaborating Agents
**Context:** When multiple agents collaborate, which skills should each agent have access to?

Options:
- A: Agent-scoped skills - Each agent only loads skills explicitly assigned to them via agent_types filtering.
- B: Registry-based skill assignment - Central registry defines which skills are available to which agents.
- C: All skills available to all agents - Maximum flexibility, no scoping restrictions.
- D: Project>User>System priority skill resolution - Skills resolved with tier precedence like agents.
- E: Tiered Registry with Agent Scoping - Registry-based assignment + Project>User>System priority + agent_types filtering. FUTURE: Option F (Progressive Disclosure) planned for Phase 2.

### Q20: Claude Code Restart Requirements During Collaboration
**Context:** When new agents/skills are added during session, does Claude Code need restart?

Options:
- A: Hot reload - New agents/skills immediately available without restart via dynamic loading.
- B: Graceful session refresh - Trigger lightweight refresh that reloads agents/skills without full restart.
- C: Manual restart required - User must explicitly restart Claude Code to load new agents/skills.
- D: Session Boundary Only - Claude Code native behavior: agents loaded at session start, new agents available next session. Workaround: /agents command for interactive creation.

---

## Resume Instructions

**Next session:** Read this file, continue from first PENDING question.
**Methodology:** BMad Master facilitates, President decides each question.
**After completion:** Update ARCHITECTURAL-DECISIONS.md with D3 decision.
