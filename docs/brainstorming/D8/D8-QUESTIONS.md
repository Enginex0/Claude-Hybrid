# D8: Plugin & Agent Format - Question Set

**Decision:** How does Claude-Hybrid structure plugins and agents?
**Status:** ✅ COMPLETE (15/15 DECIDED)
**Generated:** 2025-12-10 (Session X)
**Updated:** 2025-12-12 - ALL 15 QUESTIONS DECIDED (Q15 gap resolved)
**Sources:** Claude Code architecture (03-EXTENSION-SYSTEM.md, 05-CONFIGURATION.md), Personal BMAD architecture

---

## Redundancy Audit Notes

The following 8 questions were removed as they overlap with decisions made in D2-D5:

| Removed | Original Topic | Overlap Reason |
|---------|---------------|----------------|
| Q5 | Agent frontmatter required fields | Constrained by D3 decisions |
| Q6 | Description for Task matching | D3-Q16 filename stem makes this moot |
| Q7 | Skills auto-loading format | D5-Q17 progressive loading decided |
| Q12 | Subagent permission inheritance | D2+D3 enforcement covers this |
| Q13 | Plugin discovery paths | D5-Q6 Project>User>Bundled priority |
| Q14 | Plugin enablement control | D3-Q15 + D5-Q9 patterns cover this |
| Q16 | Plugin internal discovery | D5-Q16 3-tier structure applies |
| Q19 | Agent file naming for Task | DUPLICATE of D3-Q16 |

---

## Checkpoint Status

| Question | Status | Answer |
|----------|--------|--------|
| Q1 | **DECIDED** | Option B: Standard (name + version + description) |
| Q2 | **DECIDED** | Option B: Semantic Versioning (X.Y.Z) |
| Q3 | **DECIDED** | Option A: No dependencies (future path to C) |
| Q4 | **DECIDED** | Option A: Name-directory match (constraint-forced) |
| Q5 | **DECIDED** | Option B: Fixed set (inherit/sonnet/opus/haiku) |
| Q6 | **DECIDED** | Option B: Tiered (default/elevated/bypass) |
| Q7 | **DECIDED** | Option C: Least-privilege wins |
| Q8 | **DECIDED** | Hybrid B+C: Session warning + Per-op audit |
| Q9 | **DECIDED** | Option B: Marketplace-qualified (plugin@marketplace) |
| Q10 | **DECIDED** | Option D: Hybrid (YAML frontmatter + XML sections) |
| Q11 | **DECIDED** | Option D: Configurable gates (template + opt-in/out) |
| Q12 | **DECIDED** | Option B: Optional namespacing (plugin:agent when ambiguous) |
| Q13 | **DECIDED** | Option B: Optional sidecar (static only, D5-Q20 compliant) |
| Q14 | **DECIDED** | Option D: Hybrid backward-compatible (ALREADY IMPLEMENTED) |
| Q15 | **DECIDED** | Option C+E: Multi-Point Programmable Gates |

---

## Questions: Plugin Manifest Format (Q1-Q4)

### Q1: What should be the required fields in plugin.json manifest?
Options:
- A: Minimal (name only) - Claude Code pattern allows single `{"name": "plugin-name"}` manifest, lowest barrier to entry
- B: Standard (name + version + description) - Adds versioning and discoverability without complexity
- C: Extended (name + version + description + author + keywords) - Full metadata for marketplace/discovery scenarios
- D: Comprehensive (all above + dependencies + compatibility + permissions) - Enterprise-grade manifest with full metadata

### Q2: How should plugin manifest versioning be structured?
Options:
- A: No versioning requirement - Plugins operate independently without version tracking
- B: Semantic versioning (semver) - Standard `major.minor.patch` format enabling dependency management
- C: Date-based versioning - Use `YYYY.MM.DD` format tied to modification date
- D: Hybrid versioning - Optional semver in manifest with auto-generated date fallback

### Q3: Should plugin.json support dependency declarations?
Options:
- A: No dependencies - Plugins are fully self-contained units with no inter-plugin dependencies
- B: Plugin dependencies - Allow declaring required plugins (`{"dependencies": {"other-plugin": ">=1.0.0"}}`)
- C: System dependencies - Declare required MCP servers, tools, or Claude Code version
- D: Full dependency graph - Both plugin and system dependencies with conflict resolution

