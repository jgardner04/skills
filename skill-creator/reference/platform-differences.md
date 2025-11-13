# Platform-Specific Guidance for Claude Skills

Understanding the differences between Claude surfaces to create skills that work everywhere.

## Overview

Claude skills can run on three different surfaces:
1. **Claude.ai** - Web interface and mobile apps
2. **Claude API** - Programmatic access for developers
3. **Claude Code** - CLI tool for development workflows

Each platform has different capabilities, constraints, and runtime environments. This guide helps you create skills that work effectively across all platforms or target specific ones.

## Quick Comparison

| Feature | Claude.ai | Claude API | Claude Code |
|---------|-----------|------------|-------------|
| **Skill Scope** | User-specific | Workspace-wide | Project or user |
| **Network Access** | Variable (admin settings) | No (by default) | Yes (full access) |
| **File System** | Limited (uploads only) | Limited | Full access |
| **Package Installation** | No | No | Yes (with permissions) |
| **Bash Commands** | No | Limited (sandboxed) | Yes (full shell) |
| **Best For** | Personal productivity | Programmatic workflows | Development tasks |

## Claude.ai

### Overview
Web-based interface with mobile app support. Skills help individual users with their work.

### Characteristics

**Skill Scope**: User-specific only
- Each user uploads their own skills
- Skills are not shared across workspace
- No way to distribute org-wide skills
- Good for personal productivity

**Network Access**: Variable
- Depends on user settings
- Depends on admin/organization policies
- Can be restricted by IT
- Skills should handle network unavailability gracefully

**File System Access**: Upload-based
- Users upload files through the UI
- Skills can read uploaded files
- Skills can generate downloadable files
- No direct file system access

**Tool Availability**:
- ✅ Read (uploaded files)
- ✅ Write (generate downloads)
- ⚠️  WebFetch (if network allowed)
- ⚠️  WebSearch (if network allowed)
- ❌ Bash (no shell access)
- ❌ Git operations

### Best Practices for Claude.ai

#### Make Network Access Optional
```markdown
## Using the API (Optional)

If you have network access enabled, this skill can fetch live data.
Otherwise, you can upload data files directly.
```

#### Provide Upload Instructions
```markdown
## Setup

1. Download the template from [link]
2. Fill in your data
3. Upload the file to Claude
4. Use this skill to process it
```

#### Handle Missing Dependencies
```markdown
## Note

This skill works best with network access. If network is disabled,
you can still use the basic features by providing data manually.
```

#### Use Read/Write Effectively
- Generate files users can download
- Process uploaded CSV, JSON, Markdown
- Create reports, summaries, visualizations (as text/markdown)

### Example: Claude.ai-Friendly Skill

```yaml
---
name: meeting-notes-formatter
description: Format raw meeting notes into structured summaries with action items. Works with uploaded text files or pasted content.
tools: Read, Write
---

# Meeting Notes Formatter

Formats meeting notes into professional summaries.

## How to Use

**Option 1: Upload a file**
1. Save your meeting notes as a .txt or .md file
2. Upload to Claude
3. Ask me to format it: "Format the meeting notes"

**Option 2: Paste directly**
1. Copy your meeting notes
2. Paste into the chat
3. Ask me to format it

## What You'll Get

- Executive summary
- Key discussion points
- Action items with owners
- Decisions made
- Follow-up topics

No network access required!
```

## Claude API

### Overview
Programmatic access for developers to integrate Claude into applications and workflows.

### Characteristics

**Skill Scope**: Workspace-wide
- Skills are available to all workspace members
- Configured at the organization level
- Shared across all API calls in the workspace
- Centralized management

**Network Access**: None by default
- No outbound network requests
- No API calls to external services
- Skills must work offline
- Security-focused design

**Dependency Management**: Pre-configured only
- No dynamic package installation
- Dependencies must be pre-installed in the runtime
- Limited to standard library + pre-approved packages
- Skills cannot require new dependencies

**Execution Environment**: Sandboxed
- Controlled execution environment
- Limited file system access
- Security restrictions
- Predictable, reproducible behavior

**Tool Availability**:
- ✅ Read (from provided context)
- ✅ Write (to return data)
- ⚠️  Bash (sandboxed, limited commands)
- ❌ WebFetch (no network)
- ❌ WebSearch (no network)
- ❌ Package installation

### Best Practices for Claude API

