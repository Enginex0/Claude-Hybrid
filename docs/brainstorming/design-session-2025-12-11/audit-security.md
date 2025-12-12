# Security Audit Report: claude-mpm

**Audit Date:** 2025-12-11
**Auditor:** Security Specialist Agent
**Codebase Version:** 5.1.2 (Enginex0/claude-mpm fork)
**Target Directory:** `/home/president/bmad-systems/claude-mpm/src/claude_mpm/`

---

## Executive Summary

The claude-mpm codebase has several security concerns that should be addressed in Claude-Hybrid. The most critical findings involve **insecure deserialization using pickle**, **command injection vulnerabilities via shell=True**, and the **unconditional use of --dangerously-skip-permissions flag**. The codebase does have some positive security patterns including path traversal validation and dangerous pattern detection in hooks. Overall security posture: **MODERATE RISK** - functional but needs hardening before production use.

---

## CRITICAL (Fix Before Porting)

| File:Line | Vulnerability | Severity | Fix Required |
|-----------|---------------|----------|--------------|
| `core/cache.py:407` | **Insecure Deserialization (pickle.load)** - Cache loading uses pickle without integrity verification. Malicious cache files could execute arbitrary code. | CRITICAL | Replace pickle with JSON or implement HMAC verification of cache files. |
| `storage/state_storage.py:199-202` | **Insecure Deserialization (pickle.load)** - State storage uses pickle for both compressed and uncompressed data. | CRITICAL | Use JSON with msgpack fallback for binary data, or implement signed serialization. |
| `services/memory/indexed_memory.py:225,601` | **Insecure Deserialization (pickle.load)** - Memory index loading uses pickle. | CRITICAL | Migrate to secure serialization format. |
| `cli/commands/postmortem.py:255` | **Command Injection (shell=True)** - Auto-fix commands executed with shell=True from user-defined action.commands list. | CRITICAL | Use subprocess.run() with argument list instead of shell=True. |
| `services/self_upgrade_service.py:406` | **Command Injection (shell=True)** - Upgrade commands executed with shell=True. | CRITICAL | Parse and validate command before execution, use argument list. |
| `core/interactive_session.py:397` | **Dangerous Flag Always Enabled** - `--dangerously-skip-permissions` is unconditionally added to claude command. | CRITICAL | Make this opt-in based on explicit user configuration. |
| `core/oneshot_session.py:328` | **Dangerous Flag Always Enabled** - Same issue in oneshot session mode. | CRITICAL | Make permission bypass opt-in. |

---

## HIGH (Should Fix in Claude-Hybrid)

| File:Line | Issue | Risk | Mitigation |
|-----------|-------|------|------------|
| `skills/bundled/testing/webapp-testing/scripts/with_server.py:89-92` | **shell=True in subprocess.Popen** - Server commands run with shell=True for cd/&& support. | HIGH | Refactor to change directory with cwd parameter and run commands separately. |
| `config/model_config.py:285-286` | **API Key in Environment** - API keys read from environment without encryption. | HIGH | Consider secure secret storage (keyring, vault) for sensitive credentials. |
| `hooks/claude_hooks/installer.py:381` | **chmod on script** - Making scripts executable could enable malicious script execution. | HIGH | Validate script content/source before chmod. |
| `dashboard/` | **No Authentication** - Dashboard server (aiohttp) has no authentication mechanism. | HIGH | Implement at least basic authentication for dashboard access. |
| `dashboard/` | **No Rate Limiting** - Socket.IO server lacks rate limiting, vulnerable to DoS. | HIGH | Implement per-client rate limiting. |

---

## MEDIUM (Best Practice Violations)

