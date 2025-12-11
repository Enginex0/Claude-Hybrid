# D5: Context Management - Question Set

**Decision:** How does Claude-Hybrid manage context through 3-level progressive disclosure?
**Status:** ✅ COMPLETE (20/20 DECIDED)
**Generated:** 2025-12-10
**Sources:** claude-mpm skills/registry.py, InstructionCacheService, GitSourceSyncService, BMAD workflows (58+), Anthropic MCP progressive disclosure patterns

---

## Checkpoint Status

| Question | Status | Answer |
|----------|--------|--------|
| Q1 | **DECIDED** | Option A: Strict Sequential Loading - Only current step in memory |
| Q2 | **DECIDED** | Option A: Fine Granularity (CORRECTED: 1,000-2,500 tokens per step) |
| Q3 | **DECIDED** | Option A: Frontmatter State in Output File (PRE-SELECTED by D4) |
| Q4 | **DECIDED** | Option A: Dual Format Support - Markdown + YAML |
| Q5 | **DECIDED** | Option E (Synthesized): Track as Workflow Selection (C) + Loading Strategies (D) |
| Q6 | **DECIDED** | Option A: Project > User > Bundled priority (PRE-SELECTED by D3-Q9) |
| Q7 | **DECIDED** | Option A: Full 3-Level Progressive Disclosure (L1/L2/L3) |
| Q8 | **DECIDED** | Option A: Require Explicit Restart (PRE-SELECTED by D3-Q20) |
| Q9 | **DECIDED** | Option C: Manifest-Based Selective Loading |
| Q10 | **DECIDED** | Option A: Registry-Based Linking Only (PRE-SELECTED by D3-Q16) |
| Q11 | **DECIDED** | Option C: Hybrid Inline/External - Critical-path inline, supplementary external |
| Q12 | **DECIDED** | Option C: Hash-Based Primary - SHA-256 hash-based caching |
| Q13 | **DECIDED** | Option A: Hash-Based Invalidation - SHA-256 content hashing |
| Q14 | **DECIDED** | Option A: Full ETag Implementation - HTTP conditional requests + SHA-256 |
| Q15 | **DECIDED** | Option A: Categorical Templates - Flat directory with semantic naming |
| Q16 | **DECIDED** | Option A: Three-tier Structure (L1/L2/L3) (PRE-SELECTED by D5-Q7) |
| Q17 | **DECIDED** | Option D: Progressive Loading (L1 always, L2 on activation, L3 on-demand) |
| Q18 | **DECIDED** | Option B: Shorthand when unambiguous - 'skill-name' or 'plugin:skill' |
| Q19 | **DECIDED** | Option C: Reference files never auto-loaded - explicit Read tool required |
| Q20 | **DECIDED** | Option B: Single response model (PRE-SELECTED by D3-Q8) |

---

## Questions: Workflow Step Loading Strategy & State Tracking (Q1-Q4)

### Q1: How should workflow step files be loaded during execution?
**Context:** BMAD mandates "NEVER load multiple step files simultaneously". Workflow execution must progress through steps in order.

Options:
- A: Strict Sequential Loading - Only current step in memory, must complete in order, no skipping. Enforces linear progression.
- B: Lookahead Loading - Load current step + peek at next step for context. Allows better planning but violates BMAD mandate.
- C: Parallel Loading with Gating - Load all steps upfront but gate execution to sequential. Faster initial load but higher memory.
- D: Dynamic Load-Unload - Load current step, unload previous step, preload next step in background for smooth transitions.

### Q2: What is the appropriate granularity for step-level instructions?
**Context:** BMAD evidence shows 677-2,469 tokens per step. Each step must be self-contained enough to follow without additional context.

Options:
- A: Fine Granularity - 1,000-2,500 tokens per step (matches BMAD actual data). Each step is complete instruction unit.
- B: Medium Granularity - 2,500-5,000 tokens per step. Fewer transitions, more context per step.
- C: Coarse Granularity - 5,000-10,000 tokens per step. Minimal transitions, risk of overwhelming context.
- D: Variable Granularity - Adaptive sizing based on complexity. Simple steps get 1K tokens, complex steps get 5K+.

