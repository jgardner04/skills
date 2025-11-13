# Skills Marketplace

A curated collection of Claude agent skills for enhancing AI capabilities across various domains. This repository provides reusable, well-documented skills that can be integrated into Claude Code, Claude.ai, or Claude API workflows.

## What are Skills?

Skills are specialized instruction sets that enhance Claude's capabilities for specific tasks. Each skill is defined in a simple `SKILL.md` file containing:
- YAML frontmatter with metadata (name, description, license)
- Detailed instructions and examples
- Optional supporting files (scripts, templates, reference docs)

When you add a skill, Claude automatically knows when and how to use it based on the skill's description.

## Getting Started

### Using Skills with Claude Code

1. Install Claude Code from [claude.ai/code](https://claude.ai/code)
2. Skills from this repository can be installed via the marketplace (once published)
3. Or manually: Clone this repo and reference skills in your `.claude-plugin/` configuration

### Using Skills with Claude.ai

For Claude Pro and Team plan subscribers:
1. Navigate to your project settings
2. Add custom instructions from any skill's SKILL.md file
3. Claude will now have access to that skill's capabilities

### Using Skills with Claude API

Use the Skills API to programmatically attach skills to your conversations:
```python
import anthropic

client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Your task here"}],
    skills=["skill-name"]
)
```

## Repository Structure

```
skills/
├── .claude-plugin/         # Marketplace configuration
├── .github/                # Issue templates and workflows
├── template-skill/         # Starter template for new skills
├── skill-name/            # Individual skill directories
│   ├── SKILL.md          # Required: Skill definition
│   ├── LICENSE.txt       # Individual skill license
│   ├── scripts/          # Optional: Utility scripts
│   ├── reference/        # Optional: Reference documentation
│   └── templates/        # Optional: Template files
├── agent_skills_spec.md  # Skills specification
└── README.md             # This file
```

## Creating a Skill

Want to contribute a new skill? Great! Here's how:

1. **Start with the template**: Copy the `template-skill/` folder and rename it (use lowercase with hyphens)
2. **Edit SKILL.md**: Add your skill's metadata and instructions
3. **Add supporting files**: Include any scripts, templates, or reference docs
4. **Test thoroughly**: Ensure your skill works as expected
5. **Submit a PR**: See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines

See [agent_skills_spec.md](agent_skills_spec.md) for the complete specification.

## Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting a pull request.

Key points:
- Follow the skills specification in [agent_skills_spec.md](agent_skills_spec.md)
- Include comprehensive documentation
- Test your skill thoroughly
- Use appropriate licensing (Apache 2.0 recommended for example skills)

## License

This repository is licensed under the MIT License. See [LICENSE](LICENSE) for details.

Individual skills may have their own licenses. Check each skill's `LICENSE.txt` file.

## Security

Please report security vulnerabilities privately. See [SECURITY.md](SECURITY.md) for details.

## Support

- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/jgardner04/skills/issues)
- **Discussions**: Ask questions and share ideas in [GitHub Discussions](https://github.com/jgardner04/skills/discussions)
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)

## Acknowledgments

This repository structure and skills specification are inspired by [Anthropic's official skills repository](https://github.com/anthropics/skills).