| File:Line | Issue | Recommendation |
|-----------|-------|----------------|
| `core/api_validator.py:98-280` | **No Request Timeout Variance** - Hardcoded 10-second timeout across all API calls. | Use adaptive timeouts based on operation type. |
| `hooks/validation_hooks.py:144-151` | **Basic Pattern Matching** - Dangerous pattern detection uses simple string matching, easily bypassed. | Implement AST-based analysis for code patterns. |
| `utils/subprocess_utils.py:67` | **Comment suggests avoiding shell=True** - Good practice but not enforced programmatically. | Add static analysis rule to detect shell=True usage. |
| `config/socketio_config.py` | **JSON Config without Schema Validation** - Config files loaded without schema validation. | Add JSON schema validation for config files. |
| `services/unified/config_strategies/error_handling_strategy.py:345` | **ast.literal_eval usage** - While safer than eval(), still processes arbitrary strings. | Prefer explicit parsing for known data formats. |
| Multiple files | **Logging without Sanitization** - Potential for log injection if user data logged. | Sanitize user input before logging. |

---

## LOW (Minor Improvements)

| File:Line | Issue | Suggestion |
|-----------|-------|------------|
| `core/file_utils.py:30,44` | **Default permissions 0o755** - May be more permissive than needed. | Consider 0o700 for user-only directories. |
| `scripts/socketio_daemon.py` | **PID File without Lock** - Race condition possible on daemon start. | Use file locking for PID file. |
| `tools/code_tree_builder.py:84` | **Gitignore parsing** - Custom parsing without security validation. | Use pathspec library consistently. |
| `config/experimental_features.py:85-86` | **Environment Variable Parsing** - Boolean parsing could be more robust. | Use strict boolean parsing. |

---

## Secrets Scan Results

### Hardcoded Secrets Found: NONE

The codebase properly uses environment variables for secrets:
- `ANTHROPIC_API_KEY` - API key for Claude
- `CLAUDE_MAX_TOKENS`, `CLAUDE_MODEL` - Configuration values
- `OLLAMA_*` - Ollama configuration
- `MODEL_PROVIDER` - Provider selection

### Secret Handling Patterns (GOOD):
- API keys loaded from environment: `/config/model_config.py:285-286`
- `.env` file guidance in documentation
- No hardcoded credentials detected in codebase

### Secret Handling Concerns:
1. API keys stored in plaintext in environment (standard but not ideal)
2. No secure secret storage integration (e.g., keyring, vault)
3. Comments mention API keys in `/config/model_config.py:406` example config

---

## Dangerous Pattern Scan

### pickle.load Usage (CRITICAL - Arbitrary Code Execution Risk)

| Location | Context | Risk |
|----------|---------|------|
| `core/cache.py:407` | Cache persistence loading | Cache file tampering leads to code execution |
| `storage/state_storage.py:199` | Compressed state loading | State file tampering leads to code execution |
| `storage/state_storage.py:202` | Uncompressed state loading | State file tampering leads to code execution |
| `services/memory/indexed_memory.py:225` | Memory index loading | Index file tampering leads to code execution |
| `services/memory/indexed_memory.py:601` | Combined indexes loading | Index file tampering leads to code execution |

### shell=True Usage (HIGH - Command Injection Risk)

| Location | Context | Controllable Input? |
|----------|---------|---------------------|
| `cli/commands/postmortem.py:255` | Auto-fix command execution | YES - from action.commands |
| `services/self_upgrade_service.py:406` | Package upgrade | Partially - from update_info |
| `skills/.../with_server.py:92` | Server process launch | YES - from server config |

### os.execvpe Usage (Process Replacement)

| Location | Purpose | Security Impact |
|----------|---------|-----------------|
| `core/interactive_session.py:585` | Launch Claude Code | Intentional - but uses dangerous flag |
| `services/self_upgrade_service.py:437-443` | Restart after upgrade | Intentional process replacement |

### eval/exec Patterns

No direct `eval()` or `exec()` usage in production code paths. The codebase properly warns about these in:
- `hooks/validation_hooks.py:149-150` - Blocked patterns list
- `skills/bundled/json-data-handling.md` - Documentation warning

---

## Input Validation Analysis

### Good Patterns Found:

1. **Path Traversal Prevention** (`skills/skills_service.py:91-105`)
   ```python
   def _validate_safe_path(self, base: Path, target: Path) -> bool:
       try:
           target.resolve().relative_to(base.resolve())
           return True
       except ValueError:
           return False
   ```
   This is used at lines 287-289 and 586-588.

