# Claude Skills Examples

Real-world examples of well-designed skills across different complexity levels and use cases.

## Table of Contents

1. [Simple Skills](#simple-skills) - Just SKILL.md, no scripts
2. [Skills with Scripts](#skills-with-scripts) - Including helper utilities
3. [Complex Skills](#complex-skills) - Full-featured with references
4. [Platform-Specific Skills](#platform-specific-skills) - Optimized for one platform
5. [Universal Skills](#universal-skills) - Work across all platforms

---

## Simple Skills

### Example 1: Commit Message Formatter

**Use Case**: Help developers write conventional commit messages

**Structure**:
```
commit-formatter/
└── SKILL.md
```

**SKILL.md**:
```markdown
---
name: commit-formatter
description: Format git commit messages following Conventional Commits. Use when writing commits or reviewing commit history for proper formatting.
---

# Commit Message Formatter

Helps create well-formatted git commit messages following the Conventional Commits specification.

## When to Use

- Writing new commit messages
- Reviewing existing commits for proper format
- Teaching team members commit conventions
- Generating changelogs

## Commit Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

## Types

- **feat**: New feature for users
- **fix**: Bug fix
- **docs**: Documentation only changes
- **style**: Code style changes (formatting, semicolons)
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Performance improvement
- **test**: Adding or updating tests
- **chore**: Maintenance tasks (deps, configs)
- **ci**: CI/CD changes

## Subject Line Rules

- Use imperative mood ("add" not "added")
- No period at the end
- Keep under 50 characters
- Lowercase (except proper nouns)

## Body (Optional)

- Wrap at 72 characters
- Explain WHAT and WHY (not HOW)
- Separate from subject with blank line

## Footer (Optional)

- **Breaking changes**: `BREAKING CHANGE: <description>`
- **Issue references**: `Closes #123`, `Fixes #456`
- **Co-authors**: `Co-authored-by: Name <email>`

## Examples

### Simple Feature
```
feat(auth): add OAuth2 Google login
```

### Bug Fix with Body
```
fix(api): handle null user service response

The user service occasionally returns null when the user is not
found. This adds proper null checking and returns a 404 status.
```

### Breaking Change
```
feat(api)!: redesign authentication endpoints

BREAKING CHANGE: The /auth endpoint now requires POST instead of GET.
All clients must be updated to send POST requests with JSON body
containing username and password fields.

Migration guide: https://docs.example.com/v2-migration

Closes #456
```

### Multiple Issues
```
fix(ui): resolve button alignment in mobile view

Fixes several CSS issues affecting mobile users:
- Button text now wraps properly
- Icons align correctly with text
- Touch targets meet minimum 44px requirement

Fixes #789, #790, #791
```

## Interactive Mode

Just tell me what you changed, and I'll help format it:

**Example conversation**:
- You: "I added a new login page"
- Me: "Was this a new feature or a fix?"
- You: "New feature"
- Me: "What component/area does this affect?"
- You: "Authentication"
- Me: "Here's your commit message: `feat(auth): add login page`"
```

**Why This Works**:
- Clear, actionable instructions
- Concrete examples for different scenarios
- Covers edge cases (breaking changes, multiple issues)
- Action-oriented description triggers automatic use
- No dependencies or scripts needed

---

### Example 2: JSON Formatter

**Use Case**: Format and validate JSON data

**Structure**:
```
json-formatter/
└── SKILL.md
```

**SKILL.md**:
```markdown
---
name: json-formatter
description: Format, validate, and pretty-print JSON data. Use when working with JSON files, API responses, or config files that need formatting or validation.
---

# JSON Formatter

Format and validate JSON data with helpful error messages.

## When to Use

- Format messy JSON
- Validate JSON syntax
- Compare JSON structures
- Convert between compact and pretty formats
- Debug JSON parsing errors

## Features

### 1. Pretty Printing

Transform compact JSON into readable format:

**Input**:
```json
{"name":"John","age":30,"city":"NYC"}
```

**Output**:
```json
{
  "name": "John",
  "age": 30,
  "city": "NYC"
}
```

### 2. Validation

Check for common JSON errors:
- Missing commas
- Trailing commas
- Unquoted keys
- Single quotes instead of double quotes
- Unescaped characters

### 3. Minification

Reduce JSON size for transmission:

**Input**:
```json
{
  "users": [
    {
      "name": "John",
      "age": 30
    }
  ]
}
```

**Output**:
```json
{"users":[{"name":"John","age":30}]}
```

### 4. Structure Analysis

- Count objects, arrays, and primitives
- Find deeply nested paths
- Identify large values
- Detect duplicate keys

## Usage

Just paste or upload your JSON and tell me what you need:

- "Format this JSON"
- "Validate this JSON"
- "Minify this JSON"
- "What's wrong with this JSON?"
- "Compare these two JSON files"

## Common Fixes

### Trailing Comma
❌ `{"name": "John", "age": 30,}`
✅ `{"name": "John", "age": 30}`

### Single Quotes
❌ `{'name': 'John'}`
✅ `{"name": "John"}`

### Unquoted Keys
❌ `{name: "John"}`
✅ `{"name": "John"}`

### Missing Comma
❌ `{"name": "John" "age": 30}`
✅ `{"name": "John", "age": 30}`

## Tips

- Use JSON for configs (not YAML) when strict validation needed
- Keep nesting under 5 levels for readability
- Consider splitting large JSON files
- Use consistent key naming (camelCase or snake_case)
```

---

## Skills with Scripts

### Example 3: API Response Validator

**Use Case**: Validate API responses against schemas

**Structure**:
```
api-validator/
├── SKILL.md
├── scripts/
│   ├── __init__.py
│   ├── validator.py
│   └── schema_builder.py
└── README.md
```

**SKILL.md**:
```markdown
---
name: api-validator
description: Validate API responses against JSON schemas with detailed error reports. Use PROACTIVELY when testing or debugging REST APIs.
tools: Bash, Read, Write
model: sonnet
---

# API Response Validator

Comprehensive validation for API responses.

## Features

- Validate against JSON Schema
- Auto-generate schemas from examples
- Test status codes, headers, body
- Performance metrics
- Security checks

## Usage

### Validate a Response

```
Validate this API response:
{
  "status": 200,
  "body": {"user_id": 123, "name": "John"}
}

Against schema:
{
  "type": "object",
  "required": ["user_id", "name"],
  "properties": {
    "user_id": {"type": "integer"},
    "name": {"type": "string"}
  }
}
```

### Generate Schema

```
Generate a schema for this response:
{"user_id": 123, "name": "John", "email": "john@example.com"}
```

### Batch Validation

```
Validate all responses in ./tests/responses/
```

## Scripts

This skill includes Python scripts for deterministic validation:

- `validator.py`: Core validation logic
- `schema_builder.py`: Generate schemas from examples

Run manually:
```bash
python scripts/validator.py response.json schema.json
```

See README.md for detailed script documentation.
```

**scripts/validator.py**:
```python
#!/usr/bin/env python3
"""Validate JSON against JSON Schema."""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple


def validate_json(data: Dict[str, Any], schema: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate JSON data against schema.

    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []

    # Check required fields
    if "required" in schema:
        for field in schema["required"]:
            if field not in data:
                errors.append(f"Missing required field: {field}")

    # Check field types
    if "properties" in schema:
        for field, field_schema in schema["properties"].items():
            if field in data:
                expected_type = field_schema.get("type")
                actual_value = data[field]

                if not check_type(actual_value, expected_type):
                    errors.append(
                        f"Field '{field}' has wrong type. "
                        f"Expected {expected_type}, got {type(actual_value).__name__}"
                    )

    return len(errors) == 0, errors


def check_type(value: Any, expected_type: str) -> bool:
    """Check if value matches expected JSON type."""
    type_map = {
        "string": str,
        "integer": int,
        "number": (int, float),
        "boolean": bool,
        "array": list,
        "object": dict,
        "null": type(None),
    }

    expected_python_type = type_map.get(expected_type)
    if expected_python_type is None:
        return True  # Unknown type, skip check

    return isinstance(value, expected_python_type)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate JSON against schema")
    parser.add_argument("data_file", type=Path, help="JSON data file")
    parser.add_argument("schema_file", type=Path, help="JSON schema file")

    args = parser.parse_args()

    # Load files
    try:
        data = json.loads(args.data_file.read_text())
        schema = json.loads(args.schema_file.read_text())
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON - {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Validate
    is_valid, errors = validate_json(data, schema)

    if is_valid:
        print("✅ Validation passed")
        return 0
    else:
        print("❌ Validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

**Why This Works**:
- Combines AI guidance with deterministic validation
- Scripts provide precise, repeatable checks
- Clear examples show usage patterns
- Works across platforms (with network in Code, offline in API)

---

## Complex Skills

### Example 4: Database Migration Helper

**Use Case**: Validate and generate database migrations

**Structure**:
```
db-migrator/
├── SKILL.md
├── scripts/
│   ├── __init__.py
│   ├── validate_migration.py
│   ├── generate_rollback.py
│   └── analyze_schema.py
└── references/
    ├── sql-best-practices.md
    ├── migration-patterns.md
    └── examples.md
```

**SKILL.md**:
```markdown
---
name: db-migrator
description: Create and validate database migrations with automatic rollback generation. Use PROACTIVELY when designing schema changes or creating migration files.
tools: Bash, Read, Write, Edit
model: sonnet
---

# Database Migration Helper

Comprehensive toolkit for database migrations.

## When to Use

- Creating new migrations
- Validating migration safety
- Generating rollback scripts
- Reviewing schema changes
- Planning database refactoring

## Features

### 1. Migration Validation

Checks for:
- Breaking changes (column removal, type changes)
- Performance issues (missing indexes, table locks)
- Data integrity risks (missing constraints)
- Naming conventions
- SQL syntax

### 2. Rollback Generation

Automatically generates rollback scripts for:
- Table creation → DROP TABLE
- Column addition → ALTER TABLE DROP COLUMN
- Index creation → DROP INDEX
- Data migrations → Inverse operations

### 3. Schema Analysis

- Compare schemas across environments
- Identify drift
- Suggest optimizations
- Generate documentation

## Quick Start

### Create a Migration

```
Create a migration to add an email column to the users table
```

I'll generate:
- Forward migration (add column)
- Rollback migration (remove column)
- Validation checks
- Index recommendations

### Validate Existing Migration

```
Validate this migration:
[paste your SQL]
```

I'll check for safety issues and suggest improvements.

### Generate Rollback

```
Generate rollback for:
[paste forward migration]
```

## Best Practices

For detailed migration patterns and SQL best practices:
```
Read .claude-plugin/references/sql-best-practices.md
```

## Scripts

### validate_migration.py

Validates SQL migrations for safety:

```bash
python scripts/validate_migration.py migration.sql
```

Checks:
- Syntax errors
- Breaking changes
- Performance issues
- Security risks

### generate_rollback.py

Creates rollback scripts:

```bash
python scripts/generate_rollback.py migration.sql > rollback.sql
```

### analyze_schema.py

Compares schema files:

```bash
python scripts/analyze_schema.py schema1.sql schema2.sql
```

## References

- **sql-best-practices.md**: SQL coding standards and patterns
- **migration-patterns.md**: Common migration scenarios with examples
- **examples.md**: Real-world migration examples

Load as needed for detailed guidance.
```

**Why This Works**:
- Combines AI reasoning with automated checks
- References provide deep expertise without token cost
- Scripts handle deterministic tasks
- Clear separation of concerns
- Works great in Claude Code with full tool access

---

## Summary

### Choosing Skill Complexity

**Simple** (SKILL.md only):
- Documentation formatting
- Writing assistance
- Simple validation
- Template generation

**With Scripts**:
- Data validation
- File processing
- Format conversion
- Code generation

**Complex** (Full featured):
- Multi-step workflows
- Technical domains (databases, APIs)
- Integration with external tools
- Comprehensive validation

### Key Takeaways

1. **Start simple**: Most skills don't need scripts
2. **Add scripts**: When you need deterministic, repeatable operations
3. **Use references**: For detailed specs that don't need to be in context
4. **Test thoroughly**: Ensure skills work as expected
5. **Document well**: Clear examples help users and Claude

### Templates

Use these examples as templates for your own skills:
- Copy the structure
- Adapt the content
- Validate with the validator
- Test thoroughly
- Share with the community!