### Q4: How should plugin naming and directory structure be enforced?
Options:
- A: Name-directory match (Claude Code pattern) - `plugin.json.name` must match containing directory name
- B: Flexible naming - Directory and manifest name can differ, use manifest name as identifier
- C: Namespace prefixes - Require `{org}:{plugin-name}` format to prevent collisions
- D: UUID-based identification - Use UUIDs internally with human-readable display names

---

## Questions: Agent Model Selection (Q5)

### Q5: Should agents support model selection and what options should be available?
*Note: Focus on model options only; frontmatter schema constrained by D3 decisions.*

Options:
- A: Inherit only - All agents use parent session model (simplest, no resource optimization)
- B: Fixed set (inherit/sonnet/opus/haiku) - Claude Code's current model options
- C: Extended set - Add future models (claude-4, etc.) with validation against available models
- D: Dynamic discovery - Query available models at runtime, validate against Claude API

---

## Questions: Permission Modes (Q6-Q8)

### Q6: What permission modes should Claude-Hybrid support?
Options:
- A: Binary (default/bypassPermissions) - Claude Code's current two-mode system
- B: Tiered (default/elevated/bypass) - Add intermediate level for semi-trusted operations
- C: Granular (per-tool permissions) - Define permissions per tool type (Read/Write/Bash/etc.)
- D: Role-based - Permission profiles tied to agent roles (analyst=read-only, dev=full-access)

### Q7: How should agent permissionMode interact with global settings?
*Note: Scope limited to global vs agent precedence; subagent inheritance covered by D2+D3.*

Options:
- A: Agent overrides global - Agent frontmatter `permissionMode` supersedes `settings.json` setting
- B: Global overrides agent - `settings.json` always takes precedence for security
- C: Least-privilege wins - Use more restrictive of global vs agent setting
- D: Most-permissive wins - Use less restrictive setting (for trusted environments)

### Q8: Should permission bypass require explicit user acknowledgment?
Options:
- A: Silent bypass - `bypassPermissions` operates without any user notification
- B: Session-start warning - Notify user once at session start when bypass mode is active
- C: Per-operation audit - Log all bypassed operations for later review
- D: Confirmation prompt - Require one-time user confirmation when bypass mode first activates

---

## Questions: Plugin Identification (Q9)

### Q9: What plugin identifier format should be used in enabledPlugins?
Options:
- A: Simple name - `"plugin-name": true`
- B: Marketplace-qualified (Claude Code pattern) - `"plugin-name@marketplace": true`
- C: Path-based - `"~/.claude/plugins/marketplaces/local/plugins/plugin-name": true`
- D: Content-addressed - Use hash of plugin contents for verification

---

## Questions: Agent Format Specification (Q10-Q12)

