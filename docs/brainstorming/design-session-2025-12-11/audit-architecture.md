# Architecture Audit Report: claude-mpm

**Audit Date:** 2025-12-11
**Codebase:** claude-mpm (Enginex0 fork v5.1.2)
**Source:** `/home/president/bmad-systems/claude-mpm/src/claude_mpm/`
**Total Python Files:** 737
**Reference Document:** ARCHITECTURE-COMPLETE.md

---

## Executive Summary

The claude-mpm codebase exhibits **severe over-engineering** throughout, with multiple redundant systems, excessive abstraction layers, and premature generalization. The architecture document itself acknowledges "3 DI containers (isolated, NO CROSS-COMMUNICATION!)" and "4 config systems" as features rather than recognizing them as architectural debt. While the core concept (deploy config files, then exec to Claude Code) is sound, the implementation is 10-20x more complex than necessary. **Claude-Hybrid should carry over the essential patterns but reject 80% of the implementation complexity.**

---

## KEEP (Clean Architecture, Port Directly)

| Module/Pattern | What's Good | Why Keep |
|----------------|-------------|----------|
| **`os.execvpe()` handoff** (`interactive_session.py:571`) | Clean process replacement - MPM deploys files then replaces itself with Claude Code | This is the core value proposition. Simple, elegant, Unix-native |
| **Singleton Config pattern** (`core/config.py`) | Thread-safe singleton with proper double-check locking | Configuration should be loaded once and shared |
| **LRU FileSystemCache** (`core/cache.py`) | Well-implemented LRU cache with TTL, size limits, and stats | Single, clean cache implementation - use as template |
| **Agent template deployment** (concept) | Deploy markdown templates to `~/.claude/agents/` | Core functionality that Claude Code consumes |
| **Hook system concept** (7 events) | PreToolUse, PostToolUse, etc. | Event system for observability is valuable |
| **PM_INSTRUCTIONS assembly** | Concatenate sections into single system prompt | Simple text assembly is correct approach |

---

## REFACTOR (Over-Engineered, Simplify)

| Module/Pattern | Over-Engineering | Suggested Simplification |
|----------------|------------------|--------------------------|
| **3 DI Containers** (DIContainer, ServiceContainer, MCPServiceRegistry) | 3 separate containers with "NO CROSS-COMMUNICATION" - defeats purpose of DI | **Single container**. DI should unify dependencies, not fragment them |
| **4 Config Systems** (Legacy, UnifiedConfig, UnifiedConfigManager, UnifiedConfigService) | All 4 exist despite architecture doc claiming "unified now active" | **Single Config class**. Legacy Config (1012 LOC) works fine - delete the others |
| **72 deployment files** in `services/agents/deployment/` | Pipeline/Strategy/Facade/Builder/Processor patterns for copying files | **Single deployer class** with ~200 LOC. It's file copying, not enterprise Java |
| **11 cache implementations** (per architecture doc) | 4-layer cache architecture: Foundation, Framework, Subprocess, Specialized | **2 caches max**: Memory (LRU) and Disk (simple JSON). Delete the rest |
| **81+ exception classes** | Full hierarchy with context, error codes, factory functions | **5-10 exception classes max**. MPMError, ConfigError, DeployError, HookError |
| **agent_template_builder.py** (55KB, 1400+ LOC) | Massive template builder with processors, validators, generators | **~100 LOC function**. Templates are markdown files, not compiled artifacts |
| **Services abstraction layers** | services/core/, services/agents/, services/unified/, etc. with interfaces | **Flat service structure**. Most "services" are single-purpose utilities |
| **Validation subsystem** | validation/, validators/, multiple validation passes | **Single validation function** per domain. Don't enterprise-ify validation |

---

## REJECT (Broken Architecture, Don't Carry Over)

