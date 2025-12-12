# Session 8 Gap Analysis - Claude-Hybrid Architecture

**Date:** 2025-12-12
**Purpose:** Document all gaps identified in D1-D10 that must be filled before creating unified architectural blueprint
**Status:** Gaps Identified - Awaiting Resolution

---

## Executive Summary

Session 8 deployed 5 specialized agents to analyze D1-D10 for blueprint completeness. The analysis found that while 162 questions are decided, several critical implementation details are missing or underspecified.

**Critical Finding:** Agent Classification is at only 10% coverage - this is a BLOCKER for implementation.

---

## Gap Analysis Results by Decision Set

### D1-D2: Control Layer & PM Agent

| Component | Coverage | Gap Description |
|-----------|----------|-----------------|
| PM Agent/Orchestrator | 70% | PM_INSTRUCTIONS.md structure not fully specified |
| Hook System | 60% | Only 4/7 hook events have full input/output contracts |
| Circuit Breakers | 50% | CB#1-CB#8 definitions and violation criteria not specified |

**Questions Needed:**
- Q: What is the complete structure of PM_INSTRUCTIONS.md?
- Q: What are the input/output contracts for all 7 hook events?
- Q: What are the explicit definitions for CB#1-CB#8?

### D3-D4: State & Agent Management

| Component | Coverage | Gap Description |
|-----------|----------|-----------------|
| Frontmatter SSOT | 70% | Complete field list not specified |
| Delegation Chain | 40% | How PM routes to agents not fully defined |
| Agent Classification | **10%** | **CRITICAL: 87 agents not classified into tiers** |
| Tiering Criteria | 60% | Criteria for Tier 1/2/3 placement incomplete |

**Questions Needed:**
- Q: What are all required frontmatter fields for state tracking?
- Q: What is the complete delegation chain from PM to specialist agents?
- Q: What criteria determine Tier 1 vs Tier 2 vs Tier 3 classification?
- Q: How are the 87 agents classified? (This may be implementation, not architecture)

### D5-D6: Progressive Disclosure & System Prompt

| Component | Coverage | Gap Description |
|-----------|----------|-----------------|
| Progressive Disclosure | YES | COMPLETE |
| Process Handoff | YES | COMPLETE |
| System Prompt Assembly | PARTIAL | 10 sections not fully detailed |
| 12-Phase Initialization | PARTIAL | Phase details missing |

**Questions Needed:**
- Q: What are the exact 10 sections of system prompt assembly?
- Q: What happens in each of the 12 initialization phases?

### D7-D8: Services & Token Management

| Component | Coverage | Gap Description |
|-----------|----------|-----------------|
| MCP Aggregator | YES | COMPLETE |
| Advisory Pattern | NO | JSON format for routing hints not specified |
| TokenCountingService | NO | 3-tier fallback (API → tiktoken → char) not specified |
| ContextThresholdManager | PARTIAL | Actions at 70%/85%/95% thresholds not specified |
| Agent Template | YES | COMPLETE |

**Questions Needed:**
- Q: What is the JSON schema for advisory pattern responses?
- Q: What is the TokenCountingService 3-tier fallback specification?
- Q: What actions does ContextThresholdManager take at 70%, 85%, 95%?

### D9-D10: Workflow & Agent Unification

| Component | Coverage | Status |
|-----------|----------|--------|
| All 6 Components | YES | **FULLY SPECIFIED** |

No gaps identified in D9-D10.

---

## Gap-to-D* Mapping

| Gap | Target D* | Priority |
|-----|-----------|----------|
| PM_INSTRUCTIONS.md structure | D2 | HIGH |
| Hook event contracts (7 events) | D2 | HIGH |
| Circuit Breaker definitions CB#1-CB#8 | D2 | HIGH |
| Frontmatter SSOT field list | D3 | MEDIUM |
| Delegation chain specification | D3 | MEDIUM |
| Agent Classification criteria | D3 | **CRITICAL** |
| Tiering criteria (Tier 1/2/3) | D3 | HIGH |
| System Prompt 10 sections | D6 | MEDIUM |
| 12-Phase Initialization | D6 | MEDIUM |
| Advisory Pattern JSON schema | D7 | HIGH |
| TokenCountingService spec | D7 | HIGH |
| ContextThresholdManager actions | D7 | MEDIUM |

---

## Proposed New Questions

### For D2-QUESTIONS.md

```markdown
### Q21: PM_INSTRUCTIONS.md Structure
What is the complete structure and section list for PM_INSTRUCTIONS.md?

Options:
- A: 10-section structure (from D6-Q6)
- B: Minimal 5-section structure
- C: Modular composition from fragments
- D: Single monolithic file

### Q22: Hook Event Input/Output Contracts
What are the input/output contracts for all 7 hook events?

Options:
- A: Typed contracts per event (PreToolUse, PostToolUse, Stop, etc.)
- B: Generic event envelope with event-specific payload
- C: Callback-style with context object
- D: Message-passing with defined schemas

### Q23: Circuit Breaker Definitions (CB#1-CB#8)
What are the explicit definitions and violation criteria for CB#1-CB#8?

Options:
- A: Security breakers (CB#1-CB#3), Quality breakers (CB#4-CB#6), Process breakers (CB#7-CB#8)
- B: Tiered severity (HARD breakers vs SOFT breakers)
- C: Domain-specific breakers per agent type
- D: Unified breaker with configurable rules
```

### For D3-QUESTIONS.md

```markdown
### Q21: Agent Classification Criteria
What criteria determine Tier 1 vs Tier 2 vs Tier 3 agent classification?

Options:
- A: Frequency-based (daily use = Tier 1, weekly = Tier 2, rare = Tier 3)
- B: Criticality-based (core workflows = Tier 1, supporting = Tier 2, specialized = Tier 3)
- C: Dependency-based (orchestrators = Tier 1, engineers = Tier 2, specialists = Tier 3)
- D: Hybrid criteria combining frequency + criticality + dependency
```

### For D7-QUESTIONS.md

```markdown
### Q17: Advisory Pattern JSON Schema
What is the JSON schema for MCP advisory pattern responses?

Options:
- A: {suggested_agent, suggested_skills, reasoning, confidence}
- B: {agent_id, confidence_score, alternatives[], rationale}
- C: {recommendation: {agent, skills}, metadata: {confidence, source}}
- D: Simple {agent: string, confidence: float}

### Q18: TokenCountingService Specification
What is the TokenCountingService 3-tier fallback specification?

Options:
- A: Anthropic API → tiktoken → character estimate (÷4)
- B: tiktoken primary → API validation → character fallback
- C: Character estimate always (fastest, least accurate)
- D: Configurable tier preference per environment

### Q19: ContextThresholdManager Actions
What actions does ContextThresholdManager take at each threshold?

Options:
- A: 70% = warn, 85% = summarize, 95% = force-compact
- B: 70% = log, 85% = warn user, 95% = block new content
- C: Progressive disclosure adjustment (reduce L2 loading)
- D: Configurable actions per threshold
```

---

## Resolution Path

1. **Immediate:** Present this gap mapping to user for validation
2. **If approved:** Add proposed questions to appropriate D* files
3. **Decide questions:** Work through each new question with user
4. **After all gaps filled:** Create unified architectural blueprint
5. **Blueprint complete:** Proceed to implementation phase

---

## User Philosophy (Reference)

> "Like building a house, an engineer needs the architectural blueprint first. Everything needs to be in the decision files entirely, then proceed to the phase where everything is drawn as one whole architect file."

---

*Document created Session 9 | 2025-12-12 | Gap analysis from Session 8*