### Q3: Where should workflow progression tracking state be persisted?
**Context:** D4-Q8 establishes frontmatter as SSOT. D4 binding constraints (Q1, Q2, Q6, Q8, Q12) pre-selected Option A.

Options:
- A: Frontmatter State in Output File - stepsCompleted array, current_step in YAML frontmatter of generated document.
- B: Separate State File - .claude/workflow-state.json tracks progression independently from output document.
- C: In-Memory Only - State lives in Python runtime, lost on restart. Fastest but non-persistent.
- D: Database Persistence - SQLite database tracks all workflow state with full history and rollback capability.

### Q4: What file formats should workflows support?
**Context:** Both Markdown and YAML support frontmatter. BMAD has 58+ production workflows in various formats.

Options:
- A: Dual Format Support - Markdown for complex multi-step workflows (step-file architecture), YAML for simple declarative workflows.
- B: Markdown Only - Single format for consistency. YAML workflows convert to Markdown internally.
- C: YAML Only - Pure declarative approach. All workflows are YAML with embedded instructions.
- D: Plugin-Based Formats - Core supports Markdown+YAML, allow plugins to register additional formats (JSON, TOML).

---

## Questions: Multi-Track Context Budget Management (Q5)

### Q5: How should different workflow tracks manage their context budgets?
**Context:** Workflows may have different context requirements. Some are documentation-heavy, others are code-heavy.

Options:
- A: Uniform Budget - All tracks use same context management. Simple but inflexible.
- B: Track-Specific Budgets - Each track (Quick, Standard, Comprehensive) has predefined budget limits.
- C: Track as Workflow Selection - Tracks select workflows, context management is uniform via progressive disclosure.
- D: Track-Specific Loading Strategies - Base context management is uniform, but tracks optimize loading patterns.
- E: Synthesized (C+D) - Tracks select workflows, uniform context management via L1/L2/L3, with track-optimized loading.

---

## Questions: Skill Loading Priority & Progressive Disclosure Architecture (Q6-Q8)

### Q6: How should skill loading priority be resolved across installation tiers?
**Context:** D3-Q9 establishes hybrid installation with priority resolution. D3-Q17 establishes project highest priority.

Options:
- A: Project > User > Bundled priority - Project skills override user override bundled. Already implemented in claude-mpm.
- B: User > Project > Bundled priority - User preferences take precedence over project-specific configurations.
- C: Explicit priority declarations - Skills declare their priority level in frontmatter, system resolves conflicts.
- D: Last-installed wins - Most recently installed skill takes priority regardless of tier.

### Q7: Should Claude-Hybrid implement multi-level progressive disclosure for context management?
**Context:** claude-mpm implements 3-level progressive disclosure: L1 metadata always loaded, L2 entry point on activation, L3 references on demand. 50-80% token savings validated.

Options:
- A: Full 3-Level Progressive Disclosure - L1 metadata always loaded, L2 entry point on activation, L3 references on demand.
- B: Two-Level Loading - L1 metadata always loaded, L2 full content on activation only.
- C: Eager Loading - Load all skill content upfront for maximum context availability.
- D: Pure On-Demand - Load nothing until explicitly requested via Read tool.

### Q8: Should skill definitions support hot-reload during active sessions?
**Context:** D3-Q20 establishes session boundary loading for agents. Skills use identical filesystem scan mechanism.

Options:
- A: Require Explicit Restart (Session Boundary Only) - Native Claude Code behavior, matches agent loading pattern.
- B: File Watcher with Auto-Reload - Monitor filesystem for changes, reload modified skills automatically.
- C: Manual Reload Command - Provide /reload-skills command for mid-session refresh without full restart.
- D: Hybrid Approach - Session boundary default, optional file watcher mode for development environments.

---

## Questions: Skill Activation Triggers & Agent-to-Skill Linking (Q9-Q10)

