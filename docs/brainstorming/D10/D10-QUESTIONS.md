# D10: Workflow Engine & Lifecycle - Question Set

**Decision:** How does Claude-Hybrid execute workflows and enforce lifecycle?
**Status:** ✅ COMPLETE (17/17 DECIDED)
**Generated:** 2025-12-10
**Updated:** 2025-12-11 - All questions decided
**Sources:** BMAD Method architecture and workflow documentation (02-ARCHITECTURE-CORE.md, 05-WORKFLOWS-SYSTEM.md, 14-WORKFLOW-PATHS.md, 15-CUSTOMIZATION-EXTENSION.md)

---

## Redundancy Audit Notes

The following 8 questions were removed due to overlap with existing D2-D5 decisions:

| Removed | Original Topic | Overlaps With |
|---------|----------------|---------------|
| Q2 | Execution mandates (HOW enforced) | D2 domain - refocus on WHICH mandates exist |
| Q4 | Normal vs YOLO modes | D2-Q17 mode-conditional bypass decided |
| Q13 | 4-phase lifecycle enforcement | D2-Q15 already decided exactly this |
| Q14 | Phase skip handling | D2-Q16/Q17 tiered HARD/SOFT covers this |
| Q15 | Prerequisite enforcement | D2-Q18/Q19 patterns cover this |
| Q16 | Phase completion tracking | D4 state tracking territory |
| Q17 | Project level detection | D3-Q12 hybrid with override decided |
| Q18 | Track selection | D5-Q5 already decided track selection mechanism |
| Q2 (current) | Save-and-pause pattern | D2-Q17 mode-conditional bypass covers this |

---

## Checkpoint Status

| Question | Status | Answer |
|----------|--------|--------|
| Q1 | **DECIDED** | Option D: Hybrid Executor Pattern |
| Q2 | **DECIDED** | Option A: Full Deep Merge Implementation |
| Q3 | **DECIDED** | Option A: Per-Agent Customize Files |
| Q4 | **DECIDED** | Option B: Whitelist Approach |
| Q5 | **DECIDED** | Option D: Type-Specific Resolution |
| Q6 | **DECIDED** | Option D: Registry-Driven Injection |
| Q7 | **DECIDED** | Option B: Variables + Protocols |
| Q8 | **DECIDED** | Option D: Hybrid Protocol System |
| Q9 | **DECIDED** | Option B: Mode-Triggered Injection |
| Q10 | **DECIDED** | Option A: Template-Based Generation |
| Q11 | **DECIDED** | Option A: Standalone Path Files |
| Q12 | **DECIDED** | Option B: Handler-Multi with Fuzzy Matching |
| Q13 | **DECIDED** | Option D: Hybrid Validation |
| Q14 | **DECIDED** | Option D: Template-driven |
| Q15 | **DECIDED** | Option A: Unified Agent Template v3.0 (2,000-3,000 tokens, 10 agent_types) |
| Q16 | **DECIDED** | Option A: L1 Frontmatter Aggregation (agent files = registry SSOT) |
| Q17 | **DECIDED** | Option A: 6-Step Facilitated Workflow (collaborative discovery compulsory) |

---

## Questions: workflow.xml Universal Executor (Q1)

### Q1: How should Claude-Hybrid implement the universal workflow executor pattern?
**Context:** BMAD's workflow.xml is a single XML file that can execute ANY workflow through declarative mandates and step processing rules.

Options:
- A: Single Universal Executor - One executor file that interprets workflow.yaml/workflow.md files declaratively (BMAD pattern)
- B: Typed Executors - Multiple executor types specialized for different workflow categories (template-workflow vs action-workflow)
- C: Orchestrator-Embedded Execution - No separate executor; the PM orchestrator agent interprets workflows directly
- D: Hybrid Executor Pattern - Universal executor for structure, with pluggable handlers for specialized processing

**NOTE:** Save-and-pause pattern (template-output) behavior is governed by D2-Q17 mode-conditional bypass decision.

---

## Questions: Deep Merge Customization System (Q2-Q5)

### Q2: How should Claude-Hybrid implement the deep merge pattern for agent customization?
**Context:** BMAD's deepMerge allows customize.yaml to override/extend agent definitions: objects merge recursively, arrays append, scalars override.

Options:
- A: Full Deep Merge Implementation - Objects merge recursively, arrays append, scalars override (exact BMAD pattern)
- B: Selective Override Only - Support scalar and object override, but arrays replace entirely rather than append
- C: Layer-Based Merge - Multiple customize layers (project, user, system) with defined precedence
- D: Explicit Merge Directives - Require merge strategy annotation per field ($override, $append, $replace)

### Q3: Where should customization files be located for agent extension?
**Context:** BMAD uses per-agent customize.yaml files in the agent directory structure.

> **NOTE:** See D3-Q9 for related directory structure decisions. This question focuses on customize file PLACEMENT strategy.