#### Design for Offline Operation
```python
# ❌ Bad: Requires network
def fetch_user_data(user_id):
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()

# ✅ Good: Works with provided data
def process_user_data(user_data: dict) -> dict:
    """Process user data provided by the caller."""
    return {
        "summary": generate_summary(user_data),
        "insights": extract_insights(user_data),
    }
```

#### Use Only Standard Library
```python
# ✅ Good: Standard library only
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# ❌ Bad: External dependency
import pandas as pd  # Not available unless pre-installed
```

#### Document Data Requirements
```markdown
## API Integration

This skill requires the following data to be provided:

### Input Format
```json
{
  "users": [...],
  "events": [...],
  "config": {...}
}
```

### Output Format
```json
{
  "report": "...",
  "metrics": {...},
  "recommendations": [...]
}
```
```

#### Provide Clear Error Messages
```python
def validate_input(data: dict) -> tuple[bool, str]:
    """Validate input data structure."""
    if "users" not in data:
        return False, "Missing required field: 'users'"
    if not isinstance(data["users"], list):
        return False, "Field 'users' must be a list"
    return True, ""
```

### Example: API-Optimized Skill

```yaml
---
name: data-transformer
description: Transform and validate JSON data structures. Requires data to be provided via API call. Works entirely offline with no external dependencies.
tools: Read, Write
model: haiku
---

# Data Transformer

Transforms JSON data according to specified rules.

## API Usage

```python
import anthropic

client = anthropic.Anthropic()

# Provide data in the API call
message = client.messages.create(
    model="claude-3-sonnet-20240229",
    messages=[{
        "role": "user",
        "content": f"Transform this data: {json.dumps(data)}"
    }]
)
```

## Input Requirements

The skill expects JSON data in this format:
```json
{
  "data": [...],
  "rules": {...}
}
```

## Output

Returns transformed data:
```json
{
  "transformed": [...],
  "errors": [],
  "stats": {...}
}
```

## No Dependencies

Uses only Python standard library - no external packages required.
```

## Claude Code

### Overview
CLI tool for development workflows with full system access.

### Characteristics

**Skill Scope**: Flexible
- Project-level: `.claude/skills/` (shared with team via git)
- User-level: `~/.claude/agents/` (personal)
- Plugin-level: `.claude-plugin/` (distributable)

**Network Access**: Full
- Unrestricted outbound requests
- Can call APIs
- Can fetch web pages
- Can download resources

**File System Access**: Full
- Read any accessible file
- Write to any writable location
- Execute commands
- Full git integration

**Package Installation**: Available
- Can install Python packages (pip)
- Can install npm packages
- Can use system package managers
- Can compile code

**Tool Availability**:
- ✅ All tools available
- ✅ Bash (full shell access)
- ✅ WebFetch
- ✅ WebSearch
- ✅ Git operations
- ✅ Read/Write/Edit
- ✅ Task (subagents)

### Best Practices for Claude Code

#### Leverage Full Capabilities
```yaml
---
name: api-tester
description: Test REST APIs with automatic request generation and validation. Use when developing or debugging API endpoints.
tools: Bash, Read, Write, WebFetch
---

# API Tester

Tests REST APIs with comprehensive validation.

## Features

- Automatic request generation
- Response validation
- Performance metrics
- Error handling tests
- OpenAPI spec generation

## Requirements

```bash
pip install requests pyyaml jsonschema
```

## Usage

Just tell me the API endpoint to test!
```

#### Use Project Configuration
```markdown
## Setup

Add to `.claude/settings.json`:

```json
{
  "env": {
    "API_KEY": "${YOUR_API_KEY}",
    "API_URL": "https://api.example.com"
  }
}
```

The skill will read these values automatically.
```

#### Integrate with Development Tools
```bash
# Run linters
black your_script.py
pylint your_script.py

# Run tests
pytest tests/

# Build project
npm run build
```

#### Create Complex Workflows
```markdown
## Workflow

1. Fetch latest data from API
2. Validate against schema
3. Transform and process
4. Update local files
5. Generate report
6. Commit changes to git
```

### Example: Claude Code-Optimized Skill

```yaml
---
name: github-issue-helper
description: Manage GitHub issues - create, update, search, and analyze issues using gh CLI. Use when working with GitHub repositories in development.
tools: Bash, Read, Write, Edit, Grep
---

# GitHub Issue Helper

Comprehensive GitHub issue management using gh CLI.

## Requirements

```bash
# Install GitHub CLI
brew install gh  # macOS
# OR
apt install gh   # Linux

