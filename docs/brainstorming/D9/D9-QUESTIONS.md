# D9: Path Variables & File Structure - Question Set

**Decision:** How does Claude-Hybrid manage path variables and file structure?
**Status:** ✅ COMPLETE (19/19 DECIDED)
**Generated:** 2025-12-10 (Session X)
**Updated:** 2025-12-11 - Removed 5 redundant questions (previously 20, now 15)
**Sources:** Personal BMAD architecture (BMAD-PERSONAL-ARCHITECTURE.md), BMAD Method configuration (09-CONFIGURATION.md)

---

## Redundancy Audit Notes

The following questions were removed due to overlap with prior D2-D5 decisions:

| Removed | Topic | Overlaps With | Reason |
|---------|-------|---------------|--------|
| Q1 (old) | 4-level cascade adoption | D4-Q16 | Variable resolution cascade already decided in D4 |
| Q9 (old) | Path variable resolution mechanism | D2-Q20 | Hybrid resolution (hooks for System/Path) decided in D2 |
| Q17 (old) | Global/local boundary enforcement | D2 | Enforcement framework covers boundary enforcement |
| Q18 (old) | Project override capability | D3-Q9/Q17 | Priority cascade (Project>User>System) decided in D3 |
| Q15 (current) | Framework update propagation | D5-Q8 | Session boundary loading semantics already decided |

---

## Checkpoint Status

| Question | Status | Answer |
|----------|--------|--------|
| Q1 | **DECIDED** | Option C: Hybrid Resolution (env + Claude Code context) |
| Q2 | **DECIDED** | Option C: Variable-Chained ({home}/.claude/bmad) |
| Q3 | **DECIDED** | Option A: Direct Aliasing (bmad_path = {bmad-framework-root}) |
| Q4 | **DECIDED** | Option A: Personal BMAD Structure (~/.claude/{plugins,bmad,workflows,commands}/) |
| Q5 | **DECIDED** | Option A: Module-first Organization ({module}/config.yaml, agents/, workflows/) |
| Q6 | **DECIDED** | Option A: Claude Code Plugin Path (~/.claude/plugins/.../agents/) - 99.4% perf |
| Q7 | **DECIDED** | Option A: Fixed Structure ({project-root}/bmad/{epics,stories,analysis,blueprints,research}/) |
| Q8 | **DECIDED** | Option C: Two-Phase Resolution (D2-Q20 PRE-SELECTS) |
| Q9 | **DECIDED** | HYBRID A+C: Tier-Aware Handling |
| Q10 | **DECIDED** | Option A: No Conditionals |
| Q11 | **DECIDED** | Option A: On First Write (Lazy) |
| Q12 | **DECIDED** | Option B: Installer-Required (D6-Q5 PRE-SELECTS) |
| Q13 | **DECIDED** | Option A: Full Path Creation (mkdir -p) |
| Q14 | **DECIDED** | Option A: No Placeholders (lazy = never empty) |
| Q15 | **DECIDED** | Option A: Reference-Only (Store paths, load on-demand via Read tool) |
| Q16 | **DECIDED** | Option D: Layered Styles (System + User + Project cascade) |
| Q17 | **DECIDED** | Option E: Hybrid (Strict for critical, Flexible for exploratory) |
| Q18 | **DECIDED** | Option B: Extended Mapping (Base + Cross-Phase Validation) |
| Q19 | **DECIDED** | Option E: Multi-Method (Docs + Checklists + Approval for Critical, Automated for All) |

---

## Q1-Q3: Variable Resolution Levels

### Q1: How should System-level variables be resolved?
System variables are the foundation: `{home}` and `{project-root}`.

Options:
- A: Runtime literals - `{home}` resolved from `$HOME` env var, `{project-root}` from `$(pwd)` at invocation time
- B: Configuration-defined - Both variables explicitly defined in a root config file, no runtime detection
- C: Hybrid resolution - `{home}` from env var (stable), `{project-root}` from Claude Code's working directory context
- D: Context-injected - Variables injected by SessionStart hook based on detected environment, no manual resolution

### Q2: Should Framework-level variables use absolute or relative paths internally?
Framework variables like `{bmad-framework-root}` reference global installation.

