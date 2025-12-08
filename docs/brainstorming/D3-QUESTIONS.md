# D3: Multi-Agent Strategy - Question Set

**Decision:** How do multiple agents collaborate in Claude-Hybrid?
**Status:** PENDING
**Generated:** 2025-12-07 (Session 5)
**Sources:** 4 documents analyzed by subagents

---

## Checkpoint Status

| Question | Status | Answer |
|----------|--------|--------|
| Q1 | **DECIDED** | **Option E: Tiered Hybrid Selection (User→Scenario→Scoring→Rotation)** |
| Q2 | **DECIDED** | **Option D: Contextual Hybrid Cross-Talk (Mode-based: A for brainstorm, C for implementation, B for structured)** |
| Q3 | **DECIDED** | **Option E: State-Managed with Mode-Tiered Mechanisms (D foundation + A triggers + C task completion)** |
| Q4 | **DECIDED** | **Option D: Exploration vs Execution (Party Mode for exploration, Sequential Delegation for execution)** |
| Q5 | **DECIDED** | **Option D: Hybrid State Management (Tier 1: Working Memory, Tier 2: Session/Frontmatter, Tier 3: Persistent/Tickets)** |
| Q6-Q20 | PENDING | - |

---

## Questions from BMAD 10-PARTY-MODE.md

### Q1: How should agents be selected for parallel collaboration?
Options:
- A: Intelligent scoring algorithm - Score agents based on role match, identity relevance, principles alignment, then pick 2-3 highest-scoring with diverse perspectives
- B: Scenario-based selection - Use predefined selection strategies based on question type (technical -> Architect + Developer; product -> PM + UX)
- C: User-directed selection - When user addresses a specific agent, include that agent plus 1-2 complementary agents chosen by the system
- D: Rotation-based selection - Track participation history and ensure all agents contribute over time

### Q2: How should cross-talk between agents be structured?
Options:
- A: Natural discourse model - Agents refer to each other by name, build on or respectfully disagree with points, ask each other questions
- B: Sequential response model - Each agent responds independently to the user without acknowledging other agents
- C: Bounded interaction model - Allow cross-talk but enforce expertise boundaries so agents only comment within their domain

### Q3: How should parallel agent discussions be terminated?
Options:
- A: Explicit trigger words - User says specific exit commands ("*exit", "goodbye", "end party", "quit")
- B: Natural conclusion detection - System detects when conversation naturally concludes and prompts confirmation
- C: Task completion - Agent(s) complete the assigned task and automatically return control
- D: State-managed transitions - Track party_active flag in frontmatter and transition through Init -> Active -> Exit states

### Q4: When should Party Mode (parallel discussion) be used versus Sequential Delegation?
Options:
- A: Creative brainstorming scenarios - Use Party Mode for divergent thinking where multiple perspectives generate richer ideas
- B: Complex multi-domain questions - Use Party Mode when a question spans multiple expertise areas requiring real-time synthesis
- C: Task-focused work - Use Sequential Delegation when specific deliverables are needed and agents work independently
- D: General discussion vs. implementation - Party Mode for exploration; Sequential Delegation for actual implementation

### Q5: How should agent state and context be managed during multi-agent collaboration?
Options:
- A: Frontmatter tracking - Use YAML frontmatter with stepsCompleted, workflowType, party_active flags
- B: Ticket-based state - Use ticket system to track state and enable task handoffs between agents
- C: Conversation context - Maintain shared conversation context that all participating agents can reference
- D: Hybrid state management - Combine workflow frontmatter for Party Mode with ticket state for Sequential Delegation

---

## Questions from BMAD 13-SUB-AGENTS-SYSTEM.md

### Q6: How should main agents decide when to invoke sub-agents?
Options:
- A: Injection-triggered invocation - Sub-agents are invoked when workflow reaches injection points that hint usage
- B: Proactive trigger matching - Main agent reads sub-agent descriptions containing "use PROACTIVELY when [trigger]" and autonomously decides
- C: Explicit orchestrator direction - A separate orchestrator agent decides when main agents should invoke sub-agents
- D: User-directed invocation - User explicitly requests sub-agent usage rather than agents deciding autonomously

### Q7: What is the appropriate granularity for sub-agent specialization?
Options:
- A: Fine-grained specialization (BMAD approach) - 16 highly focused sub-agents in 4 categories, each with single-purpose expertise
- B: Coarse-grained specialization - Fewer, broader sub-agents that handle multiple related tasks to reduce delegation overhead
- C: Dynamic specialization - Sub-agents that can be composed or configured at runtime based on task requirements

### Q8: How should sub-agent output be returned to the calling agent?
Options:
- A: Complete structured analysis in final message - Sub-agent MUST return ready-to-use content directly, no summaries or references
- B: File-based handoff - Sub-agent writes output to file, returns file path for parent agent to read
- C: Structured data return - Sub-agent returns JSON/YAML that parent agent parses and integrates
- D: Incremental streaming - Sub-agent streams partial results as work progresses for real-time integration

### Q9: Where should sub-agent definitions be installed for multi-agent systems?
Options:
- A: Project-level installation - Sub-agents in `{project}/.claude/agents/` for project-specific customization
- B: User-level global installation - Sub-agents in `~/.claude/agents/` for consistent behavior across projects
- C: Hybrid installation - Core sub-agents global, project-specific sub-agents local
- D: Runtime loading - Sub-agents loaded dynamically from remote registry based on workflow needs