2. **Dangerous Task Pattern Detection** (`hooks/validation_hooks.py:144-157`)
   - Blocks: `rm -rf /`, `sudo rm`, `format c:`, `__import__`, `eval(`, `exec(`
   - Applied before task execution

3. **Tool Analysis Patterns** (`hooks/claude_hooks/tool_analysis.py:166`)
   - Detects `chmod 777` as suspicious

### Gaps in Input Validation:

1. **No Input Sanitization for Logging** - User-provided data logged without sanitization
2. **String-based Pattern Matching** - Easily bypassed with encoding or obfuscation
3. **No YAML SafeLoader Verification** - Could not find explicit yaml.safe_load enforcement
4. **Socket.IO Event Data** - No schema validation on incoming events

---

## Authentication/Authorization Analysis

### Current State: MINIMAL

1. **Dashboard**: No authentication - anyone with network access can view
2. **MCP Gateway**: No authentication layer
3. **API Validation**: Only validates API keys exist, no permission scoping
4. **Claude Code**: Runs with `--dangerously-skip-permissions` always

### Recommendations:
1. Add HTTP Basic Auth or token-based auth to dashboard
2. Implement MCP tool permission scoping
3. Make `--dangerously-skip-permissions` opt-in only

---

## Dependency Security Analysis

### Python Version: 3.11+ (GOOD - Recent, supported)

### Key Dependencies Review:

| Package | Version | Known Vulnerabilities | Notes |
|---------|---------|----------------------|-------|
| `requests>=2.25.0` | Minimum version | CVE-2023-32681 (<2.31.0) | Update minimum to 2.31.0 |
| `flask>=3.0.0` | Recent | Clean | Good |
| `aiohttp>=3.9.0` | Recent | Clean | Good |
| `pyyaml>=6.0` | Recent | Clean | Good |
| `anthropic>=0.40.0` | Recent | Clean | Good |
| `pillow>=9.0.0` | In agents extra | CVE-2023-44271 (<10.0.1) | Update to >=10.0.1 |
| `lxml>=4.9.0` | In data-processing | Clean | Good |
| `cryptography` | Not listed | N/A | Consider adding for secure operations |

### Recommendations:
1. Update `requests` minimum to `>=2.31.0`
2. Update `pillow` minimum to `>=10.0.1`
3. Add dependency scanning to CI/CD (e.g., `pip-audit`, `safety`)
4. Consider adding `cryptography` for HMAC signing of serialized data

---

## Security Recommendations for Claude-Hybrid

### Priority 1: Critical Fixes

1. **Replace pickle with JSON/msgpack**
   ```python
   # Instead of pickle.load
   import json
   with open(cache_path, 'r') as f:
       data = json.load(f)
   ```
   For binary data, use msgpack with schema validation.

2. **Eliminate shell=True**
   ```python
   # Instead of
   subprocess.run(cmd, shell=True)
   # Use
   subprocess.run(shlex.split(cmd))
   # Or better, pass explicit argument list
   subprocess.run(['pip', 'install', 'package'])
   ```

3. **Make --dangerously-skip-permissions opt-in**
   ```python
   cmd = ["claude"]
   if self.config.skip_permissions:  # Explicit opt-in
       cmd.append("--dangerously-skip-permissions")
   ```

### Priority 2: High Importance

4. **Add Dashboard Authentication**
   ```python
   from aiohttp_basicauth import BasicAuthMiddleware
   auth = BasicAuthMiddleware(username='admin', password=os.getenv('DASHBOARD_PASSWORD'))
   app = web.Application(middlewares=[auth])
   ```

5. **Implement Rate Limiting**
   ```python
   from aiolimiter import AsyncLimiter
   rate_limit = AsyncLimiter(100, 60)  # 100 requests per minute
   ```

6. **Add HMAC verification for cache files** (if keeping binary format)
   ```python
   import hmac
   import hashlib

   def verify_cache(data: bytes, signature: bytes, key: bytes) -> bool:
       expected = hmac.new(key, data, hashlib.sha256).digest()
       return hmac.compare_digest(expected, signature)
   ```

### Priority 3: Best Practices