### Q9: What mechanism should trigger skill activation and loading?
**Context:** D3-Q9, D3-Q15, D3-Q17, D3-Q19 establish registry-based patterns. Anthropic MCP achieves 98.7% token reduction, CMU reports 70% agent failures from context overflow.

Options:
- A: Auto-load all skills - Every skill loaded into context on session start. Simple but token-expensive.
- B: Keyword-Based Activation - Skills define trigger keywords, auto-load when keywords detected in conversation.
- C: Manifest-Based Selective Loading - Agent frontmatter declares required skills, load only declared dependencies.
- D: Pure On-Demand - Skills never auto-load, Claude must explicitly invoke via Skill tool based on descriptions.

### Q10: How should agents link to their required skills?
**Context:** D3-Q16 mandates O(1) deterministic lookup via filename stem matching. Berkeley BFCL shows 27.3% accuracy loss with keyword inference.

Options:
- A: Registry-Based Linking Only - Agents declare skill dependencies by exact skill name. O(1) deterministic lookup.
- B: Keyword Inference - System infers skill requirements from agent description text. Flexible but error-prone.
- C: Hybrid Linking - Registry-based as primary, keyword inference as fallback for discovery.
- D: Capability-Based Linking - Agents declare required capabilities, system matches to skills providing those capabilities.

---

## Questions: Instruction Template Management & Caching (Q11-Q15)

### Q11: Should instruction templates be externalized or embedded inline?
**Context:** D5-Q7 establishes 3-level progressive disclosure. Externalization enables progressive loading; inline keeps critical path fast.

Options:
- A: Full Externalization - All instruction content in separate files, loaded via progressive disclosure.
- B: Full Inline Embedding - All instructions embedded in agent/skill files for immediate availability.
- C: Hybrid Inline/External - Critical-path instructions inline (L1), supplementary material external (L2/L3).
- D: Dynamic Selection - System decides inline vs external based on content size and usage frequency.

### Q12: What should be the primary mechanism for template caching?
**Context:** D4-Q13 establishes hash-based validation. D4-Q19 establishes SHA-256 as PRIMARY mechanism.

Options:
- A: TTL-Based Primary - Time-to-live expiration as primary mechanism, hash validation as secondary check.
- B: Hybrid TTL+Hash - Equal weight to both mechanisms, use whichever triggers first.
- C: Hash-Based Primary - SHA-256 hash-based caching as PRIMARY mechanism, TTL as secondary cleanup.
- D: No Caching - Always regenerate templates on demand for guaranteed freshness.

### Q13: What should trigger template cache invalidation?
**Context:** D4-Q13/Q19/D5-Q12 establish hash-based PRIMARY caching. Git, Docker, npm, Kubernetes, Terraform all use content-hash invalidation.

Options:
- A: Hash-Based Invalidation - SHA-256 content hashing detects template changes, invalidate only when content differs.
- B: TTL Expiration - Invalidate after fixed time period regardless of content changes.
- C: Manual Invalidation - Provide /clear-cache command, no automatic invalidation.
- D: Dependency-Tracked Invalidation - Invalidate when any dependency (included file, variable source) changes.

### Q14: How should remote template sync be validated?
**Context:** GitSourceSyncService implements three-layer pattern: ETag + SHA-256 + SQLite. HTTP 304 Not Modified provides 95%+ bandwidth savings.

Options:
- A: Full ETag Implementation - HTTP conditional requests with ETag + mandatory SHA-256 content validation + SQLite state persistence.
- B: Content-Hash Only - Skip ETags, always fetch and validate via SHA-256. Simpler but higher bandwidth.
- C: Timestamp-Based - Use Last-Modified headers for sync decisions. Faster but less reliable.
- D: Full Download Always - No optimization, always fetch complete content. Maximum reliability, maximum bandwidth.

### Q15: How should instruction template files be organized?
**Context:** D5-Q11/Q12/Q13 establish hash-based caching. Django, Jinja2, Handlebars, BMAD, claude-mpm use flat categorical organization.

