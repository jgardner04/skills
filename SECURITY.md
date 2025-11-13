# Security Policy

## Reporting a Vulnerability

We take the security of this skills marketplace seriously. If you discover a security vulnerability, please help us by reporting it responsibly.

### How to Report

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them in one of the following ways:

1. **Preferred**: Use GitHub's private vulnerability reporting feature:
   - Go to the [Security tab](https://github.com/jgardner04/skills/security)
   - Click "Report a vulnerability"
   - Fill out the form with details

2. **Alternative**: Open a private security advisory:
   - Navigate to https://github.com/jgardner04/skills/security/advisories/new
   - Provide detailed information about the vulnerability

3. **Email**: If the above options are not available, you can contact the maintainer directly through GitHub.

### What to Include

When reporting a vulnerability, please include:

- **Type of vulnerability**: (e.g., XSS, command injection, hardcoded credentials)
- **Location**: Which skill(s) or file(s) are affected
- **Step-by-step reproduction**: How to reproduce the issue
- **Impact**: What an attacker could potentially do
- **Affected versions**: If applicable
- **Suggested fix**: If you have recommendations

### Example Report

```
**Vulnerability Type**: Command Injection
**Location**: data-processor/scripts/process.py
**Affected Versions**: All versions

**Description**:
The script accepts user input without sanitization and passes it directly to
subprocess.call(), allowing arbitrary command execution.

**Reproduction Steps**:
1. Run the script with: python process.py "; rm -rf /"
2. Commands after the semicolon are executed

**Impact**:
Attackers could execute arbitrary system commands with the permissions of the
user running the script.

**Suggested Fix**:
Use subprocess.run() with shell=False and pass arguments as a list instead of
a string.
```

## Security Best Practices for Contributors

When creating or modifying skills, please follow these security guidelines:

### 1. No Hardcoded Credentials
- Never include API keys, tokens, passwords, or credentials
- Use environment variables for sensitive data
- Document required environment variables in README

**Bad:**
```python
API_KEY = "sk-1234567890abcdef"
```

**Good:**
```python
import os
API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable required")
```

### 2. Input Validation
- Validate and sanitize all user inputs
- Use parameterized queries for databases
- Escape output when rendering user data

**Bad:**
```python
subprocess.call(f"echo {user_input}", shell=True)
```

**Good:**
```python
subprocess.run(["echo", user_input], shell=False)
```

### 3. Dependency Security
- Keep dependencies up to date
- Use pinned versions in requirements.txt or package.json
- Audit dependencies for known vulnerabilities
- Minimize dependency count

### 4. File System Access
- Validate file paths to prevent directory traversal
- Use absolute paths when possible
- Restrict file access to intended directories
- Never execute files from untrusted sources

**Bad:**
```python
file_path = user_input  # Could be ../../etc/passwd
with open(file_path) as f:
    return f.read()
```

**Good:**
```python
import os
base_dir = "/safe/directory"
file_name = os.path.basename(user_input)  # Strip any path components
file_path = os.path.join(base_dir, file_name)
if not file_path.startswith(base_dir):
    raise ValueError("Invalid file path")
```

### 5. Command Execution
- Avoid shell=True when using subprocess
- Pass arguments as lists, not strings
- Sanitize all inputs used in commands
- Use least privilege principle

### 6. Web Requests
- Validate and sanitize URLs
- Use HTTPS when possible
- Set appropriate timeouts
- Handle errors securely (don't leak sensitive info)

### 7. Data Privacy
- Don't log sensitive information
- Handle personal data appropriately
- Document data collection in skill README
- Follow data minimization principles

## Scope

This security policy applies to:

- All skills in this repository
- Supporting scripts and utilities
- Configuration files
- Documentation that includes code examples

## Response Timeline

When you report a vulnerability:

- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 5 business days
- **Status Updates**: Every 10 business days until resolved
- **Resolution**: Timeline depends on severity and complexity

### Severity Levels

**Critical**: Immediate attention (remote code execution, data breach)
- Target fix: Within 7 days

**High**: High priority (privilege escalation, significant data exposure)
- Target fix: Within 30 days

**Medium**: Normal priority (minor data exposure, DoS)
- Target fix: Within 90 days

**Low**: Low priority (information disclosure, minor issues)
- Target fix: Best effort

## Public Disclosure

- Vulnerabilities will not be publicly disclosed until a fix is available
- We will coordinate disclosure timing with the reporter
- Credit will be given to reporters in security advisories (if desired)
- We follow responsible disclosure practices

## Security Updates

Security updates will be communicated through:

- GitHub Security Advisories
- Repository CHANGELOG.md
- Git tags for patched versions
- Release notes

## Out of Scope

The following are generally considered out of scope:

- Vulnerabilities in third-party dependencies (report to upstream)
- Social engineering attacks
- Physical attacks
- Issues requiring physical access to systems
- Browser-specific bugs (report to browser vendors)

## Recognition

We appreciate security researchers who help keep this project secure. With your permission, we will:

- Credit you in the security advisory
- List you in our SECURITY_CONTRIBUTORS.md file (if created)
- Mention you in release notes

## Questions

If you have questions about this security policy, please open a public issue (for non-sensitive questions) or contact the maintainer through GitHub.

Thank you for helping keep the Skills Marketplace secure!
