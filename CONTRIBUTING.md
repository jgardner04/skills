# Contributing to Skills Marketplace

Thank you for your interest in contributing to this skills marketplace! This guide will help you create high-quality skills that benefit the entire community.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Skill Guidelines](#skill-guidelines)
- [Submission Process](#submission-process)
- [Review Process](#review-process)
- [Licensing](#licensing)

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## Getting Started

### Prerequisites

- Familiarity with Claude and AI agent concepts
- Understanding of the skills specification ([agent_skills_spec.md](agent_skills_spec.md))
- Access to Claude Code, Claude.ai, or Claude API for testing

### Setting Up Your Environment

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/skills.git`
3. Create a new branch: `git checkout -b skill/your-skill-name`
4. Copy the template: `cp -r template-skill/ your-skill-name/`

## How to Contribute

### Types of Contributions

We welcome several types of contributions:

1. **New Skills**: Add a completely new skill to the marketplace
2. **Skill Improvements**: Enhance existing skills with better instructions or examples
3. **Bug Fixes**: Fix issues in existing skills
4. **Documentation**: Improve documentation, examples, or guides
5. **Templates**: Contribute useful templates or supporting files

### Creating a New Skill

#### Step 1: Choose a Unique Name

- Use lowercase letters, numbers, and hyphens only (kebab-case)
- Make it descriptive and concise
- Check existing skills to avoid duplicates
- Examples: `api-builder`, `data-analyzer`, `code-reviewer`

#### Step 2: Create the Skill Structure

```
your-skill-name/
├── SKILL.md              # Required: Main skill definition
├── LICENSE.txt           # Required: Skill license
├── README.md             # Optional: Additional documentation
├── scripts/              # Optional: Utility scripts
├── reference/            # Optional: Reference materials
└── templates/            # Optional: Template files
```

#### Step 3: Write the SKILL.md File

Your `SKILL.md` must include:

**Required YAML Frontmatter:**
```yaml
---
name: your-skill-name
description: A clear, concise description of what the skill does and when Claude should use it. Be specific about use cases and trigger conditions.
license: Apache 2.0
---
```

**Markdown Content:**
- Clear introduction explaining the skill's purpose
- Detailed instructions for Claude to follow
- Examples demonstrating usage
- Any constraints or limitations
- References to supporting files (if any)

**Best Practices:**
- Be explicit about when the skill should be activated
- Include concrete examples
- Document any dependencies or prerequisites
- Explain expected inputs and outputs
- Use clear, structured Markdown formatting

#### Step 4: Add Supporting Files

**Scripts** (`scripts/` directory):
- Include utility scripts that support the skill
- Add requirements.txt for Python dependencies
- Add package.json for Node.js dependencies
- Document how to run each script

**Reference Materials** (`reference/` directory):
- Include API documentation, best practices, or guides
- Use Markdown format for consistency
- Link to external resources when appropriate

**Templates** (`templates/` directory):
- Provide starter templates or boilerplate code
- Include comments explaining each section
- Keep templates minimal but functional

#### Step 5: Choose a License

**Recommended: Apache 2.0**
- Permissive open-source license
- Allows commercial use
- Includes patent protection
- Compatible with this repository's MIT license

**Alternative: MIT**
- Simple, permissive license
- Minimal restrictions

**Proprietary Licenses**
- Only if absolutely necessary
- Must be clearly documented
- May limit adoption

Copy the appropriate license template to `LICENSE.txt` in your skill directory.

#### Step 6: Test Your Skill

Before submitting:

1. **Test with Claude Code**: Add the skill locally and verify it works
2. **Test with Claude.ai**: Copy instructions to project settings and test
3. **Verify Activation**: Ensure Claude activates the skill at appropriate times
4. **Check Examples**: Verify all examples in your documentation work
5. **Review Dependencies**: Test any scripts or templates included

**Testing Checklist:**
- [ ] Skill activates when expected
- [ ] Instructions are clear and unambiguous
- [ ] Examples work as documented
- [ ] No security vulnerabilities
- [ ] Scripts run without errors
- [ ] Dependencies are documented
- [ ] License is properly specified

## Skill Guidelines

### Quality Standards

**Clarity**
- Write clear, unambiguous instructions
- Use simple language
- Avoid jargon without explanation
- Structure content logically

**Completeness**
- Include all necessary information
- Document edge cases
- Provide examples for common scenarios
- Reference supporting files

**Specificity**
- Be explicit about trigger conditions
- Define expected inputs and outputs
- Specify constraints and limitations
- Include concrete examples

**Safety**
- Avoid instructions that could cause harm
- Don't include hardcoded credentials
- Document security considerations
- Follow secure coding practices

### Description Guidelines

The `description` field in your SKILL.md frontmatter is crucial. It should:

1. **Explain what the skill does** (1-2 sentences)
2. **Specify when Claude should use it** (trigger conditions)
3. **List key capabilities** (enumerated if multiple)

**Good Example:**
```yaml
description: Comprehensive API endpoint builder for RESTful services with automatic documentation generation. Use when creating new APIs, designing endpoints, or generating OpenAPI specifications. Supports (1) Endpoint design, (2) Request/response schemas, (3) Authentication patterns, (4) Documentation generation.
```

**Bad Example:**
```yaml
description: Helps with APIs
```

### File Organization

- Keep related files together in subdirectories
- Use descriptive filenames
- Include README files in subdirectories when helpful
- Maintain consistent naming conventions

### Documentation Standards

- Use proper Markdown formatting
- Include code blocks with syntax highlighting
- Add links to external resources
- Keep line length reasonable (80-100 characters)
- Use tables for structured data
- Include diagrams or images when helpful

## Submission Process

### Before Submitting

1. Review the [skills specification](agent_skills_spec.md)
2. Complete the testing checklist
3. Ensure all files are properly formatted
4. Write a clear commit message
5. Update relevant documentation

### Submitting a Pull Request

1. **Commit Your Changes**
   ```bash
   git add your-skill-name/
   git commit -m "Add [skill-name]: Brief description"
   ```

2. **Push to Your Fork**
   ```bash
   git push origin skill/your-skill-name
   ```

3. **Create Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill out the PR template completely
   - Submit for review

### Pull Request Template

Your PR should include:

- **Skill Name**: Clear, descriptive name
- **Description**: What the skill does
- **Type**: New skill, enhancement, bug fix, etc.
- **Testing**: How you tested it
- **Checklist**: Completed PR checklist items
- **Additional Notes**: Any relevant context

## Review Process

### What Reviewers Look For

1. **Adherence to Specification**: Follows agent_skills_spec.md
2. **Quality**: Clear, complete, and well-documented
3. **Testing**: Properly tested and verified
4. **Licensing**: Appropriate license included
5. **Security**: No vulnerabilities or sensitive data
6. **Originality**: Not duplicating existing skills

### Review Timeline

- Initial review: Within 5-7 business days
- Feedback provided via PR comments
- Revisions requested as needed
- Approval and merge once requirements met

### After Approval

Once your PR is approved:
1. It will be merged into the main branch
2. Your skill becomes part of the marketplace
3. It will be included in the next marketplace update
4. You'll be credited as a contributor

## Licensing

### Repository License

This repository is licensed under the MIT License. By contributing, you agree that your contributions will be licensed under the same license.

### Individual Skill Licenses

Each skill can have its own license:
- Include a `LICENSE.txt` file in your skill directory
- Recommended: Apache 2.0 or MIT for open-source skills
- Clearly state the license in your SKILL.md frontmatter
- Ensure compatibility with the repository's MIT license

### Third-Party Dependencies

If your skill includes third-party code or dependencies:
- Document all dependencies
- Include proper attribution
- Ensure licenses are compatible
- Add to THIRD_PARTY_NOTICES.md if necessary

## Getting Help

Need assistance?

- **Questions**: Open a [GitHub Discussion](https://github.com/jgardner04/skills/discussions)
- **Issues**: Report bugs via [GitHub Issues](https://github.com/jgardner04/skills/issues)
- **Skill Ideas**: Use the "Skill Submission" issue template
- **General Help**: Tag your discussion with "help wanted"

## Recognition

Contributors are recognized in several ways:
- Listed in repository contributors
- Credited in skill documentation
- Mentioned in release notes
- Featured in community showcases

Thank you for contributing to the Skills Marketplace!