| Module/Pattern | Issue | Why Reject |
|----------------|-------|------------|
| **Multiple singleton containers** | DIContainer AND ServiceContainer AND MCPServiceRegistry all have global instances | Architectural contradiction - singletons + multiple containers = chaos |
| **unified_config.py** (UnifiedConfig via Pydantic) | 450+ LOC of Pydantic models for config that config.py already handles | Dead weight. Never properly integrated per architecture doc |
| **Pipeline pattern for deployment** (`pipeline/`, 6+ files) | PipelineBuilder, PipelineExecutor, 5 Step classes for file deployment | Complexity for complexity's sake. `shutil.copy` does the job |
| **Strategy pattern for deployment** (`strategies/`, 5+ files) | StrategySelector, BaseStrategy, SystemStrategy, UserStrategy, ProjectStrategy | Wrong pattern. Strategies should differ in algorithm, not just paths |
| **Facade pattern** (`facade/`, 4 files) | DeploymentFacade, DeploymentExecutor, Async/Sync variants | Unnecessary indirection. Direct calls are clearer |
| **Processors subdirectory** (`processors/`, 4 files) | AgentDeploymentContext, AgentDeploymentResult, AgentProcessor | Over-abstraction of simple operations |
| **services/exceptions.py** (758 LOC) | SocketIOServerError, DaemonConflictError, PortConflictError, etc. with resolution steps | Exceptions shouldn't contain troubleshooting guides. Use logging/docs |
| **Interface explosion** | IServiceContainer, ICacheManager, IPathResolver, etc. | Python uses duck typing. Interfaces add ceremony without value |
| **AgentSkillsInjector** | Removed as dead code (per architecture doc) | Confirmed dead code - good that it was removed |
| **Multi-layer validation** (`validation/` subdirs everywhere) | validation_step.py, agent_validator.py, deployment_validator.py, template_validator.py | Consolidated validation is simpler and more consistent |

---

## Dependency Graph Analysis

### Core Module Dependencies (Problematic)

```
core/container.py
    -> services/core/interfaces.py (IServiceContainer)
    -> core/logger.py

services/core/service_container.py
    -> core/logger.py
    (No shared interface with core/container.py!)

core/config.py
    -> utils/config_manager.py
    -> core/exceptions.py
    -> core/unified_paths.py
    -> core/logging_utils.py
    (1012 LOC for config!)

core/unified_config.py
    -> pydantic, pydantic_settings
    -> core/exceptions.py
    (DUPLICATE of config.py - never integrated)
```

### Deployment Service Dependencies (Over-Coupled)

```
services/agents/deployment/
    72 Python files
    ~15KB-55KB per major file
    Circular dependencies through shared models

    agent_deployment.py (42KB) depends on:
        -> agent_config_provider.py (15KB)
        -> agent_lifecycle_manager.py (38KB)
        -> agent_template_builder.py (55KB)
        -> agent_validator.py (13KB)
        -> multi_source_deployment_service.py (48KB)
        -> ...20+ more internal dependencies
```

---

## Coupling Metrics

| Module | Afferent (Ca) | Efferent (Ce) | Instability (I) | Assessment |
|--------|---------------|---------------|-----------------|------------|
| `core/config.py` | 50+ | 5 | 0.09 | Stable but BLOATED (1012 LOC) |
| `core/container.py` | 30+ | 3 | 0.09 | Stable but DUPLICATED |
| `services/core/service_container.py` | 10+ | 2 | 0.17 | Redundant with core/container |
| `services/agents/deployment/` (whole dir) | 20+ | 40+ | 0.67 | Highly unstable, over-coupled |
| `core/exceptions.py` | 80+ | 1 | 0.01 | Stable, but 537 LOC for exceptions |
| `services/exceptions.py` | 20+ | 5 | 0.20 | DUPLICATE exception hierarchy |

**Key Insight:** High coupling within deployment services creates a "dependency hairball" where changes cascade unpredictably.

---

## Layer Analysis

### Current Layers (Problematic)

```
Layer 1: CLI (cli/, 98 files)
    - Entry points, parsers, commands
    - VIOLATION: Some commands directly instantiate services

Layer 2: Core (core/, 100+ files)
    - Container, Config, Cache, Exceptions
    - VIOLATION: 2 config systems, 2 DI containers in "core"

Layer 3: Services (services/, 150+ files)
    - Another container, another config, business logic
    - VIOLATION: service_container duplicates core/container

Layer 4: Hooks (hooks/, 30+ files)
    - Event handling, memory integration
    - OK: Mostly isolated

Layer 5: Utils (utils/, 20+ files)
    - Utilities that should be in stdlib or core
    - VIOLATION: config_manager duplicates core/config functionality
```

### Layer Violations Found

1. **CLI -> Services (bypassing Core):** Several CLI commands instantiate services directly
2. **Core/config -> Utils/config_manager:** Core depends on utils (inverted)
3. **Services/core -> Core/logger:** Services "core" depends on core (naming confusion)
4. **Two DI containers:** core/container AND services/core/service_container (fragmented)
5. **Two exception hierarchies:** core/exceptions AND services/exceptions (duplicate)

---

## Cohesion Analysis

### Low Cohesion Modules (Doing Too Many Things)