Options:
- A: Absolute paths only - All framework variables resolve to full absolute paths (e.g., `/home/president/.claude/bmad`)
- B: Home-relative paths - Framework variables use `~/.claude/` notation, expanded at resolution time
- C: Variable-chained - Framework variables reference System variables (e.g., `{home}/.claude/bmad`), resolved via cascade
- D: Mixed approach - Root framework path is absolute, sub-paths are relative within framework (e.g., `{bmad-framework-root}/core/protocols`)

### Q3: How should Legacy variable aliases be handled?
Legacy variables (`bmad_path`, `output_folder`) provide backward compatibility.

Options:
- A: Direct aliasing - Legacy variables are simple aliases to modern variables (e.g., `bmad_path` = `{bmad-framework-root}`)
- B: Deprecated warnings - Support legacy variables but emit warnings encouraging migration to modern names
- C: Translation layer - Maintain a mapping file that translates legacy to modern at load time
- D: No legacy support - Drop legacy variables entirely, require all configs to use modern variable names

---

## Q4-Q7: Complete File Structure Layout

### Q4: What should be the root structure for Claude-Hybrid's global installation?
Personal BMAD uses `~/.claude/` with plugins, bmad, workflows, commands subdirectories.

Options:
- A: Personal BMAD structure - Adopt `~/.claude/{plugins,bmad,workflows,commands}/` layout exactly
- B: Simplified structure - Use `~/.claude/hybrid/{agents,config,workflows}/` with fewer top-level directories
- C: XDG-compliant - Use `~/.config/claude-hybrid/` for config, `~/.local/share/claude-hybrid/` for data
- D: Merged structure - Single `~/.claude-hybrid/` directory with all components (agents, config, workflows, commands)

### Q5: How should module directories be organized within the framework?
Personal BMAD organizes by module: core, bmm, cis, android, hooking, security, etc.

Options:
- A: Module-first organization - `{framework-root}/{module}/` with config.yaml, agents/, tasks/ per module
- B: Type-first organization - `{framework-root}/agents/`, `{framework-root}/workflows/`, `{framework-root}/configs/` with module subdirs inside
- C: Flat module structure - `{framework-root}/` contains module configs directly, no nesting (e.g., `bmm-config.yaml`)
- D: Hybrid organization - Core components type-first, domain modules organized module-first

### Q6: Where should agent plugin files be located?
Personal BMAD uses `~/.claude/plugins/marketplaces/local/plugins/{module}/agents/`.

Options:
- A: Claude Code plugin path - Keep `~/.claude/plugins/marketplaces/local/plugins/{module}/agents/` for native auto-discovery
- B: Framework-local agents - Move to `{bmad-framework-root}/agents/{module}/` for simpler structure
- C: Dual location - Plugin path for auto-discovered agents, framework path for orchestrated-only agents
- D: Single agents directory - All agents in `~/.claude/agents/{module}/` regardless of invocation method

### Q7: How should project-local output directories be structured?
Personal BMAD uses `{project-root}/bmad/` with epics, stories, analysis, blueprints, research subdirs.