### Q10: How should the delegation relationship between main agents and sub-agents be structured?
Options:
- A: Hierarchical single-parent delegation - Main agent invokes sub-agent via Task tool, sub-agent returns to same parent
- B: Shared sub-agent pool - Multiple main agents can invoke the same sub-agent concurrently with orchestrator managing conflicts
- C: Chained sub-agent delegation - Sub-agents can invoke other sub-agents creating delegation chains (multi-level depth)
- D: Peer collaboration - Sub-agents can communicate directly with each other without returning to parent first

---

## Questions from BMAD 04-AGENTS-SYSTEM.md

### Q11: How should orchestration differ between IDE and Web environments?
Options:
- A: Single orchestrator pattern - Use one orchestrator that adapts behavior based on environment detection
- B: Dual orchestrator pattern - Maintain separate orchestrators: BMad Master for IDE, BMad Web Orchestrator for Web
- C: Unified orchestrator with environment adapters - One orchestrator core with pluggable handlers for IDE vs Web

### Q12: Should agent transformation be explicit (user-invoked) or implicit (orchestrator-decided)?
Options:
- A: Explicit transformation only - User must invoke command to switch agents, orchestrator never auto-switches
- B: Implicit orchestrator-driven - Orchestrator analyzes task and automatically transforms to appropriate agent
- C: Hybrid with user override - Orchestrator suggests/auto-selects agents based on task type, but user can override
- D: Task-triggered transformation - Menu items automatically load the appropriate agent

### Q13: How should Party Mode multi-agent collaboration work in Claude-Hybrid?
Options:
- A: Sequential delegation via Task tool - PM delegates to one agent at a time; agents complete work and return before next
- B: Parallel discussion (2-3 agents) - Multiple agents loaded simultaneously for cross-talk and real-time collaboration
- C: Agent manifest-driven selection - Use manifest to dynamically select relevant agents based on task domain
- D: Module-scoped Party Mode - Limit party mode to agents within same module to reduce context overhead

### Q14: How should agent personas and principles influence collaboration behavior?
Options:
- A: Persona-driven conflict resolution - When agents disagree, defer to the agent whose principles most align with task
- B: Communication style adaptation - Agents adjust their outputs based on receiving agent's communication style
- C: Principle voting - Multiple agents' principles weighted equally; conflicts resolved by finding common ground
- D: Hierarchical persona authority - Define clear hierarchy based on persona seniority and role scope

### Q15: Should specialized module agents be available in all contexts or domain-restricted?
Options:
- A: Always available - All agents accessible regardless of project type; user/orchestrator decides relevance
- B: Module-based activation - Only activate relevant modules based on project type
- C: Core + on-demand modules - Core agents always available; specialized modules loaded explicitly when needed
- D: Project configuration - Config file specifies which modules/agents are available at initialization

---

## Questions from Claude-MPM 05-AGENTS-SKILLS.md

### Q16: How should Task tool agent matching work in multi-agent scenarios?
Options:
- A: Filename stem matching (Claude Code native) - Use existing pattern where Task tool matches subagent_type to filename stem
- B: Category-based routing - Route based on agent categories rather than individual agent names
- C: Keyword/capability matching - Use skill auto-linking mechanism that infers agent from keywords

### Q17: What agent discovery tier should take precedence when multiple agents exist with the same name?
Options:
- A: Remote highest (4-tier priority) - Remote > User > Project > System
- B: Project highest - Invert priority so project-specific agents always override
- C: Merge with override - Combine capabilities from multiple tiers, with higher tiers overriding specific fields

### Q18: How should PM delegate to the 92 available specialized agents?
Options:
- A: Direct Task tool invocation - PM uses Task tool with specific subagent_type matching agent filename stems
- B: Category-first routing - PM delegates to category and a router within that category selects specific agent
- C: Capability-based selection - PM describes needed capabilities and matching algorithm selects appropriate agent
- D: Tool sandboxing aware - PM uses TodoWrite only, then Task tool delegates to specialists with full toolset

### Q19: Should skills be loaded per-agent or shared across collaborating agents?
Options:
- A: Agent-scoped skills - Each agent loads only skills mapped via agent_types field in skill YAML frontmatter
- B: Registry-based assignment - Use skills_registry.yaml which maps agents to required/optional skills
- C: Progressive disclosure shared - All agents share skills but use 3-level progressive disclosure to save 50-80% tokens
- D: Project-tier override - Skills follow 3-tier priority so collaborating agents in same project share overrides

### Q20: When should Claude Code restart be required during multi-agent collaboration?
Options:
- A: Never during session - Pre-deploy all agents and skills before session starts; no runtime changes that require restart
- B: On new agent/skill deployment - If remote sync adds new agents or PM dynamically deploys skills, require restart
- C: Lazy restart on first access - Cache newly deployed agents/skills but only restart when agent needs newly-deployed capability
- D: Session boundary only - Allow agent deployment during session but new agents only available in next session

---

## Resume Instructions

**Next session:** Read this file, continue from first PENDING question.
**Methodology:** BMad Master facilitates, President decides each question.
**After completion:** Update ARCHITECTURAL-DECISIONS.md with D3 decision.