### Q10: Should agents support embedded configuration beyond YAML frontmatter?
Options:
- A: Frontmatter only - All config in YAML frontmatter, body is pure persona content
- B: XML sections (BMAD pattern) - Support `<session_config>`, `<response_gate>` sections in body
- C: Markdown sections - Use special markdown headers (## CONFIG:, ## GATE:) for structured data
- D: Hybrid format - YAML frontmatter for standard fields, XML sections for extended config

### Q11: Should agent format include response gate enforcement?
Options:
- A: No gates - Agent personas are purely instructional, no embedded verification
- B: Optional gates - Allow but don't require `<response_gate>` sections
- C: Mandatory gates (BMAD pattern) - All agents must include 5-step response gate protocol
- D: Configurable gates - Gate template defined globally, agents opt-in/out per agent

### Q12: Should agents support plugin namespacing in subagent_type?
Options:
- A: No namespacing - Agent names are globally unique across all plugins
- B: Optional namespacing (Claude Code pattern) - Support `plugin:agent` format when ambiguous
- C: Required namespacing - Always use `plugin:agent` format for clarity
- D: Hierarchical namespacing - Support `marketplace:plugin:agent` for full qualification

---

## Questions: Gap Analysis Additions (Q13)

### Q13: Should agents support sidecar knowledge directories?
**Context:** BMAD supports expert agents having a `{agent}-sidecar/` directory containing `instructions.md`, `memories.md`, and `knowledge/` subdirectories with domain-specific files. Critical actions can load these via `Load COMPLETE file {agent-folder}/toolsmith-sidecar/knowledge/deploy.md`.

Options:
- A: No sidecar support - All agent knowledge must be in the main agent file or referenced via skills.
- B: Optional sidecar directories - Agents MAY have `{agent}-sidecar/` with predefined structure; loaded on-demand.
- C: Mandatory sidecar for experts - Expert/specialist agents MUST have sidecar directories; orchestrators do not.
- D: Flexible knowledge references - Agent frontmatter specifies arbitrary knowledge file paths; no fixed sidecar structure.

### Q14: Should agents support multiple trigger patterns via triggers array?
**Context:** Recent BMAD Method changes updated the agent schema from single `trigger` field to `triggers` array, allowing agents to activate on multiple patterns. This affects backward compatibility and matching logic.

Options:
- A: Single trigger only - Maintain current schema with one trigger string per agent for simplicity.
- B: Triggers array (BMAD pattern) - Support array of trigger patterns; agent activates on any match.
- C: Trigger object - Support `{patterns: [], priority: number, context: string}` for rich triggering rules.
- D: Hybrid backward-compatible - Single `trigger` for simple agents, `triggers` array for complex activation; both supported.

---

## Questions: Gap Resolution - Gate Mechanism (Q15)

### Q15: How should hook-based validation gates operate?
**Context:** D8-Q11 decided gates are "configurable (template + opt-in/out)" but not HOW gates work.

Options:
- A: Pre-Response Gate - Validate response before sending to user
- B: Pre-Tool Gate - Validate tool parameters before execution (extends PreToolUse)
- C: Multi-Point Gates - Gates at multiple points (pre-tool, post-tool, pre-response)
- D: Schema Gate - Gates validate against predefined schemas only
- E: Programmable Gates - Gates execute custom validation logic

**Related Decision:** D8-Q11

---

#### **DECIDED: Option C+E - Multi-Point Programmable Gates**

**Specialist Consensus:** 3/3 unanimous on E (Programmable), 2/3 favor C+E hybrid (9/10 avg confidence)

**Binding Constraints Satisfied:**
- D2-Q15: PreToolUse phase for hard enforcement ✅
- D2-Q16: Hybrid structural+runtime ✅
- D2-Q8: Two-tier hard/soft enforcement ✅
- D2-Q12: permissionDecisionReason schema ✅

**Evidence:**
- Claude Code: Only PreToolUse and UserPromptSubmit can BLOCK (PostToolUse cannot)
- BMAD: 5-step programmable gate protocol (IDENTIFY→RUN→READ→VERIFY→CLAIM)
- Industry: 7/7 frameworks use multi-point + programmable (LangGraph, CrewAI, AutoGen, OpenAI, Semantic Kernel, NeMo, Guardrails AI)

**Eliminated Options:**
- ❌ A: No PreResponse hook exists in Claude Code
- ❌ B standalone: Ignores D2-Q8's soft tier requirement
- ❌ D standalone: Cannot implement BMAD's 5-step decision protocol

**Architecture:**
- C (Multi-Point) = WHERE: PreToolUse (hard/blocking), PostToolUse (soft/audit), Instructional (soft/template)
- E (Programmable) = HOW: BMAD 5-step protocol with decision trees and conditional logic

**Implementation:** ~150-200 LOC net new, 90% reuse of gate-function.md (326 LOC), ~$4,500 3-year TCO

**Analogy:** Airport security with multiple checkpoints - TSA (PreToolUse) can DENY boarding, Gate Agent (PostToolUse) can FLAG but not deny, Flight Attendant (Instructional) provides guidance. Each uses programmable screening logic.

**Decided:** 2025-12-12

---

## Resume Instructions

**Status:** ✅ D8 COMPLETE! All 15/15 questions DECIDED.
**Next:** Update ARCHITECTURAL-DECISIONS.md with D8 summary.
**Methodology:** BMad Master facilitated, President decided each question.