Options:
- A: Per-Agent Customize Files - customize.yaml alongside each agent definition (BMAD pattern)
- B: Central Customization Registry - Single customizations.yaml that references agent IDs and their overrides
- C: Hierarchical Customization - Project-level, module-level, and agent-level customize files with cascade
- D: Hybrid Location Strategy - Per-agent for simple overrides, central registry for cross-cutting customizations

### Q4: What agent properties should be customizable via the merge system?
**Context:** BMAD allows customization of persona (communication_style, principles), menu items, prompts, and critical_actions.

Options:
- A: Full Property Customization - All agent YAML properties are customizable via deep merge
- B: Whitelist Approach - Only explicitly permitted properties (persona, menu, prompts) can be customized
- C: Blacklist Approach - Everything customizable except protected properties (metadata.id, metadata.type)
- D: Tiered Permissions - Different customization rights for project-level vs user-level customize files

### Q5: How should customization conflicts be resolved when multiple sources apply?
**Context:** With hierarchical customization (project > user > bundled), conflicts can arise when same property is customized at multiple levels.

> **NOTE:** This question focuses on MERGE SEMANTICS (how values combine), distinct from priority chain ordering.

Options:
- A: Strict Priority - Higher tier always wins (project beats user beats bundled)
- B: Merge with Priority - Deep merge all tiers in priority order, later values override earlier
- C: Explicit Conflict Resolution - Require explicit annotation when overriding lower-tier customizations
- D: Type-Specific Resolution - Arrays always append across tiers, objects merge, scalars follow priority

---

## Questions: Content Injection System (Q6-Q9)

### Q6: How should Claude-Hybrid implement sub-agent hint injection?
**Context:** BMAD uses injection points that provide hints for when to invoke sub-agents, embedded dynamically in workflow content.

Options:
- A: Marker-Based Injection - Use special markers in workflow files that are replaced with sub-agent hints at load time
- B: Frontmatter Hints - Define sub-agent hints in workflow frontmatter, injected into context during execution
- C: Orchestrator-Managed Hints - PM orchestrator dynamically injects hints based on current workflow phase
- D: Registry-Driven Injection - Sub-agent registry defines injection points, system auto-injects when conditions match

### Q7: What dynamic content should be injectable during workflow execution?
**Context:** BMAD supports variable resolution, protocol invocation, and step content injection.

Options:
- A: Variable Resolution Only - Support {variable} and {{template}} resolution, no structural injection
- B: Variables + Protocols - Support variables plus invoke-protocol for reusable behavior patterns
- C: Full Content Injection - Variables, protocols, invoke-workflow, invoke-task, conditional content
- D: Configurable Injection Scope - Project-level configuration of which injection types are enabled

### Q8: How should the system handle protocol discovery and invocation?
**Context:** BMAD's discover_inputs protocol demonstrates reusable strategies (FULL_LOAD, SELECTIVE_LOAD, INDEX_GUIDED).

Options:
- A: Inline Protocol Definition - Protocols defined inline in workflow files, resolved at execution time
- B: External Protocol Library - Protocols stored in separate files, invoked by name
- C: Strategy Pattern Protocols - Protocols define multiple strategies, executor selects based on context
- D: Hybrid Protocol System - Core protocols in library, custom protocols inline, with strategy selection

### Q9: Should Claude-Hybrid support dynamic agent persona injection during workflows?
**Context:** Party Mode injects agent personas dynamically based on selection; workflows may need context-specific persona adjustments.

Options:
- A: No Dynamic Persona - Agent personas fixed at spawn, no mid-workflow injection
- B: Mode-Triggered Injection - Persona adjustments only when entering Party Mode or similar collaborative states
- C: Workflow-Declared Injection - Workflow steps can explicitly trigger persona context injection for relevant agents
- D: Continuous Persona Adaptation - System continuously injects relevant persona elements based on conversation flow

---

## Questions: Path Files & Status Tracking (Q10-Q11)

### Q10: How should workflow-init create and manage the bmm-workflow-status tracking file?
**Context:** workflow-init creates bmm-workflow-status.yaml with selected path, discovery workflow selections, and phase ready status.

> **NOTE:** Related to D4 state tracking. This question focuses on CREATION mechanism during workflow-init.

Options:
- A: Template-Based Generation - Use workflow status template, fill with path + selections + initial status
- B: Incremental Status Building - Build status file progressively as user makes selections during init
- C: Configuration Merge - Merge path YAML with user selections into unified status document
- D: Database-Backed Status - Store status in ticket/database, generate YAML view on demand

### Q11: How should the 4 path files (method-greenfield, method-brownfield, enterprise-greenfield, enterprise-brownfield) be structured and selected?
**Context:** Path files define phase structure with prerequisites, phase 0-3 workflows, and workflow flags (required/optional/recommended/conditional).

Options:
- A: Standalone Path Files - Each path is independent YAML with full phase/workflow definitions
- B: Base + Override Pattern - Single base path with override files for greenfield/brownfield and method/enterprise variants
- C: Declarative Path Composition - Define reusable workflow blocks, compose paths from blocks based on criteria
- D: Dynamic Path Assembly - Assemble path at runtime based on project characteristics rather than selecting predefined file

