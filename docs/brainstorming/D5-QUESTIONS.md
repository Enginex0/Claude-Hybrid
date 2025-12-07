# D5: Context Management - Question Set

**Decision:** How does Claude-Hybrid manage the 200k context limit?
**Status:** PENDING
**Generated:** 2025-12-07 (Session 5)
**Sources:** 4 documents analyzed by subagents

---

## Checkpoint Status

| Question | Status | Answer |
|----------|--------|--------|
| Q1-Q20 | PENDING | - |

---

## Questions from BMAD 05-WORKFLOWS-SYSTEM.md

### Q1: Should Claude-Hybrid use step-file architecture with sequential loading or allow parallel step loading?
Options:
- A: Strict Sequential Loading - Only current step in memory, must complete in order, no skipping (BMAD: "NEVER load multiple step files simultaneously")
- B: Selective Parallel Loading - Allow loading related steps together when they share context
- C: Hybrid Approach - Sequential by default, but allow explicit "batch load" directive for known-safe step combinations
- D: Pre-fetch with Discard - Load next step speculatively but discard from context if current step branches differently

### Q2: What granularity should micro-files have in Claude-Hybrid's context management?
Options:
- A: BMAD-style Fine Granularity - Each step is self-contained instruction file (~100-500 tokens per step file)
- B: Medium Granularity - Combine 2-3 related steps into single files to reduce loading overhead
- C: Adaptive Granularity - Small files for complex workflows, larger combined files for simple workflows
- D: Token-Budget Granularity - Split files based on target token count regardless of logical step boundaries

### Q3: How should Claude-Hybrid track workflow state to enable just-in-time loading?
Options:
- A: Frontmatter State in Output File - Track stepsCompleted array and current_step in YAML frontmatter of generated document
- B: Separate State File - Maintain lightweight JSON state file separate from output documents
- C: In-Memory State with Checkpoint - Track state in context, checkpoint to file only at step transitions
- D: Orchestrator-Managed State - Let runtime orchestrator agent maintain state externally, workflows are stateless

### Q4: Should Claude-Hybrid support multiple workflow formats (Markdown vs YAML) or standardize on one?
Options:
- A: Dual Format Support - Markdown for complex multi-step workflows, YAML for simpler declarative workflows
- B: Markdown Only - Standardize on markdown for consistency, use frontmatter for configuration
- C: YAML Only - Standardize on YAML for machine-readability and easier parsing by orchestrator
- D: Format Auto-Detection - Support both but auto-convert to internal canonical representation at load time

### Q5: How should Claude-Hybrid handle the "3 Tracks" architecture for context budget allocation?
Options:
- A: Track-Based Token Budgets - Quick Flow gets minimal context (~10K), BMAD Method gets standard (~50K), Enterprise gets full budget (~150K)
- B: Dynamic Track Scaling - All tracks start small, scale up context budget as complexity is detected during execution
- C: Track as Workflow Selection Only - Tracks determine which workflows to run, but context management is uniform across tracks
- D: Track-Specific Loading Strategies - Quick Flow uses eager loading (small total), BMAD uses just-in-time, Enterprise uses aggressive eviction

---

## Questions from Claude-MPM 05-AGENTS-SKILLS.md

### Q6: How should the skill loading tier priority be configured for context management?
Options:
- A: Project > User > Bundled priority - project-level skills override user and bundled, ensuring minimal context pollution
- B: Dynamic priority based on current task - adjust which tier takes precedence based on agent type or task context
- C: Flat loading with explicit include/exclude lists - ignore tier hierarchy and use explicit configuration to control what loads

### Q7: Should 3-Level Progressive Disclosure (L1 metadata, L2 entry point, L3 references) be the primary context management strategy?
Options:
- A: Full 3-level progressive disclosure - L1 metadata always loaded (minimal), L2 entry point on activation, L3 references on demand (50-80% token savings)
- B: 2-level simplified approach - Merge L1/L2 into single lightweight index, load L3 references on demand
- C: Flat loading with size limits - Skip progressive disclosure entirely but cap skill file sizes to manage context
- D: Hybrid approach - Use 3-level for large skills (329 skills), flat loading for small/critical skills

### Q8: What restart semantics should apply when skills are deployed mid-session?
Options:
- A: Require explicit restart - Skills discovered at startup only ("Claude Code RESTART REQUIRED after skill deployment")
- B: Hot-reload mechanism - Implement runtime skill discovery without restart
- C: Session-scoped caching - Cache skill state at session start, allow refresh command

### Q9: How should multi-source agent discovery (4-tier) interact with context limits?
Options:
- A: Lazy loading with Remote priority - Only load agent templates when invoked, Remote tier takes precedence
- B: Eager loading with deduplication - Load all tiers at startup but deduplicate by name (higher priority wins)
- C: Manifest-based selective loading - Use lightweight manifest to decide which agents to load based on project needs
- D: On-demand remote fetch - Keep only local agents in context, fetch remote agents only when explicitly needed

### Q10: Should skill invocation use registry-based linking or keyword inference for context efficiency?
Options:
- A: Registry-based linking only - Use skills_registry.yaml mappings for predictable, minimal context loading
- B: Keyword inference only - Use skill_manager.py keyword matching for flexibility
- C: Hybrid registry + keyword - Registry for core mappings, keyword inference as fallback for dynamic skill discovery
- D: User-declared skill activation - Require explicit skill invocation via Skill tool, no automatic loading

