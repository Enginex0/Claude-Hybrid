# D8 Session Roundup

**Decision Area:** Plugin & Agent Format
**Status:** Not Started
**Questions:** 0/20 complete

## Current Position
- Starting fresh with Q1
- No decisions made yet

## Topics Covered

### Plugin Manifest Format (Q1-Q4)
- Required fields in plugin.json
- Versioning structure
- Dependency declarations
- Naming and directory enforcement

### Agent Frontmatter Schema (Q5-Q8)
- Required frontmatter fields
- Description structure for Task tool matching
- Skills auto-loading specification
- Model selection options

### Permission Modes (Q9-Q12)
- Supported permission modes
- Global vs agent permission interaction
- User acknowledgment for bypass
- Subagent permission inheritance

### Plugin Discovery Mechanism (Q13-Q16)
- Plugin discovery paths
- Plugin enablement control
- Plugin identifier format
- Component discovery within plugins

### Agent Format Specification (Q17-Q20)
- Embedded configuration support
- Response gate enforcement
- File naming and Task tool matching
- Plugin namespacing in subagent_type

## Source Documents Analyzed
1. `/home/president/bmad-systems/claude-code-architecture/03-EXTENSION-SYSTEM.md`
   - Plugin directory structure
   - Plugin manifest schema
   - Agent file format and YAML frontmatter
   - Task tool matching patterns
   - Skill and command systems

2. `/home/president/bmad-systems/claude-code-architecture/05-CONFIGURATION.md`
   - settings.json full schema
   - enabledPlugins format
   - Permission modes (default/bypassPermissions)
   - Configuration hierarchy

3. `/home/president/bmad-systems/personal bmad/BMAD-PERSONAL-ARCHITECTURE.md`
   - Agent format specification with response gates
   - Session config embedded in agents
   - Color reference for agent domains
   - Orchestration model patterns

## Resume Instructions
1. Read D8-QUESTIONS.md
2. Present Q1 options to President
3. Record decision in progress.txt
4. Update state.json

## Context for Next Session
This workspace is INDEPENDENT. You can work on D8 while other Claude sessions work on D6-D7, D9-D10 simultaneously.

## Key Patterns from Sources

### Claude Code Plugin Structure
```
plugin-name/
  .claude-plugin/
    plugin.json        # {"name": "plugin-name", "version": "1.0.0", ...}
  agents/
    agent-name.md      # YAML frontmatter + persona content
  skills/
    skill-name/
      SKILL.md
  commands/
    command-name.md
```

### Claude Code Agent Frontmatter
```yaml
---
name: agent-name
description: "Usage guidance..."
model: inherit|sonnet|opus|haiku
permissionMode: default|bypassPermissions
skills: skill1, skill2
color: orange
---
```

### BMAD Extended Agent Format
```yaml
---
name: agent-name
description: |
  Use this agent when [triggers]...
  <example>
  Context: ...
  </example>
model: inherit
color: green
---

<session_config>
  user_name: ...
  bmad_path: ...
</session_config>

<response_gate critical="MANDATORY">
  5-step verification protocol
</response_gate>
```

### Plugin Enablement Pattern
```json
{
  "enabledPlugins": {
    "plugin-name@marketplace": true
  }
}
```