Options:
- A: Fixed structure - Predefined subdirectories (epics, stories, analysis, blueprints, research) auto-created
- B: Workflow-driven structure - Directories created based on which workflows are executed (only create what's used)
- C: Configurable structure - Project config defines which output directories to create and their names
- D: Flat output - All outputs in single `{project-root}/bmad/` directory with naming conventions instead of subdirs

---

## Q8-Q11: Variable Resolution Engine

### Q8: In what order should variable references be resolved?
The cascade defines priority, but resolution order affects availability.

Options:
- A: Top-down eager - Resolve System first, then Framework, then Project, then Legacy (all upfront before workflow)
- B: Lazy on-demand - Resolve variables only when referenced, caching results for subsequent references
- C: Two-phase resolution - First pass resolves System+Framework (static), second pass resolves Project+Runtime (dynamic)
- D: Single-pass with fallback - Attempt full resolution in one pass, fallback to literal if variable undefined

### Q9: How should circular or undefined variable references be handled?
E.g., `{var-a}` references `{var-b}` which references `{var-a}`.

Options:
- A: Fail-fast with error - Detect circular references during resolution, throw fatal error immediately
- B: Max-depth protection - Allow limited recursion depth (e.g., 10 levels), error if exceeded
- C: Undefined as literal - If variable is undefined, treat `{undefined-var}` as literal string (no substitution)
- D: Validation phase - Pre-validate all variable definitions before resolution, reject invalid configs at load time

### Q10: Should variable resolution support conditional logic?
E.g., `{output-root:?default-value}` or `{env:USE_LOCAL|{project-root}|{remote-root}}`.

Options:
- A: No conditionals - Variables are simple substitutions only, conditionals handled at workflow logic level
- B: Default value syntax - Support `{variable:-default}` style fallbacks for undefined variables
- C: Full conditional expressions - Support ternary-style `{condition?true-value:false-value}` in variable definitions
- D: External config conditionals - Conditionals defined in config files, not in variable syntax itself

### Q11: When should project output directories be auto-created?
Personal BMAD creates dirs via `mkdir -p` when first file is written.

Options:
- A: On first write - Directories created automatically when a workflow first writes to that path (lazy creation)
- B: On project initialization - All configured output directories created when `/bmad-init` or similar command runs
- C: On workflow start - Directories needed by the current workflow created at workflow initialization
- D: Never auto-create - Require manual directory creation, fail if directory doesn't exist

---

## Q12-Q14: Auto-Creation Behavior

### Q12: Should the framework directory structure be auto-created on first use?
First invocation of Claude-Hybrid may need to set up global directories.

Options:
- A: Full auto-creation - All framework directories created on first `bmad-master` invocation
- B: Installer-required - Explicit installation command (e.g., `bmad install`) must be run first
- C: Minimal auto-creation - Only essential directories auto-created, optional modules installed on demand
- D: Validation only - Check for required structure, provide clear error message if missing

### Q13: How should missing intermediate directories be handled?
E.g., writing to `{output-root}/epics/sprint-1/epic-001.md` when `sprint-1/` doesn't exist.

Options:
- A: Full path creation - Use `mkdir -p` equivalent to create all intermediate directories
- B: Single-level creation - Only create the immediate parent directory, error if grandparent missing
- C: Configurable depth - Config setting controls how many levels of directories can be auto-created
- D: Structured paths only - Only auto-create directories that match predefined structure patterns

### Q14: Should auto-creation include README or .gitkeep files?
Empty directories may not persist in git without placeholder files.

Options:
- A: No placeholders - Just create directories, let git/user handle tracking
- B: .gitkeep files - Add empty `.gitkeep` to auto-created directories for git tracking
- C: README.md files - Add descriptive `README.md` explaining the directory's purpose
- D: Configurable placeholders - Project config specifies which placeholder strategy to use

---

## Q15: Hybrid Global/Local Model Details (Borderline)

### Q15: Should project-local state reference global paths or maintain copies?
E.g., does project state file store `{bmad-framework-root}/workflows/...` or copy workflow content?

**NOTE:** Related to D2 enforcement framework decisions. This question addresses state storage strategy specifically.

Options:
- A: Reference-only - Project state stores paths/references to global files, loads on demand
- B: Copy-on-use - Global files are copied to project-local cache when first used, project uses copies
- C: Snapshot versioning - Project stores snapshot of global files at project init, explicit refresh updates
- D: Hybrid references - Static content (agents, workflows) referenced, dynamic content (configs) copied locally

### Q16: Where should output styles be deployed?
**Context:** Recent Claude-MPM changes renamed output styles and deploy them to `~/.claude/styles/` directory. This affects path variable definitions and style discovery.

Options:
- A: Dedicated styles directory - Deploy to `~/.claude/styles/` as separate top-level directory (Claude-MPM pattern).
- B: Framework-embedded styles - Deploy to `{bmad-framework-root}/styles/` within the framework structure.
- C: Project-local styles - Deploy to `{project-root}/.claude/styles/` for project-specific customization.
- D: Layered styles - System styles in `~/.claude/styles/`, project overrides in `{project-root}/.claude/styles/`.

---

## Questions: Gap Resolution - BMAD 4-Phase Workflow (Q17-Q19)

### Q17: How should Claude-Hybrid implement BMAD's 4-Phase Workflow Lifecycle?
**Context:** CORE-VISION.md:25 requires "4-Phase Lifecycle (Analysis → Planning → Solutioning → Implementation)". D2-Q15's "4-Phase Lifecycle" is HOOK phases (SessionStart/PreToolUse/PreCompact/Stop), NOT this workflow lifecycle.

Options:
- A: Strict Sequential - Phases must complete in order, no skipping
- B: Flexible Sequential - Default order, allow skipping with explicit override
- C: Parallel Phases - Some phases can run in parallel (e.g., Planning + early Solutioning)
- D: Iterative Phases - Allow returning to earlier phases based on findings
- E: Hybrid - Strict for critical workflows, flexible for exploratory

**CORE-VISION Reference:** Line 25

**✅ DECIDED: Option E - Hybrid (Strict for Critical, Flexible for Exploratory)**

**Decision Details:**
- **Confidence:** 8.3/10
- **Specialist Consensus:** 3/3 UNANIMOUS (Tech Lead 9/10, Research 8/10, Coder 8/10)
- **Binding Constraints Satisfied:** D2-Q15 (4-phase hook lifecycle), D2-Q16 (hybrid enforcement), D5-Q1 (strict sequential), D5-Q3 (frontmatter SSOT)
- **Industry Validation:** 63-78% success rate with hybrid models vs 24% for ad-hoc; 53-61% enterprise adoption
- **Implementation:** ~435-650 LOC total, 55-81% reuse, ~80-290 net new LOC
- **3-Year TCO:** ~$6,000-8,000

**Key Decisions:**
- Phase 1 (Analysis): OPTIONAL - can skip for brownfield projects
- Phase 2 (Planning): REQUIRED - mandatory for all workflows
- Phase 3 (Solutioning): TRACK-DEPENDENT - Quick Flow skips, BMad Method requires
- Phase 4 (Implementation): REQUIRED - full validation
- Iteration: Via correct-course workflow (structured return, not ad-hoc jumping)
- Progressive Proof: L1 → L1-L2 → L1-L3 → L1-L4

**Analogy (Highway System):** Phase 1 = scenic route (optional), Phase 2 = toll plaza (mandatory), Phase 3 = HOV lane (track-dependent), Phase 4 = destination (required). correct-course = U-turn ramp.

**Decided:** 2025-12-12, Session 81

---

### Q18: How should BMAD phases map to MPM validation layers?
**Context:** CORE-VISION.md:81-90 proposes explicit mapping:
- Phase 1 (Analysis) → Layer 1 (Schema Validation)
- Phase 2 (Planning) → Layer 2 (Business Rule Validation)
- Phase 3 (Solutioning) → Layer 3 (Execution Gates)
- Phase 4 (Implementation) → Layer 4 (Runtime Monitoring)

Options:
- A: Direct Mapping - Exactly as CORE-VISION proposes
- B: Extended Mapping - Base mapping + additional cross-phase validation
- C: Configurable Mapping - Project-level configuration of phase-layer relationships
- D: Adaptive Mapping - Mapping adjusts based on project complexity (L0-L4)

**CORE-VISION Reference:** Lines 81-90

**✅ DECIDED: Option B - Extended Mapping (Base + Cross-Phase Validation)**

**Decision Details:**
- **Confidence:** 9/10
- **Specialist Consensus:** 3/3 UNANIMOUS (Tech Lead 9/10, Research 9/10, Coder 9/10)
- **Binding Constraints Satisfied:** D2-Q15, D2-Q16, D2-Q21/Q22 (progressive proof), D5-Q1, D5-Q3, D10-Q1 (universal executor), D10-Q13 (hybrid validation) - ALL 7 CONSTRAINTS
- **Industry Validation:** GitLab CI, AWS Step Functions, Dagster all use progressive cumulative validation
- **Implementation:** ~505-850 LOC total, 55-88% reuse, ~60-400 net new LOC
- **3-Year TCO:** ~$6,000-9,000

**Extended Mapping Pattern (Cumulative):**
- Phase 1 (Analysis) → L1 only (schema validation)
- Phase 2 (Planning) → L1 + L2 (schema + business rules)
- Phase 3 (Solutioning) → L1 + L2 + L3 (+ execution gates)
- Phase 4 (Implementation) → L1 + L2 + L3 + L4 (all layers)

**Cross-Phase Validation:**
- Before Phase 3: Validate Phase 2 outputs
- Before Phase 4: Validate Phase 2 AND Phase 3 outputs
- Regression checks: Later phases validate earlier phase artifacts

**Analogy (Airport Security):** L1 = ticket check (structure exists), L2 = ID verification (policy compliance), L3 = security scan (gate clearance), L4 = in-flight monitoring (runtime). Extended adds cross-checkpoint verification.

**Decided:** 2025-12-12, Session 81

---

### Q19: What artifacts constitute "proof" for each phase transition?
**Context:** CORE-VISION.md:64,75 requires "Phased development with proof requirements" and "No phase proceeds without proof".

Options:
- A: Document-Based Proof:
  - Analysis→Planning: Validated requirements.md
  - Planning→Solutioning: Validated architecture.md
  - Solutioning→Implementation: Validated tech-spec.md
  - Implementation→Complete: Passing tests + code review
- B: Checklist-Based Proof - Each phase has completion checklist
- C: Approval-Based Proof - Human approval required at each gate
- D: Automated Proof - Automated validation scripts at each gate
- E: Multi-Method - Documents + checklists + approval for critical, automated for others

**CORE-VISION Reference:** Lines 64, 75

**✅ DECIDED: Option E - Multi-Method Proof**

**Decision Details:**
- **Confidence:** 8.5/10
- **Specialist Consensus:** 3/3 UNANIMOUS (Tech Lead 9/10, Research 8/10, Engineer 8.5/10)
- **Binding Constraints Satisfied:** D9-Q17 (Hybrid), D9-Q18 (Extended Mapping), D2-Q22 (Progressive Proof), D10-Q13 (Hybrid Validation), CORE-VISION:64,75
- **Industry Validation:** GitLab CI, GitHub Actions, AWS Step Functions, Temporal, Dagster all use multi-method proofs
- **Implementation:** ~440 LOC total, 65% reuse, ~154 net new LOC
- **3-Year TCO:** ~$7,000-10,000

**Proof Matrix by Phase Transition:**

| Phase Transition | Document | Checklist | Approval | Automated |
|------------------|----------|-----------|----------|-----------|
| Analysis → Planning | product-brief.md | - | - | L1 |
| Planning → Solutioning | PRD.md | prd/checklist.md | - | L1+L2 |
| Solutioning → Implementation | architecture.md | architecture/checklist.md | CRITICAL only | L1+L2+L3 |
| Implementation → Complete | tech-spec.md | code-review/checklist.md | CRITICAL only | L1+L2+L3+L4 |

**Key Insight:**
- CRITICAL workflows: Full multi-method (Documents + Checklists + Approval + Automated)
- EXPLORATORY workflows: Automated validation primarily (lighter touch)
- Aligns with D9-Q17's Hybrid decision and D9-Q18's Progressive L1→L4 mapping

**Analogy (Commercial Flight Clearance):** Phase transitions are like aircraft clearance - routine flights (exploratory) have fewer manual checks, international flights (critical) require more human verification. Automated systems (radar, transponder) run at ALL levels.

**Decided:** 2025-12-12, Session 82

---

## Resume Instructions

**Status:** ✅ D9 COMPLETE - All 19 questions decided.
**Methodology:** BMad Master facilitated, President decided each question.
**Next:** Update ARCHITECTURAL-DECISIONS.md with D9 decision.

**Session 82 (2025-12-12) Summary:**
- D9-Q19: Option E (Multi-Method Proof) - 3/3 UNANIMOUS
- D9 100% COMPLETE - Final question of Claude-Hybrid architectural decisions

**Session 81 (2025-12-12) Summary:**
- D9-Q17: Option E (Hybrid) - 3/3 UNANIMOUS
- D9-Q18: Option B (Extended Mapping) - 3/3 UNANIMOUS