---

## Questions from Claude-MPM 08-CACHE-CLI.md

### Q11: Should Claude-Hybrid adopt the 54-template externalization pattern that achieved 48.1% token reduction?
Options:
- A: Full Adoption - Externalize all extensive examples, workflows, and reference material into separate markdown files
- B: Selective Adoption - Externalize only the largest context consumers while keeping core instructions inline
- C: Hybrid Inline/External - Keep critical-path instructions inline for immediate availability, externalize supplementary material only
- D: Alternative Token Reduction - Explore other compression techniques rather than template externalization

### Q12: How should Claude-Hybrid implement cache layering for context management?
Options:
- A: Four-Layer Architecture - Foundation (LRU + TTL) -> Framework (specialized) -> Subprocess (singleton) -> Specialized (hash-based)
- B: Simplified Two-Layer - Use only Foundation (file-based LRU with TTL) and Specialized (hash-based for instructions)
- C: Hash-Based Primary - Use SHA-256 hash-based caching as the primary mechanism to detect content changes without TTL
- D: Memory-Pressure Aware - Implement 80% memory threshold with background cleanup as primary context management strategy

### Q13: What invalidation strategy should Claude-Hybrid use for externalized templates?
Options:
- A: Hash-Based Invalidation - Use SHA-256 content hashing to detect template changes and invalidate only when content differs
- B: TTL-Based with Pattern Matching - Use TTL expiration combined with pattern-based invalidation for template categories
- C: Manual Invalidation - Require explicit cache clearing via CLI commands
- D: Hybrid Hash + Memory-Pressure - Combine hash-based detection with 80% memory threshold triggers

### Q14: Should Claude-Hybrid use the Git-Sync ETag mechanism for template versioning?
Options:
- A: Full ETag Implementation - Adopt HTTP conditional requests with ETag caching for 95%+ bandwidth reduction
- B: Local SHA-256 Only - Skip remote sync complexity, use local file system hash tracking
- C: Database-Tracked State - Use SQLite tracking with sources, file hashes, and sync history tables
- D: Modification Time Based - Use simple file modification time tracking without hash complexity

### Q15: How should Claude-Hybrid organize its template reference patterns?
Options:
- A: Categorical Templates - Organize into functional categories (circuit-breakers.md, research-gate-examples.md, etc.)
- B: Flat Template Directory - Single templates/ directory with all markdown files using simple references
- C: Hierarchical Namespacing - Organize templates by domain (templates/workflow/, templates/examples/, templates/gates/)
- D: Inline Template IDs - Use short template identifiers in main instructions with a template registry

---

## Questions from Claude Code 03-EXTENSION-SYSTEM.md

### Q16: How should skills implement progressive disclosure for context management?
Options:
- A: Three-tier structure (L1: SKILL.md core always loaded, L2: references/ deep-dive docs, L3: examples/ concrete usage)
- B: Flat structure with everything in SKILL.md and let Claude decide what to reference
- C: On-demand loading where SKILL.md contains only metadata and all content lives in subdirectories
- D: Size-based tiering where content below a threshold lives in SKILL.md and larger content is externalized

### Q17: When should Claude-Hybrid load skills - upfront via agent frontmatter or on-demand via Skill tool?
Options:
- A: Agent frontmatter auto-loading (skills listed in agent YAML are loaded when agent spawns)
- B: Explicit Skill tool invocation (Claude calls Skill tool just-in-time when domain knowledge is needed)
- C: Hybrid approach where critical skills auto-load via frontmatter, optional skills load on-demand
- D: Progressive loading where agent triggers skill discovery but content is fetched incrementally

### Q18: How should plugin/skill namespacing work to prevent context bloat from ambiguous resolution?
Options:
- A: Always require full namespacing ("plugin-name:skill-name") to prevent scanning multiple plugins
- B: Shorthand resolution when unambiguous (just "skill-name") with fallback to full prefix when conflicts exist
- C: Plugin manifest declares priority order for resolution, reducing search overhead
- D: Marketplace-level namespacing where local plugins take precedence over community plugins

### Q19: How should reference files be accessed to minimize context consumption?
Options:
- A: Inline file links in SKILL.md ("See references/api-guide.md for...") with Claude choosing when to load
- B: Skill tool automatically loads all files in skill directory into context
- C: Reference files are never auto-loaded; Claude must explicitly use Read tool based on SKILL.md hints
- D: Summary metadata in SKILL.md with file descriptions, enabling targeted loading based on task needs

### Q20: What agent restrictions reduce context accumulation across multi-step workflows?
Options:
- A: Stateless execution (agents cannot persist data between invocations, forcing fresh context each spawn)
- B: Single response model (agents return one final message rather than accumulating multi-turn context)
- C: No user interaction constraint (agents cannot use AskUserQuestion, preventing unbounded dialog)
- D: Tool access inheritance (agents share parent tools rather than loading separate tool definitions)

---

## Resume Instructions

**Next session:** Read this file, continue from first PENDING question.
**Methodology:** BMad Master facilitates, President decides each question.
**After completion:** Update ARCHITECTURAL-DECISIONS.md with D5 decision.
