# Claude Skills Technical Specification

Complete technical requirements and validation rules for Claude skills.

## File Structure

### Required Files

**SKILL.md** - The main skill definition file
- Must be named exactly `SKILL.md` (case-sensitive)
- Must be UTF-8 encoded
- Must start with YAML frontmatter
- Must contain content after frontmatter

### Optional Components

**scripts/** - Helper scripts and utilities
- Python, JavaScript, or bash scripts
- Should include `__init__.py` for Python packages
- Scripts should have execute permissions (Unix)
- Must not execute arbitrary code (no eval/exec)

**references/** - Reference documentation
- Markdown files with detailed specifications
- API documentation
- Database schemas
- Templates and examples
- Loaded on-demand to minimize token usage

**README.md** - Skill-specific documentation
- Installation instructions
- Usage examples
- Platform-specific notes

## YAML Frontmatter Specification

### Format

```yaml
---
name: skill-name
description: Brief description of what this skill does
---
```

### Required Fields

#### name (string, required)
- **Type**: String
- **Required**: Yes
- **Format**: Lowercase letters, numbers, hyphens only
- **Pattern**: `^[a-z0-9-]+$`
- **Min length**: 1 character
- **Max length**: 64 characters
- **Restrictions**:
  - Cannot contain "anthropic" (case-insensitive)
  - Cannot contain "claude" (case-insensitive)
  - Cannot contain XML tags (`<` or `>`)
  - Must not start or end with hyphen
  - No consecutive hyphens

**Examples**:
- ✅ Valid: `git-helper`, `api-tester`, `doc-writer-pro`
- ❌ Invalid: `GitHelper` (not lowercase), `api_tester` (underscore), `my-anthropic-skill` (contains "anthropic")

#### description (string, required)
- **Type**: String
- **Required**: Yes
- **Min length**: 1 character (after trimming whitespace)
- **Max length**: 1024 characters
- **Restrictions**:
  - Cannot be only whitespace
  - Cannot contain XML tags (regex: `<[^>]+>`)
  - Should explain WHAT the skill does
  - Should explain WHEN to use it

**Best Practices**:
- Use action-oriented language for auto-invocation
- Include trigger keywords
- Be specific about capabilities
- Mention platform requirements if relevant

**Examples**:
- ✅ Good: "Create and validate git commit messages following Conventional Commits. Use when writing commits or reviewing commit history."
- ✅ Good: "Analyze API responses and generate test cases. Use PROACTIVELY when designing or testing REST APIs."
- ❌ Poor: "Helps with git" (too vague, no trigger info)
- ❌ Poor: "A tool" (doesn't explain what or when)

### Optional Fields

#### tools (string or array, optional)
Specifies which tools this skill should have access to.

- **Type**: String (comma-separated) or Array
- **Default**: All tools (if omitted)
- **Valid tools**:
  - `Bash` - Execute shell commands
  - `Read` - Read files
  - `Write` - Write new files
  - `Edit` - Edit existing files
  - `Glob` - Find files by pattern
  - `Grep` - Search file contents
  - `WebFetch` - Fetch web pages
  - `WebSearch` - Search the web
  - `Task` - Launch subagents

**Examples**:
```yaml
# String format
tools: Bash, Read, Write

# Array format
tools:
  - Bash
  - Read
  - Write
```

**Use Cases**:
- Restrict to Read/Write for documentation-only skills
- Include Bash for scripts that need command execution
- Include WebFetch/WebSearch for research skills

#### model (string, optional)
Specifies which model to use for this skill.

- **Type**: String
- **Default**: Inherits from parent context
- **Valid values**:
  - `sonnet` - Claude Sonnet (balanced)
  - `opus` - Claude Opus (most capable)
  - `haiku` - Claude Haiku (fastest, most efficient)
  - `inherit` - Use parent context's model

**Examples**:
```yaml
# Use Haiku for fast, simple tasks
model: haiku

# Use Sonnet for complex reasoning
model: sonnet
```

## Content Requirements

### Body Structure

The content after frontmatter should be well-structured markdown:

#### Recommended Sections

1. **Overview/Introduction**
   - Brief explanation of the skill
   - Use cases

2. **When to Use This Skill**
   - Specific scenarios
   - Trigger conditions
   - Context where skill is most helpful

3. **Instructions/Workflow**
   - Step-by-step guidance
   - Clear action items
   - Decision points

4. **Examples**
   - Concrete use cases
   - Input/output examples
   - Edge cases

5. **Best Practices** (optional)
   - Tips for optimal use
   - Common patterns

6. **Troubleshooting** (optional)
   - Common issues
   - Solutions
   - Error handling

### Markdown Guidelines

- Use proper heading hierarchy (don't skip levels)
- Use code blocks with language tags
- Use lists for steps and options
- Use emphasis (bold/italic) sparingly for clarity
- Include links to external resources if helpful

### Token Efficiency

**Inactive State** (Just frontmatter loaded):
- Target: 30-50 tokens
- The name and description should be concise

**Active State** (Full SKILL.md loaded):
- Keep main instructions focused
- Move detailed specs to references/
- Use progressive disclosure

**References** (Loaded on-demand):
- No token limit
- Can be very detailed
- Include comprehensive examples
- Add API specs, schemas, etc.

## File Size Limits

- **SKILL.md**: Recommended max 50KB (will warn above this)
- **Scripts**: Reasonable size (< 1MB each)
- **References**: No strict limit, but keep focused
- **Total package**: Recommended < 10MB

## Security Requirements

### Path Safety

All file operations must:
- Validate paths to prevent traversal attacks
- Use pathlib.Path for cross-platform compatibility
- Resolve paths and check they're within expected directories
- Never accept arbitrary user paths without validation

**Example** (Python):
```python
from pathlib import Path

def safe_path(base: Path, user_input: str) -> Path:
    resolved = (base / user_input).resolve()
    if not resolved.is_relative_to(base):
        raise ValueError(f"Path traversal detected: {user_input}")
    return resolved
```

### Input Validation

- Validate all user inputs
- Use allowlists instead of denylists
- Sanitize before processing
- Check types, ranges, formats
- Provide clear error messages

### Code Execution

- **Never** use `eval()` or `exec()`
- **Never** execute arbitrary user code
- Be cautious with `pickle` - prefer JSON
- Validate file contents before processing
- Use subprocess carefully with fixed commands

### Credentials and Secrets

- Never include credentials in skill files
- Use environment variables
- Document required env vars in README
- Add secrets to .gitignore
- Use permission rules in .claude/settings.json

## Validation Checklist

Use this checklist to ensure compliance:

### Frontmatter
- [ ] File starts with `---`
- [ ] Valid YAML syntax
- [ ] Contains `name` field
- [ ] Contains `description` field
- [ ] Name is lowercase with hyphens only
- [ ] Name is 1-64 characters
- [ ] Name doesn't contain "anthropic" or "claude"
- [ ] Description is 1-1024 characters
- [ ] Description is non-empty (no whitespace-only)
- [ ] No XML tags in name or description
- [ ] Optional fields (tools, model) are valid if present

### Body Content
- [ ] Content exists after frontmatter
- [ ] Reasonable length (not too short)
- [ ] Includes "When to Use" section
- [ ] Includes instructions/steps
- [ ] Includes examples
- [ ] Uses proper markdown formatting
- [ ] Headings are hierarchical

### Directory Structure
- [ ] SKILL.md exists
- [ ] If scripts/ exists, contains relevant files
- [ ] If scripts/ has Python files, includes __init__.py
- [ ] Scripts have execute permissions (Unix)
- [ ] If references/ exists, contains markdown files
- [ ] No sensitive files (credentials, keys)

### Security
- [ ] No eval/exec in scripts
- [ ] Path operations are safe
- [ ] Inputs are validated
- [ ] No hardcoded credentials
- [ ] No path traversal vulnerabilities

### Quality
- [ ] Clear, actionable instructions
- [ ] Concrete examples provided
- [ ] Error handling documented
- [ ] Platform notes if needed
- [ ] Tested on target platforms

## Platform-Specific Requirements

### Claude.ai
- User-level skills only
- Upload via Skills UI
- Network access varies by settings
- No shell access to system

### Claude API
- Workspace-level skills
- No network access by default
- No dynamic package installation
- Integrated via API configuration

### Claude Code
- Project (.claude/skills/) or user level (~/.claude/agents/)
- Full network access
- Can execute bash commands
- Full file system access

## Versioning

While not required, consider versioning your skills:

**In manifest.json**:
```json
{
  "version": "1.2.0",
  "changelog": "Added support for X"
}
```

**Semantic Versioning Recommended**:
- Major: Breaking changes
- Minor: New features (backward compatible)
- Patch: Bug fixes

## Distribution Formats

### ZIP Package
```
skill-name.zip
├── SKILL.md
├── manifest.json (optional)
├── README.md (optional)
├── scripts/
│   └── *.py
└── references/
    └── *.md
```

### Directory Structure
```
skill-name/
├── SKILL.md
├── manifest.json (optional)
├── README.md (optional)
├── scripts/
│   └── *.py
└── references/
    └── *.md
```

### Plugin Format (.claude-plugin/)
```
.claude-plugin/
├── SKILL.md
├── scripts/
└── references/
```

## Manifest File (Optional)

When packaging, you can include a manifest.json:

```json
{
  "name": "skill-name",
  "description": "Brief description",
  "version": "1.0.0",
  "packaged_at": "2025-01-15T10:30:00Z",
  "format": "claude-skill",
  "format_version": "1.0",
  "includes_scripts": true,
  "includes_references": true,
  "tools": "Bash, Read, Write",
  "model": "sonnet"
}
```

## Common Validation Errors

### Error: "SKILL.md must start with YAML frontmatter"
**Cause**: File doesn't start with `---`
**Fix**: Add frontmatter at the beginning:
```yaml
---
name: skill-name
description: Description here
---
```

### Error: "Invalid YAML in frontmatter"
**Cause**: YAML syntax error
**Fix**: Check indentation, quotes, special characters
- Strings with `:` need quotes
- Multi-line strings need `|` or `>`
- Indentation must be consistent

### Error: "Skill name must be lowercase with hyphens only"
**Cause**: Name has uppercase, underscores, spaces, or special chars
**Fix**: Use only lowercase letters, numbers, and hyphens

### Error: "Description too long"
**Cause**: Description exceeds 1024 characters
**Fix**: Shorten description, move details to body

### Error: "Required field 'name' missing"
**Cause**: Frontmatter doesn't include name field
**Fix**: Add `name: skill-name` to frontmatter

## Testing Your Skill

1. **Validate**: Run the validator
   ```bash
   python .claude-plugin/scripts/validate_skill.py path/to/skill/
   ```

2. **Manual Testing**: Place skill and try using it
   - Test basic functionality
   - Test edge cases
   - Test error handling
   - Test on target platforms

3. **Script Testing**: If your skill includes scripts
   - Test scripts independently
   - Verify inputs/outputs
   - Check error messages
   - Test on different platforms

4. **Integration Testing**: Use skill in real scenarios
   - Invoke automatically
   - Invoke explicitly
   - Test with references
   - Test tool permissions

## Further Resources

- **Claude Skills Documentation**: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview
- **Skills Blog Post**: https://claude.com/blog/skills
- **Skills Cookbook**: https://github.com/anthropics/claude-cookbooks/tree/main/skills
- **This Project**: https://github.com/jgardner04/claude-skills-skill
