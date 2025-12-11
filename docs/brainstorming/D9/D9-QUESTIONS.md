# D9: Path Variables & File Structure - Question Set

**Decision:** How does Claude-Hybrid manage path variables and file structure?
**Status:** COMPLETE (16/16 DECIDED - 100%) 🎉
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

## Resume Instructions

**Next session:** Read this file, continue from first PENDING question.
**Methodology:** BMad Master facilitates, President decides each question.
**After completion:** Update ARCHITECTURAL-DECISIONS.md with D9 decision.
