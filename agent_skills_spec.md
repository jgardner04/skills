# Agent Skills Specification v1.0

This document defines the structure and requirements for Claude agent skills in this repository.

## Overview

A **skill** is a reusable instruction set that enhances Claude's capabilities for specific tasks. Skills are designed to be simple, portable, and easy to create.

## Minimal Skill Structure

At minimum, a skill consists of:
1. A directory with a specific name
2. A `SKILL.md` file inside that directory

```
skill-name/
└── SKILL.md
```

## Skill Naming Requirements

**Directory Name:**
- Must be lowercase
- Must use hyphens (not underscores or spaces)
- Must contain only alphanumeric characters and hyphens
- Must be descriptive and concise

**Valid Examples:**
- `api-builder`
- `data-analyzer`
- `code-reviewer`
- `mcp-builder`

**Invalid Examples:**
- `API_Builder` (uppercase, underscores)
- `data analyzer` (spaces)
- `my-skill-v2.0` (periods/special chars)

## SKILL.md Format

### Required Structure

Every `SKILL.md` file must contain:

1. **YAML Frontmatter** (required)
2. **Markdown Content** (optional but recommended)

### YAML Frontmatter

The frontmatter must be enclosed in `---` delimiters and contain valid YAML.

#### Required Fields

**`name`** (string, required)
- Must match the directory name exactly
- Same naming rules as directory (lowercase, hyphens, alphanumeric)

**`description`** (string, required)
- Explains what the skill does and when Claude should use it
- Should be 1-3 sentences
- Must include:
  - What the skill does
  - When Claude should activate it
  - Key capabilities or use cases

**Example:**
```yaml
---
name: api-builder
description: Comprehensive API endpoint builder for RESTful services with automatic documentation generation. Use when creating new APIs, designing endpoints, or generating OpenAPI specifications. Supports (1) Endpoint design, (2) Request/response schemas, (3) Authentication patterns, (4) Documentation generation.
---
```

#### Optional Fields

**`license`** (string, optional)
- Brief description of the license
- Typically references a LICENSE.txt file in the skill directory
- Examples: "Apache 2.0", "MIT", "Complete terms in LICENSE.txt"

**`allowed-tools`** (array, optional)
- List of pre-approved tools Claude can use with this skill
- Useful for restricting skill behavior
- Example: `["Read", "Write", "Bash"]`

**`metadata`** (object, optional)
- Custom key-value pairs for additional metadata
- Can include: version, author, tags, dependencies, etc.
- Example:
  ```yaml
  metadata:
    version: "1.0.0"
    author: "username"
    tags: ["api", "backend", "rest"]
  ```

### Full Example

```yaml
---
name: example-skill
description: Brief description of what this skill does and when Claude should use it. Mention specific trigger conditions and key capabilities.
license: Apache 2.0
allowed-tools:
  - Read
  - Write
  - Bash
metadata:
  version: "1.0.0"
  author: "username"
  tags: ["example", "template"]
---

# Example Skill

This is the markdown content that follows the YAML frontmatter.

## Purpose

Explain what this skill helps Claude accomplish.

## When to Use

Describe the specific scenarios when Claude should activate this skill:
- Scenario 1: ...
- Scenario 2: ...

## Instructions

Provide detailed, step-by-step instructions for Claude to follow:

1. First step
2. Second step
3. Third step

## Examples

Include concrete examples demonstrating the skill in action.

## Constraints

Document any limitations or constraints:
- Don't do X
- Always do Y
- Z is not supported

## References

Link to supporting files or external resources if needed.
```

## Supporting Files (Optional)

Skills can include additional files to support their functionality:

### scripts/
Utility scripts that assist with the skill:
- Python scripts with `requirements.txt`
- Node.js scripts with `package.json`
- Shell scripts with clear documentation

### reference/
Reference documentation:
- API documentation
- Best practices guides
- External resource links
- Tutorial content

### templates/
Template files:
- Boilerplate code
- Configuration templates
- Example implementations

### LICENSE.txt
Individual skill license (recommended):
- Each skill can have its own license
- Typically Apache 2.0 or MIT for open-source skills
- Must be compatible with repository license

## Validation Rules

### Name Validation
- Directory name must match SKILL.md `name` field exactly
- Must follow naming requirements (lowercase, hyphens, alphanumeric)

### YAML Validation
- Frontmatter must be valid YAML
- Must include required fields: `name`, `description`
- Optional fields must follow correct data types

### Content Validation
- SKILL.md must be valid Markdown after frontmatter
- Supporting files should be properly documented
- All file paths referenced in SKILL.md should exist

## Best Practices

### Description Writing
- **Be specific**: Clearly state what the skill does
- **Include triggers**: Explain when Claude should use it
- **List capabilities**: Enumerate key features if multiple exist
- **Be concise**: 1-3 sentences maximum

**Good:**
```yaml
description: Creates comprehensive test suites using pytest with fixtures and parametrization. Use when writing unit tests, integration tests, or test fixtures for Python projects. Supports (1) Test generation, (2) Fixture creation, (3) Mocking patterns, (4) Coverage analysis.
```

**Bad:**
```yaml
description: Helps with testing
```

### Instruction Writing
- Use clear, imperative language
- Break complex tasks into steps
- Include concrete examples
- Document edge cases and constraints
- Reference supporting files when relevant

### File Organization
- Keep related files together
- Use subdirectories for scripts, reference, templates
- Include README files in subdirectories if helpful
- Maintain consistent naming conventions

### Documentation Standards
- Use proper Markdown formatting
- Include code blocks with syntax highlighting
- Add links to external resources
- Keep line length reasonable (80-100 characters)
- Use headings to structure content

### Security Considerations
- Never include hardcoded credentials
- Validate all inputs in supporting scripts
- Document security considerations
- Follow secure coding practices
- Use environment variables for sensitive data

## Version History

**v1.0** (Initial Release)
- Defined minimal skill structure
- Specified required and optional frontmatter fields
- Established naming conventions
- Documented validation rules and best practices
