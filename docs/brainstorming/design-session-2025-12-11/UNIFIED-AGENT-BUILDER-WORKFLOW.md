# Unified Agent Builder Workflow Specification

**Created:** 2025-12-11 (Session 5)
**Status:** Draft for Review
**Based on:** BMAD Builder analysis + D12 Unified Template

---

## Overview

| Aspect | Value |
|--------|-------|
| **Invocation** | `/unified-agent-builder` slash command |
| **Purpose** | Create or migrate agents to D12 unified template |
| **Approach** | FACILITATION, not generation (BMAD pattern) |
| **Steps** | 6 sequential steps (adapted from BMAD's 11) |
| **Entry Point** | Compulsory collaborative discovery |

---

## Core Principles (From BMAD)

```
┌─────────────────────────────────────────────────────────────────┐
│                    WORKFLOW PRINCIPLES                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. FACILITATION, NOT GENERATION                                │
│     → Workflow GUIDES, user PROVIDES content                    │
│     → Claude assists discovery, doesn't assume                  │
│                                                                 │
│  2. STRICT SEQUENTIAL ENFORCEMENT                               │
│     → No skipping steps                                         │
│     → Each step builds on previous                              │
│     → Save progress before advancing                            │
│                                                                 │
│  3. COLLABORATIVE AT EVERY STEP                                 │
│     → Ask questions, user provides answers                      │
│     → Agent emerges from USER's knowledge                       │
│     → Iterate until user is satisfied                           │
│                                                                 │
│  4. QUALITY OVER SPEED                                          │
│     → Thoroughness ensures good agents                          │
│     → A poorly-defined agent is worse than no agent             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Workflow Modes

### Mode 1: CREATE (New Agent)
- Full collaborative discovery at every step
- User doesn't know exactly what they want yet
- PM helps clarify and refine through questions

### Mode 2: MIGRATE (Rebuild Existing Agent)
- Read existing agent, present to user
- Ask: "Is this still accurate? Any changes needed?"
- If no changes: Abbreviate steps 2-4 (pre-fill, user confirms)
- If changes: Full discovery on changed aspects
- Steps 5-6 always full (validation required)

---

## Step-by-Step Specification

---

## STEP 1: COLLABORATIVE DISCOVERY

**Purpose:** Entry point - PM facilitates brainstorming with user to define agent concept

**This step is COMPULSORY - not optional**

### 1.1 Mode Detection

```
IF user provides existing agent path:
  → MIGRATE mode
  → Read existing agent file
  → Present: "I found agent [name]. Let me show you what it currently does..."
  → Present summary of: purpose, capabilities, domain
  → Ask: "Would you like to keep this as-is and just convert to D12 format,
          or would you like to improve/change anything?"

IF user starts fresh:
  → CREATE mode
  → Begin discovery questions
```

### 1.2 Discovery Questions (CREATE mode)

Ask these questions conversationally, not as a form:

1. **Problem Space**
   - "What problem does this agent solve?"
   - "Who will use this agent?"
   - "What's frustrating about NOT having this agent?"

2. **Domain Exploration**
   - "What domain or specialty does this agent cover?"
   - "What makes this agent's expertise unique?"
   - "What specific tasks should it handle?"

3. **Success Criteria**
   - "How will you know this agent is doing a good job?"
   - "What would a successful interaction look like?"

4. **Boundaries**
   - "What should this agent NOT do?"
   - "When should it refuse or escalate?"

### 1.3 Discovery Output

Document the following (save to working file):

```yaml
# Agent Discovery - {working_name}
mode: create | migrate
source_file: [path if migrate mode]

concept:
  problem_solved: [user's words]
  primary_users: [who uses it]
  unique_value: [what makes it special]
  domain: [area of expertise]
  key_tasks: [list of specific tasks]
  success_criteria: [how to know it's working]
  boundaries: [what it should not do]
```

### 1.4 Step Completion

Present summary to user:

```
Based on our discussion, here's what I understand:

[Agent Name] will be a [domain] specialist that helps [users] with [problem].

Key capabilities:
- [task 1]
- [task 2]
- [task 3]

It will NOT: [boundaries]

Does this capture what you're looking for?
```

**Menu:**
- [A] Let's explore this deeper (Advanced Elicitation)
- [R] I want to revise something
- [C] Continue to Step 2

---

## STEP 2: AGENT CLASSIFICATION

**Purpose:** Determine agent_type, module, and model based on discovery

### 2.1 Agent Type Selection

Present the 10 agent_types with descriptions:

| Type | Description | Use When |
|------|-------------|----------|
| `engineer` | Implementation specialist | Agent writes/modifies code |
| `architect` | Design and structure | Agent designs systems/architecture |
| `qa` | Testing and quality | Agent tests, validates, ensures quality |
| `security` | Security analysis | Agent handles security concerns |
| `research` | Investigation and analysis | Agent researches, investigates, explores |
| `ops` | Operations and deployment | Agent handles DevOps, deployment, infra |
| `creative` | Creative and ideation | Agent brainstorms, creates content |
| `workflow` | Process management | Agent manages processes, coordinates work |
| `orchestrator` | Multi-agent coordination | Agent delegates to other agents |
| `specialist` | Narrow domain expert | Agent has very specific expertise |

Ask: "Based on [agent concept], which type best fits?"

### 2.2 Module Selection

Present available modules:

| Module | Domain | Examples |
|--------|--------|----------|
| `bmm` | Business Method | dev, pm, sm, analyst, architect |
| `cis` | Creative & Innovation | storyteller, brainstorming-coach |
| `bmgd` | Game Development | game-dev, game-designer |
| `core` | Core Orchestration | bmad-master |
| `advanced` | Advanced Specialists | code-archaeologist, refactor-specialist |
| `security` | Security Research | security, bypass-validator |
| `hooking` | Android Hooking | dobby-hook-master, jni-bridge-master |
| `utils` | Utilities | documentation-writer, test-guardian |

Ask: "Which module should [agent name] belong to?"

### 2.3 Model Selection

| Model | Use When |
|-------|----------|
| `opus` | Complex reasoning, architecture decisions |
| `sonnet` | Standard tasks, most agents (default) |
| `haiku` | Fast, simple tasks |

Ask: "What complexity level does this agent need?"

### 2.4 Classification Output

```yaml
classification:
  agent_type: [selected]
  module: [selected]
  model: [selected]
  rationale: [why these choices]
```

**Menu:**
- [A] Let's reconsider these choices
- [R] I want to change something
- [C] Continue to Step 3

---

## STEP 3: BUILD FRONTMATTER (L1)

**Purpose:** Collaboratively define all frontmatter fields

### 3.1 Name Generation

Format: `module:agent-name`

Examples:
- `bmm:dev`
- `cis:storyteller`
- `security:bypass-validator`

Ask: "What should we name this agent? (Will be `[module]:[name]`)"

### 3.2 Description Crafting

**Rules:**
- 150-300 characters
- NO `<example>` tags (those go in ## When to Use)
- Format: "Use this agent when [trigger]. PROACTIVELY use for [scenarios]. Specializes in [capabilities]."

Collaborate with user:
- "Let's write a description that helps PM know when to route tasks to this agent."
- Draft together, iterate until right length and clarity

### 3.3 Tags Selection

**Rules:**
- 5-10 searchable keywords
- Include: domain terms, action words, technologies

Ask: "What keywords should help find this agent?"

### 3.4 Triggers Definition

**Rules:**
- 2-5 explicit activation phrases
- What user might say that should invoke this agent

Ask: "What phrases would indicate someone needs this agent?"

### 3.5 Frontmatter Output

```yaml
---
name: [module]:[agent-name]
description: >-
  [150-300 chars, collaborative result]
version: "1.0.0"
model: [selected]
agent_type: [selected]
tags:
  - [tag1]
  - [tag2]
  # ... 5-10 tags

module: [module]
triggers:
  - "[phrase 1]"
  - "[phrase 2]"
  # ... 2-5 triggers

# Optional fields as needed:
# capabilities:
#   tools: [Read, Write, Edit, Bash, Grep, Glob]
#   tier: standard
# languages: [python, kotlin]
# frameworks: [django, fastapi]
# orchestrates: [dev, qa, security]
# authorization: educational-research
---
```

**Menu:**
- [A] Let's refine this further
- [R] I want to change something
- [C] Continue to Step 4

---

## STEP 4: BUILD BODY SECTIONS (L2)

**Purpose:** Collaboratively build each body section

### 4.1 Section: Expertise

**Rules:**
- 2-5 sentences
- NOT a repeat of description
- Explains WHY this agent is exceptional
- Include domain depth, unique approach

Ask:
- "What makes this agent's expertise deep?"
- "What experience or achievements back this up?"
- "What's unique about this agent's approach?"

### 4.2 Section: Identity

**Rules:**
- 1-3 sentences
- Clear role definition
- NO persona fluff ("You are an elite veteran...")

Ask:
- "In one sentence, what IS this agent?"

### 4.3 Section: When to Use

**Rules:**
- Include 2-4 `<example>` blocks
- Show positive AND negative examples
- Move examples from description here

Format:
```markdown
## When to Use

<example>
Context: [situation]
User: "[what user might say]"
Agent: [how agent responds/what it does]
</example>

<example>
Context: When NOT to use this agent
User: "[what user might say]"
Agent: This is [other domain] - delegate to [other-agent] instead
</example>
```

Ask:
- "Give me an example of when someone should use this agent"
- "Give me an example of when they should NOT use this agent"

### 4.4 Section: Core Capabilities

**Rules:**
- 8-15 bullet points
- Format: `**[Capability]:** [Brief description]`

Ask:
- "What are the key things this agent can do?"
- Iterate through capabilities together

### 4.5 Section: Domain-Specific Sections

**Based on agent_type:**

| Type | Recommended Sections |
|------|---------------------|
| engineer | Workflows, Patterns, Anti-Patterns |
| architect | Design Principles, Trade-offs |
| qa | Testing Strategies, Coverage Requirements |
| security | Security Protocols, Detection Methods |
| creative | Creative Methods, Techniques |
| workflow | Process Steps, Checkpoints |
| orchestrator | Delegation Patterns, Routing Rules |
| specialist | Technical Reference, Implementation Details |

Ask: "What domain-specific guidance should this agent have?"

### 4.6 Section: Boundaries

**Rules:**
- Clear refusal conditions
- Format: `**REFUSE:** [Condition] → [Why and what to do instead]`

Ask:
- "When should this agent refuse to help?"
- "When should it escalate instead?"

### 4.7 Section: Tool Awareness

**Rules:**
- Graceful degradation when tools unavailable
- Format: `If [Tool] unavailable → [Fallback strategy]`

Ask:
- "What tools does this agent use?"
- "What should it do if those tools aren't available?"

### 4.8 Section: Memory Integration (Optional)

**Only if agent should learn from interactions**

Ask: "Should this agent remember things between sessions?"

### 4.9 Body Output

Complete markdown body following D12 template structure.

**Menu:**
- [A] Let's refine sections further
- [R] I want to revise a section
- [C] Continue to Step 5

---

## STEP 5: VALIDATION

**Purpose:** Verify D12 compliance before output

### 5.1 Structural Validation (Deterministic)

Run these checks:

| Check | Requirement | Status |
|-------|-------------|--------|
| Frontmatter parses | Valid YAML | ☐ |
| Required fields | name, description, version, model, agent_type, tags | ☐ |
| Description length | 150-300 characters | ☐ |
| No examples in description | No `<example>` tags | ☐ |
| agent_type valid | One of 10 types | ☐ |
| Tags count | 5-10 keywords | ☐ |
| Token count | 1,650-2,975 tokens | ☐ |
| Line count | 600-900 lines | ☐ |

### 5.2 Section Validation

| Check | Requirement | Status |
|-------|-------------|--------|
| ## Expertise exists | Not duplicate of description | ☐ |
| ## Identity exists | 1-3 sentences, no persona fluff | ☐ |
| ## When to Use exists | 2-4 `<example>` blocks | ☐ |
| ## Core Capabilities exists | 8-15 bullet points | ☐ |
| ## Boundaries exists | Clear refusal rules | ☐ |
| ## Tool Awareness exists | Graceful degradation | ☐ |
| No session_config | Removed per D12 | ☐ |
| No response_gate | Removed per D12 | ☐ |
| No menu section | Removed per D12 | ☐ |

### 5.3 Issue Resolution

If any check fails:
- Present issue conversationally (not technical error)
- Propose fix collaboratively
- Apply fix with user approval
- Re-validate

### 5.4 Validation Output

```
✅ Validation Complete

Structural Checks: 8/8 passed
Section Checks: 6/6 passed
Token Count: [X] tokens (within 1,650-2,975 budget)
Line Count: [X] lines (within 600-900 range)

Agent is D12 compliant and ready for output.
```

**Menu:**
- [R] I want to revise something before saving
- [C] Continue to Step 6

---

## STEP 6: OUTPUT & COMPLETION

**Purpose:** Write agent file and provide next steps

### 6.1 File Output

Path: `unified/agents/[module]/[name].md`

Example: `unified/agents/bmm/dev.md`

Write complete agent file:
- Frontmatter (from Step 3)
- Body sections (from Step 4)

### 6.2 L1 Aggregation Update

Remind: "Run `extract_l1_metadata.py` to update agent-index.yaml for PM routing (D13)"

### 6.3 Completion Summary

```
🎉 Agent Created Successfully!

📄 File: unified/agents/[module]/[name].md
📊 Stats: [X] tokens, [Y] lines
✅ D12 Compliant

[Agent Name] is ready to:
- [capability 1]
- [capability 2]
- [capability 3]

Next Steps:
1. Review the generated file
2. Run extract_l1_metadata.py to update routing index
3. Test the agent with sample tasks
```

### 6.4 Workflow Complete

Mark workflow as complete.

---

## Migration Mode Adaptations

When in MIGRATE mode, steps adapt as follows:

| Step | Adaptation |
|------|------------|
| Step 1 | Read existing file, present summary, ask for changes |
| Step 2 | Pre-fill from existing, user confirms or modifies |
| Step 3 | Pre-fill frontmatter from existing, user refines |
| Step 4 | Transform existing content to D12 sections, user reviews |
| Step 5 | Full validation (no shortcuts) |
| Step 6 | Same as creation |

Key difference: User REVIEWS pre-filled content rather than building from scratch.

---

## Workflow Files Structure

```
Claude-Hybrid/
├── .claude/
│   └── commands/
│       └── unified-agent-builder.md    # Slash command entry
└── unified/
    ├── workflows/
    │   └── unified-agent-builder/
    │       ├── workflow.md              # Main workflow definition
    │       └── steps/
    │           ├── step-01-discovery.md
    │           ├── step-02-classify.md
    │           ├── step-03-frontmatter.md
    │           ├── step-04-body.md
    │           ├── step-05-validate.md
    │           └── step-06-output.md
    └── agents/
        ├── bmm/
        ├── cis/
        ├── bmgd/
        └── [other modules]/
```

---

## Comparison: BMAD vs Unified-Agent-Builder

| Aspect | BMAD (11 steps) | Unified (6 steps) |
|--------|-----------------|-------------------|
| Entry | Optional brainstorm | Compulsory discovery |
| Types | Simple/Expert/Module | 10 agent_types |
| Output | YAML → XML compiled | Markdown with frontmatter |
| Persona | 4 fields (role, identity, communication_style, principles) | D12 sections (Expertise, Identity, etc.) |
| Compilation | Required | Not needed |
| Validation | BMAD checklist | D12 13-point checklist |
| Facilitation | ✅ Full | ✅ Full (preserved) |
| Sequential | ✅ Strict | ✅ Strict (preserved) |

**Preserved from BMAD:**
- Facilitation pattern
- Strict sequential enforcement
- Collaborative at every step
- Quality over speed
- Validation before output

**Adapted for Claude-Hybrid:**
- 6 steps instead of 11 (consolidated)
- D12 template structure
- 10 agent_types instead of 3
- Markdown output (no compilation)
- D12 validation checklist

---

*Specification created Session 5 | 2025-12-11 | Draft for Review*