---

## Questions: Recent Framework Changes (Q12-Q14)

### Q12: How should the multi-menu handler system work for grouped menu items?
**Context:** Recent BMAD Method changes added `handler-multi.xml` enabling grouped menu items with fuzzy matching. Multiple menu items can route to a single handler.

Options:
- A: Single handler type - All menus use same handler regardless of grouping; no special multi-handler support.
- B: Handler-multi pattern (BMAD pattern) - Grouped menu items route to single handler via `handler-multi.xml` with fuzzy matching.
- C: Explicit routing table - Configuration file maps menu item patterns to handlers; no fuzzy matching.
- D: Dynamic handler discovery - System discovers handlers based on naming conventions; menus auto-route by convention.

### Q13: Should Claude-Hybrid include automated workflow compliance checking?
**Context:** Recent BMAD Method changes added a workflow compliance checker for automated validation before execution.

Options:
- A: No compliance checker - Rely on runtime enforcement hooks only; no pre-execution validation.
- B: Pre-execution validation (BMAD pattern) - Validate workflow against compliance rules before execution starts.
- C: Continuous compliance - Check compliance at each step transition during execution.
- D: Hybrid validation - Pre-execution for structure validation, runtime hooks for behavior enforcement.

### Q14: How should the workflow builder create continuable workflows?
**Context:** Recent BMAD Method changes enable the workflow builder to understand and create continuable workflows with resume capabilities.

Options:
- A: Implicit continuation - All workflows are continuable by default via frontmatter state tracking (D5-Q3).
- B: Explicit markers - Workflow files include continuation markers defining valid resume points.
- C: Builder metadata - Workflow builder generates continuation metadata in separate file alongside workflow.
- D: Template-driven - Continuable workflows must use specific template with built-in continuation logic.

---

## Questions: Agent Unification (Q15-Q17)

### Q15: What unified template structure should all 87 agents follow?
**Context:** Two agent systems (46 BMAD + 41 claude-mpm) have incompatible structures. Need unified template for Claude-Hybrid.

Options:
- A: Unified Template v3.0 - 2,000-3,000 tokens per agent, 10 agent_types, Frontmatter (L1) + Body (L2) structure
- B: BMAD-centric - Keep full BMAD structure with session_config, response_gate, behaviors
- C: Minimal template - 400-600 tokens, metadata only
- D: Two-tier files - Separate L1/L2 files per agent

**DECIDED:** Option A - Unified Template v3.0
- Frontmatter (L1): name, description (no examples), version, model, agent_type, tags + optional fields
- Body (L2): Expertise, Identity, When to Use, Core Capabilities, [Domain Sections], Boundaries, Tool Awareness, Memory Integration
- 10 agent_types: engineer, architect, qa, security, research, ops, creative, workflow, orchestrator, specialist
- Migration paths for both BMAD → Unified and Claude-MPM → Unified
- 13-point validation checklist

### Q16: How should PM discover and route to agents?
**Context:** PM needs to discover 87 agents and route tasks. Options: In-Process Registry vs MCP-Based Discovery.

Options:
- A: L1 Frontmatter Aggregation - Agent .md files ARE the registry (SSOT), extract_l1_metadata.py → agent-index.yaml
- B: Separate YAML Registry - Maintain separate agent-registry.yaml synced with agent files
- C: MCP-Based Discovery - MCP tool for agent discovery and routing suggestions
- D: Pure Claude-Native - No registry, Claude discovers agents via file reads

**DECIDED:** Option A - L1 Frontmatter Aggregation
- Agent files contain all routing data (name, description, agent_type, tags, triggers)
- Single source of truth = no sync problems
- Aligns with D2 (Control In-Process) - no network dependency
- Aligns with D7 (Graceful Degradation) - works 100% without MCP
- Token budget: 87 agents × ~150 tokens = ~13K tokens (94% savings vs L2 loading)

### Q17: What workflow should be used to build/rebuild agents?
**Context:** Need to build/rebuild 87 agents to unified template. Options: Automated vs Facilitated.

Options:
- A: 6-Step Facilitated Workflow - Collaborative discovery compulsory, guides user through structured process
- B: Minimal Task Agent - Simple Task agent that generates agents from brief descriptions
- C: Pure Automation - Batch script transforms existing agents automatically
- D: Optional Brainstorming - Facilitation available but not required

**DECIDED:** Option A - 6-Step Facilitated Workflow
- Step 1: Collaborative Discovery (COMPULSORY entry point)
- Step 2: Agent Classification (agent_type, module, model)
- Step 3: Build Frontmatter (L1) - collaborative
- Step 4: Build Body Sections (L2) - collaborative
- Step 5: Validation (13-point checklist)
- Step 6: Output & Completion
- Facilitation > Generation (BMAD insight)
- Quality through thoroughness > speed through shortcuts

---

## Resume Instructions

**Next session:** Read this file, continue from first PENDING question.
**Methodology:** BMad Master facilitates, President decides each question.
**After completion:** Update ARCHITECTURAL-DECISIONS.md with D10 decision.