# Authenticate
gh auth login
```

## Features

- **Create issues**: From templates or scratch
- **Search issues**: By label, state, author
- **Bulk operations**: Close, label, assign multiple issues
- **Analysis**: Generate reports, find patterns
- **Integration**: Link to commits, PRs, projects

## Commands

- "Create an issue for the bug in API endpoint"
- "Find all P0 issues assigned to me"
- "Close all issues labeled 'wontfix'"
- "Generate a weekly issue summary"

## Setup

No additional setup required if gh CLI is authenticated.
```

## Cross-Platform Skills

### Design Principles

To create skills that work across all platforms:

#### 1. Progressive Enhancement

Start with core functionality that works everywhere, add platform-specific features as available.

```markdown
## Core Features (All Platforms)
- Process uploaded/provided data
- Generate formatted output
- Validate inputs

## Enhanced Features (Claude Code Only)
- Fetch live data from APIs
- Update local files automatically
- Integrate with git workflow
```

#### 2. Graceful Degradation

Handle missing capabilities elegantly:

```markdown
## Setup

### Claude.ai / API
Upload your data file (CSV, JSON, or TXT)

### Claude Code
I can fetch data directly from your database or API.
Tell me the connection details.
```

#### 3. Platform Detection

Guide users based on their platform:

```markdown
## Platform Notes

**Claude.ai**: Upload files via the interface
**Claude API**: Provide data in the API request body
**Claude Code**: I can read files directly from your project
```

#### 4. Minimal Dependencies

Use standard library when possible:

```python
# ✅ Works everywhere
import json
from pathlib import Path

# ⚠️  Works in Claude Code only
import requests
import pandas
```

### Example: Universal Skill

```yaml
---
name: json-validator
description: Validate and format JSON data against schemas. Works with uploaded files, pasted data, or local files depending on platform.
tools: Read, Write
---

# JSON Validator

Validates JSON against schemas with detailed error reports.

## How to Use

**Claude.ai**:
1. Upload your JSON file
2. Upload your schema file (optional)
3. Ask: "Validate the JSON"

**Claude API**:
```python
message = client.messages.create(
    messages=[{
        "role": "user",
        "content": f"Validate this JSON:\n{json_data}\n\nSchema:\n{schema}"
    }]
)
```

**Claude Code**:
```
Validate JSON files in ./data/
```

## Features

- ✅ Schema validation (all platforms)
- ✅ Format checking (all platforms)
- ✅ Error highlighting (all platforms)
- ⚠️  Auto-fix suggestions (Claude Code only)
- ⚠️  Batch processing (Claude Code only)

No external dependencies required!
```

## Testing Across Platforms

### Test Checklist

- [ ] Test on Claude.ai (web interface)
- [ ] Test via Claude API (programmatic access)
- [ ] Test in Claude Code (CLI)
- [ ] Test with network disabled (API mode)
- [ ] Test with file uploads (Claude.ai mode)
- [ ] Test with local files (Claude Code mode)
- [ ] Verify error messages are clear on all platforms
- [ ] Check that platform-specific features degrade gracefully

### Platform-Specific Test Cases

**Claude.ai**:
- Upload various file formats
- Test with network restrictions
- Verify download generation works
- Test on mobile if applicable

**Claude API**:
- Test with no network access
- Verify offline operation
- Test with standard library only
- Check API response format

**Claude Code**:
- Test with project files
- Test bash commands
- Test package installation instructions
- Verify git integration

## Summary

### Choose Your Target

**Claude.ai**: Best for personal productivity skills that process documents
**Claude API**: Best for deterministic, offline data processing
**Claude Code**: Best for development workflows with full system access

### Design Patterns

**Single Platform**: Optimize for that platform's strengths
**Multi-Platform**: Use progressive enhancement and graceful degradation
**Universal**: Stick to core capabilities, document platform differences

### Key Takeaways

1. **Know your constraints**: Each platform has different capabilities
2. **Design accordingly**: Match skill design to platform capabilities
3. **Document clearly**: Tell users what works where
4. **Test thoroughly**: Verify on all target platforms
5. **Handle gracefully**: Degrade features when capabilities are missing

## Resources

- **Claude.ai**: https://claude.ai/skills
- **Claude API**: https://docs.anthropic.com/claude/docs/
- **Claude Code**: https://docs.claude.com/en/docs/claude-code/overview