Options:
- A: Categorical Templates - Flat directory with semantic naming (circuit-breakers.md, research-gate-examples.md).
- B: Flat Directory with Semantic Naming - Single templates/ directory, descriptive filenames indicate purpose.
- C: Hierarchical by Skill - templates/skill-name/template-name.md for clear ownership.
- D: Registry-Based Organization - Template manifest maps logical names to file paths, allows flexible organization.

---

## Questions: Skill Definition File Structure & Loading Timing (Q16-Q17)

### Q16: What structure should skill definition files follow?
**Context:** D5-Q7 establishes 3-level progressive disclosure. Anthropic MCP achieves 98.7% token reduction. 74% of bundled skills already implement L1/L2/L3.

Options:
- A: Three-tier Structure - L1: SKILL.md core always loaded, L2: references/ deep-dive docs, L3: examples/ concrete usage.
- B: Single-File Everything - All content in one SKILL.md file. Simple but large context footprint.
- C: Frontmatter + Sections - Single file with YAML frontmatter, markdown sections for different detail levels.
- D: Modular Components - Separate files for metadata, instructions, examples, references. Compose on load.

### Q17: When should skill content be loaded into context?
**Context:** D5-Q7 establishes 3-level progressive disclosure. D5-Q9 establishes manifest-based selection. D5-Q10 establishes registry-based linking.

Options:
- A: Session Start - Load all skills at session initialization for immediate availability.
- B: First Mention - Load skill when first referenced in conversation. Balance availability and efficiency.
- C: Explicit Invocation - Load only when explicitly invoked via Skill tool.
- D: Progressive Loading - L1 metadata always loaded, L2 on activation, L3 on-demand via Read tool.

---

## Questions: Skill Invocation Syntax & Context Management (Q18-Q20)

### Q18: Should skill invocation syntax require full qualification?
**Context:** D3-Q9/Q17 establish tier-based priority. D5-Q6 establishes Project > User > Bundled. npm, PyPI, cargo, gradle use shorthand patterns.

Options:
- A: Always Fully Qualified - Require 'plugin-name:skill-name' syntax every time. Verbose but unambiguous.
- B: Shorthand when unambiguous - Use simple 'skill-name' when unique; require 'plugin:skill' on conflicts.
- C: Namespace Prefixes - Use short prefixes like '@p/skill' (project), '@u/skill' (user), '@s/skill' (system).
- D: Priority-Based Resolution - Allow shorthand, resolve conflicts via tier priority (Project > User > Bundled).

### Q19: Should reference files be automatically loaded when skills activate?
**Context:** D5-Q7/Q17 establish progressive disclosure with on-demand L3 loading. Anthropic MCP achieves 98.7% token reduction. claude-mpm registry.py explicitly states 'Reference files NOT loaded as skills'.

Options:
- A: Inline Hints Only - SKILL.md contains inline hints about reference files, but never auto-loads them.
- B: Auto-load All References - When skill activates, automatically load all files from references/ directory.
- C: Explicit Read Tool Required - Reference files never auto-loaded; Claude must explicitly use Read tool based on hints.
- D: Smart Preloading - Load reference files that match current task context, skip unrelated references.

### Q20: How should sub-agent skill invocations handle context accumulation?
**Context:** D3-Q8 establishes complete message primary (90-95%). D4-Q14 establishes delegation chain state. D6-Q18 establishes Slash=EMBODIES, Task=DELEGATES.

Options:
- A: Full Context Accumulation - Sub-agent skill invocations accumulate in parent agent's context for full history.
- B: Single Response Model - Agents return one final message; internal skill invocations don't accumulate in parent context.
- C: Summary Accumulation - Sub-agent returns summary of skill invocations, not full transcripts.
- D: Configurable Accumulation - Agent frontmatter specifies whether to accumulate sub-agent context.

---

## Resume Instructions

**Next session:** Read this file, continue from first PENDING question.
**Methodology:** BMad Master facilitates, President decides each question.
**After completion:** Update ARCHITECTURAL-DECISIONS.md with D5 decision.
