# D9 Session Roundup

**Decision Area:** Path Variables & File Structure
**Status:** Not Started
**Questions:** 0/20 complete

## Current Position
- Starting fresh with Q1
- No decisions made yet

## Question Categories

### Q1-Q4: 4-Level Variable Cascade
- Q1: Adopt 4-level cascade from Personal BMAD?
- Q2: System-level variable resolution method
- Q3: Framework-level absolute vs relative paths
- Q4: Legacy variable alias handling

### Q5-Q8: Complete File Structure Layout
- Q5: Root structure for global installation
- Q6: Module directory organization
- Q7: Agent plugin file locations
- Q8: Project-local output directory structure

### Q9-Q12: Variable Resolution Engine
- Q9: Runtime resolution mechanism
- Q10: Variable resolution order
- Q11: Circular/undefined reference handling
- Q12: Conditional logic support in variables

### Q13-Q16: Auto-Creation Behavior
- Q13: Project output directory auto-creation timing
- Q14: Framework directory auto-creation on first use
- Q15: Missing intermediate directory handling
- Q16: README/.gitkeep placeholder strategy

### Q17-Q20: Hybrid Global/Local Model Details
- Q17: Global/local boundary enforcement
- Q18: Project override of global components
- Q19: Framework update propagation to projects
- Q20: Project state references vs copies

## Source Documents Referenced
1. `/home/president/bmad-systems/personal bmad/BMAD-PERSONAL-ARCHITECTURE.md`
   - Section 2: Path Variable System (Resolution Hierarchy, Resolution Engine)
   - Section 3: File Structure (Complete Directory Layout)

2. `/home/president/bmad-systems/bmad-method-complete-analysis/shards/09-CONFIGURATION.md`
   - 4-Level Resolution Cascade
   - Variable Substitution System
   - Configuration Output Structure

## Key Concepts from Sources

### Path Variable Resolution Hierarchy (Personal BMAD)
```
Level 1: SYSTEM VARIABLES (Literals/Runtime)
  {home}, {project-root}

Level 2: FRAMEWORK VARIABLES (Global - Fixed)
  {bmad-framework-root}, {framework-*-root}

Level 3: PROJECT VARIABLES (Local - Dynamic)
  {output-root}, {project-*}

Level 4: LEGACY VARIABLES (Backward Compatibility)
  bmad_path, output_folder
```

### Hybrid Architecture Model
- Framework = GLOBAL -> Lives in `~/.claude/`, shared across all projects
- Outputs = LOCAL -> Lives in `{project-root}/bmad/`, isolated per project
- Agents = Claude Plugins -> Auto-discovered, instant spawn via Task tool

### Auto-Creation Pattern
- Project directories auto-created when workflows write outputs
- Workflow detects `{project-root}` from current working directory
- Resolves paths like `{output-root}/epics`
- Creates directories via `mkdir -p` when writing first file

## Resume Instructions
1. Read D9-QUESTIONS.md
2. Present Q1 options to President
3. Record decision in progress.txt
4. Update state.json

## Context for Next Session
This workspace is INDEPENDENT. You can work on D9 while other Claude sessions work on D6-D8, D10 simultaneously.

## Related Decisions (Avoid Overlap)
- D2: Enforcement Mechanism (hooks, circuit breakers)
- D3: Multi-Agent Strategy (agent selection, communication)
- D4: State Tracking (workflow state, progress tracking)
- D5: Context Management (200k limit, loading strategies)

D9 focuses specifically on:
- Path variable definitions and resolution
- Directory structure layout
- Auto-creation behavior
- Global/local boundary management