| Module | Responsibilities | Cohesion Issue |
|--------|------------------|----------------|
| `core/config.py` (1012 LOC) | Load files, validate, merge, env vars, defaults, health config, recovery config, session config | Should be 3-4 separate modules |
| `agent_template_builder.py` (55KB) | Build, validate, format, version, convert, merge templates | Should be decomposed or simplified |
| `multi_source_deployment_service.py` (48KB) | Discovery, sync, deploy, validate from multiple sources | Too many responsibilities |
| `agent_lifecycle_manager.py` (38KB) | Lifecycle, health, metrics, recovery, state | God class |

### High Cohesion Modules (Good Examples)

| Module | Single Responsibility | Why Good |
|--------|----------------------|----------|
| `core/cache.py` (561 LOC) | LRU caching with TTL | Clear, focused, well-implemented |
| `core/logger.py` | Logging configuration | Simple, does one thing |
| `core/enums.py` | Enumeration definitions | Pure data definitions |

---

## Recommendations for Claude-Hybrid

### Architectural Principles

1. **Single DI Container**
   - One container, registered at startup
   - Use Python's native duck typing instead of interface explosion
   - Services register themselves, container resolves dependencies

2. **Single Configuration System**
   - One Config class (can be based on current `core/config.py` but simplified)
   - Load YAML, merge with env vars, apply defaults
   - Target: 200-300 LOC max

3. **Flat Service Structure**
   ```
   services/
       agent_deployer.py      # Single file, <300 LOC
       skill_deployer.py      # Single file, <200 LOC
       hook_manager.py        # Single file, <300 LOC
       memory_manager.py      # Single file, <200 LOC
   ```

4. **Minimal Exception Hierarchy**
   ```python
   class MPMError(Exception): pass
   class ConfigError(MPMError): pass
   class DeployError(MPMError): pass
   class HookError(MPMError): pass
   class ValidationError(MPMError): pass
   ```

5. **Two Cache Layers Maximum**
   - In-memory LRU (from `core/cache.py`)
   - Disk cache (simple JSON files)

### File Structure Target

```
claude_hybrid/
    __init__.py
    __main__.py
    config.py              # <300 LOC
    container.py           # <200 LOC
    exceptions.py          # <100 LOC
    cache.py               # <400 LOC (from current)

    cli/
        __init__.py
        parser.py
        commands.py        # All commands in one file, dispatch by subparser

    services/
        __init__.py
        agent_deployer.py  # <300 LOC
        skill_deployer.py  # <200 LOC
        hook_manager.py    # <300 LOC
        session.py         # <200 LOC (exec handoff)

    hooks/
        __init__.py
        event_handlers.py  # <300 LOC
        memory_hook.py     # <200 LOC

    models/
        __init__.py
        agent.py           # Dataclasses only, <100 LOC
        config.py          # Dataclasses only, <100 LOC
```

**Target Total:** ~3,000-4,000 LOC (vs. current ~100,000+ LOC)

### What To Port Directly

1. **`os.execvpe()` pattern** from `interactive_session.py`
2. **LRU cache implementation** from `core/cache.py`
3. **Hook event types** (PreToolUse, PostToolUse, etc.)
4. **Config file loading** (YAML support, env var override)
5. **Agent template format** (markdown with frontmatter)

### What To Rewrite Simply

1. **Agent deployment:** shutil.copy with basic validation
2. **Config:** Dataclass + YAML loader, ~200 LOC
3. **CLI:** Single argparse setup, command dispatch
4. **DI Container:** Simple dict-based registration, ~100 LOC

### What To Delete Entirely

1. All "Unified" services/configs (dead weight)
2. Pipeline/Strategy/Facade patterns
3. 90% of validation subsystem
4. Interface explosion (I* classes)
5. Duplicate exception hierarchies
6. 70 of 72 deployment files

---

## Summary Metrics

| Metric | Current | Target for Claude-Hybrid |
|--------|---------|--------------------------|
| Python files | 737 | ~30-40 |
| Total LOC | ~100,000+ | ~3,000-4,000 |
| DI Containers | 3 | 1 |
| Config Systems | 4 | 1 |
| Cache Implementations | 11 | 2 |
| Exception Classes | 81+ | 5-10 |
| Deployment Files | 72 | 1-2 |
| Complexity per file | Many >40 | All <15 |

---

## Conclusion

The claude-mpm architecture suffers from "enterprise-itis" - patterns appropriate for large Java applications applied to what should be a simple Python tool. The core value (deploy files, exec to Claude) is buried under layers of abstraction.

**For Claude-Hybrid:**
- KEEP the exec handoff pattern
- KEEP the hook event system concept
- KEEP the agent/skill deployment concept
- REFACTOR everything to be 10x simpler
- REJECT 80% of the code

The goal should be a tool that any developer can understand in an afternoon, not an architecture that requires a 1600-line document to explain.
