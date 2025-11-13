# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **skills marketplace** for Claude agent skills - a curated collection of reusable instruction sets that enhance Claude's capabilities. The repository structure mirrors [Anthropic's official skills repository](https://github.com/anthropics/skills).

## Architecture

### Core Concepts

**Skills**: Specialized instruction sets stored in individual directories, each containing:
- `SKILL.md` (required): YAML frontmatter + Markdown instructions
- `LICENSE.txt` (required): Individual skill license
- Optional: scripts/, reference/, templates/, README.md

**Skills Specification**: Defined in `agent_skills_spec.md` (v1.0)
- Minimal structure requirement: folder + SKILL.md
- Required frontmatter: name, description
- Optional frontmatter: license, allowed-tools, metadata

**Marketplace Integration**: `.claude-plugin/marketplace.json` configures skills for Claude Code discovery and installation.

### Directory Structure

```
skills/
├── .claude-plugin/
│   └── marketplace.json       # Marketplace configuration
├── .github/
│   ├── ISSUE_TEMPLATE/        # Bug, feature, skill submission templates
│   └── pull_request_template.md
├── template-skill/            # Starter template for new skills
│   ├── SKILL.md
│   └── LICENSE.txt
├── [skill-name]/             # Individual skill directories
│   ├── SKILL.md              # Required
│   ├── LICENSE.txt           # Required
│   ├── scripts/              # Optional utilities
│   ├── reference/            # Optional documentation
│   └── templates/            # Optional template files
├── agent_skills_spec.md      # Skills specification (v1.0)
├── CONTRIBUTING.md           # Contribution guidelines
├── CODE_OF_CONDUCT.md        # Community standards
├── SECURITY.md               # Security policy
└── README.md                 # Repository documentation
```

## Common Development Tasks

### Testing Skills Locally

**With Claude Code:**
1. Ensure skill is properly structured with SKILL.md
2. Verify YAML frontmatter is valid
3. Test that skill activates appropriately

**With Claude.ai:**
1. Copy SKILL.md contents to project custom instructions
2. Test skill behavior in conversations

**Validation:**
- Verify skill name matches directory name (lowercase, hyphens)
- Ensure description clearly specifies trigger conditions
- Test all examples in documentation
- Check for security issues (no hardcoded credentials)

### Creating a New Skill

1. Copy `template-skill/` to new directory: `cp -r template-skill/ new-skill-name/`
2. Edit `SKILL.md` with proper frontmatter and instructions
3. Update `LICENSE.txt` as appropriate
4. Add supporting files in scripts/, reference/, or templates/ if needed
5. Test thoroughly before committing

### Adding Skills to Marketplace

When new skills are added, update `.claude-plugin/marketplace.json`:
- Add skill name to appropriate plugin's skills array
- Ensure skill directory exists
- Verify SKILL.md has valid frontmatter

### Code Quality Standards

**SKILL.md Files:**
- Must have valid YAML frontmatter (name, description, license)
- Name must be kebab-case (lowercase, hyphens only)
- Description should be 1-3 sentences explaining purpose AND trigger conditions
- Markdown content should be clear, structured, well-formatted

**Supporting Files:**
- Python scripts: Include requirements.txt
- Node scripts: Include package.json
- Document all dependencies
- Follow secure coding practices

**Documentation:**
- Use proper Markdown formatting
- Include code examples with syntax highlighting
- Keep line length reasonable (80-100 chars)
- Link to external resources appropriately

## Important Conventions

### Naming Conventions
- **Skill directories**: lowercase-with-hyphens (kebab-case)
- **SKILL.md name field**: Must match directory name exactly
- **Files**: Use clear, descriptive names

### Licensing
- **Repository**: MIT License
- **Individual skills**: Apache 2.0 recommended (or MIT)
- Each skill must include LICENSE.txt
- Document third-party dependencies

### Git Workflow
- Branch naming: `skill/skill-name` for new skills, `fix/issue-description` for fixes
- Commit messages: Clear, descriptive (e.g., "Add api-builder skill" or "Fix: Correct frontmatter in data-analyzer")
- PRs should follow template in `.github/pull_request_template.md`

## Skills Specification Summary

From `agent_skills_spec.md` (v1.0):

**Required:**
- Directory name: lowercase, hyphens, alphanumeric only
- SKILL.md file with YAML frontmatter
- Frontmatter fields: `name`, `description`

**Optional:**
- `license`: Brief license information
- `allowed-tools`: Pre-approved tools list
- `metadata`: Custom key-value pairs
- Supporting files in subdirectories

**Validation:**
- Name must match directory name
- YAML frontmatter must be valid
- Description should explain purpose AND trigger conditions

## Security Considerations

- Never include hardcoded API keys, tokens, or credentials
- Validate all user inputs in scripts
- Document security considerations in skill documentation
- Follow secure coding practices for all supporting scripts
- Report vulnerabilities via SECURITY.md process

## References

- Skills Specification: `agent_skills_spec.md`
- Contributing Guidelines: `CONTRIBUTING.md`
- Anthropic's Skills Repo: https://github.com/anthropics/skills
- Claude Code Docs: https://docs.claude.com/en/docs/claude-code
