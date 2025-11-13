# Skill Creator

A meta-skill for creating, validating, and packaging Claude agent skills. This skill helps you build high-quality skills that extend Claude's capabilities.

## What This Skill Does

The skill-creator automates the entire skill development lifecycle:

1. **Interactive Skill Generation** - Asks clarifying questions and generates proper structure
2. **Validation** - Validates SKILL.md format, naming conventions, and requirements
3. **Packaging** - Creates distributable skill packages
4. **Guidance** - Provides best practices and platform-specific guidance

## When to Use

Claude will proactively use this skill when you:
- Want to create a new skill
- Need to validate an existing skill
- Are packaging a skill for distribution
- Want to learn skill development best practices

## Quick Start

Simply ask Claude to create a skill:

```
"I want to create a skill for [purpose]"
```

Claude will guide you through the process using the skill-creator.

## Files in This Skill

- **SKILL.md** - Main skill definition with instructions
- **reference/** - Detailed reference documentation
  - `platform-differences.md` - Platform-specific guidance (Claude.ai, API, Code)
  - `skill-examples.md` - Complete example skills
  - `skill-specification.md` - Technical specification
- **LICENSE.txt** - Apache 2.0 license

## Validation and Packaging Scripts

The skill creator references validation and packaging scripts that are available at the repository root level in `scripts/`:

- **validate_skill.py** - Validates skills against specifications
- **package_skill.py** - Creates distributable skill packages
- **skill_utils.py** - Shared utilities

See the main repository README for how to use these scripts.

## Platform Support

This skill works across:
- **Claude.ai** - User-specific skills
- **Claude API** - Workspace-wide skills
- **Claude Code** - Project/user-level skills with full capabilities

## License

Licensed under Apache 2.0. See LICENSE.txt for complete terms.

## Original Source

This skill was originally developed at https://github.com/jgardner04/claude-skills-skill and has been integrated into this marketplace.
