# D10 Session Roundup

**Decision Area:** Workflow Engine & Lifecycle
**Status:** Not Started
**Questions:** 0/20 complete

## Current Position
- Starting fresh with Q1
- No decisions made yet

## Question Categories

### Q1-Q4: workflow.xml Universal Executor
- How to implement universal workflow execution
- Execution mandates enforcement
- Template-output save-and-pause pattern
- Normal vs YOLO execution modes

### Q5-Q8: Deep Merge Customization System
- Deep merge implementation for agent customization
- Customization file locations
- Customizable property scope
- Conflict resolution across tiers

### Q9-Q12: Content Injection System
- Sub-agent hint injection
- Dynamic content types
- Protocol discovery and invocation
- Dynamic persona injection

### Q13-Q16: 4-Phase Lifecycle Enforcement
- Phase gate enforcement strategy
- Skip/override handling
- Prerequisite workflow enforcement
- Phase completion validation

### Q17-Q20: 3 Tracks Selection Logic
- Project level detection
- Track selection mechanism
- workflow-init status file creation
- Path file structure and selection

## Source Documents
- `/home/president/bmad-systems/bmad-method-complete-analysis/shards/02-ARCHITECTURE-CORE.md`
- `/home/president/bmad-systems/bmad-method-complete-analysis/shards/05-WORKFLOWS-SYSTEM.md`
- `/home/president/bmad-systems/bmad-method-complete-analysis/shards/14-WORKFLOW-PATHS.md`
- `/home/president/bmad-systems/bmad-method-complete-analysis/shards/15-CUSTOMIZATION-EXTENSION.md`

## Resume Instructions
1. Read D10-QUESTIONS.md
2. Present Q1 options to President
3. Record decision in progress.txt
4. Update state.json

## Context for Next Session
This workspace is INDEPENDENT. You can work on D10 while other Claude sessions work on D6-D9 simultaneously.

## Key Concepts from Sources

### Universal Workflow Executor (workflow.xml)
- Single XML file executes ANY workflow
- 5 core mandates for execution
- Step-by-step processing with exact order
- Template-output triggers save-pause-interact cycle
- YOLO mode bypasses confirmations

### Deep Merge System
- Objects: recursive merge
- Arrays: append new items
- Scalars: override with new value
- customize.yaml per-agent customization

### 4-Phase Lifecycle
- Phase 0: Discovery (optional/required by track)
- Phase 1: Planning (PRD, UX)
- Phase 2: Solutioning (Architecture, Stories)
- Phase 3: Implementation (Sprint, Dev)
- Prerequisites for brownfield (document-project)

### 3 Tracks Architecture
- Quick Flow: Bug fixes, small features (L0-L1)
- BMAD Method: Products, platforms (L2-L3)
- Enterprise: Full governance (L4)
- greenfield vs brownfield variants

## Non-Overlapping Topics
- D2 covers Enforcement Mechanism (hooks, circuit breakers)
- D3 covers Multi-Agent Strategy (collaboration, selection)
- D4 covers State Tracking (persistence, resumption)
- D5 covers Context Management (token budgets, loading)
- D10 covers Workflow Engine & Lifecycle (execution, phases, tracks)