7. **Add Security Headers**
   ```python
   @app.middleware
   async def security_headers(request, handler):
       response = await handler(request)
       response.headers['X-Content-Type-Options'] = 'nosniff'
       response.headers['X-Frame-Options'] = 'DENY'
       response.headers['Content-Security-Policy'] = "default-src 'self'"
       return response
   ```

8. **Implement Input Schema Validation**
   ```python
   from pydantic import BaseModel, validator

   class EventData(BaseModel):
       event_type: str
       payload: dict

       @validator('event_type')
       def validate_event_type(cls, v):
           allowed = {'tool_use', 'agent_start', 'agent_stop'}
           if v not in allowed:
               raise ValueError(f'Invalid event type: {v}')
           return v
   ```

9. **Add Dependency Scanning**
   ```yaml
   # Add to CI/CD
   - name: Security scan
     run: |
       pip install pip-audit
       pip-audit --strict
   ```

10. **Implement Secure Secret Storage**
    ```python
    import keyring

    def get_api_key(service: str) -> str:
        # Try keyring first, fall back to env
        key = keyring.get_password('claude-mpm', service)
        if not key:
            key = os.getenv(f'{service}_API_KEY')
        return key
    ```

---

## Security Checklist for Claude-Hybrid Development

### Before Each Feature:
- [ ] Input validation implemented for all user-provided data
- [ ] Output encoding applied where appropriate
- [ ] No shell=True in subprocess calls
- [ ] No pickle for untrusted data
- [ ] Secrets stored securely (not hardcoded)

### Before Release:
- [ ] Dependency audit passed (pip-audit)
- [ ] No new pickle.load calls
- [ ] No new shell=True calls
- [ ] Authentication required for network services
- [ ] Rate limiting implemented
- [ ] Security headers configured

### Ongoing:
- [ ] Regular dependency updates
- [ ] Security-focused code review
- [ ] Penetration testing (when applicable)

---

## Appendix: Files Reviewed

### Core Components
- `/home/president/bmad-systems/claude-mpm/src/claude_mpm/core/cache.py`
- `/home/president/bmad-systems/claude-mpm/src/claude_mpm/core/interactive_session.py`
- `/home/president/bmad-systems/claude-mpm/src/claude_mpm/core/oneshot_session.py`
- `/home/president/bmad-systems/claude-mpm/src/claude_mpm/core/api_validator.py`
- `/home/president/bmad-systems/claude-mpm/src/claude_mpm/core/file_utils.py`

### Storage & Memory
- `/home/president/bmad-systems/claude-mpm/src/claude_mpm/storage/state_storage.py`
- `/home/president/bmad-systems/claude-mpm/src/claude_mpm/services/memory/indexed_memory.py`

### CLI & Commands
- `/home/president/bmad-systems/claude-mpm/src/claude_mpm/cli/commands/postmortem.py`
- `/home/president/bmad-systems/claude-mpm/src/claude_mpm/cli/startup.py`

### Services
- `/home/president/bmad-systems/claude-mpm/src/claude_mpm/services/self_upgrade_service.py`
- `/home/president/bmad-systems/claude-mpm/src/claude_mpm/services/unified/analyzer_strategies/security_analyzer.py`

### Configuration
- `/home/president/bmad-systems/claude-mpm/src/claude_mpm/config/model_config.py`
- `/home/president/bmad-systems/claude-mpm/src/claude_mpm/config/socketio_config.py`
- `/home/president/bmad-systems/claude-mpm/pyproject.toml`

### Hooks & Validation
- `/home/president/bmad-systems/claude-mpm/src/claude_mpm/hooks/validation_hooks.py`
- `/home/president/bmad-systems/claude-mpm/src/claude_mpm/hooks/claude_hooks/installer.py`
- `/home/president/bmad-systems/claude-mpm/src/claude_mpm/hooks/claude_hooks/tool_analysis.py`

### Skills
- `/home/president/bmad-systems/claude-mpm/src/claude_mpm/skills/skills_service.py`
- `/home/president/bmad-systems/claude-mpm/src/claude_mpm/skills/bundled/testing/webapp-testing/scripts/with_server.py`

---

*Report generated by Security Specialist Agent*
*Audit methodology: OWASP Top 10 + Python-specific security patterns*
