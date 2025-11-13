#!/usr/bin/env python3
"""
Shared utilities for Claude skill creation, validation, and packaging.

This module provides common functionality used across the skill-creator tools.
"""

import re
import sys
from pathlib import Path
from typing import Dict, Tuple, Any, Optional

try:
    import yaml
except ImportError:
    print(
        "Error: PyYAML is required. Install with: pip install pyyaml",
        file=sys.stderr,
    )
    sys.exit(1)


class SkillError(Exception):
    """Base exception for skill-related errors."""

    pass


class SkillValidationError(SkillError):
    """Raised when skill validation fails."""

    pass


class SkillPackagingError(SkillError):
    """Raised when skill packaging fails."""

    pass


def safe_path(base: Path, user_input: str) -> Path:
    """Safely resolve a path relative to base, preventing traversal attacks.

    Args:
        base: The base directory path
        user_input: User-provided path component

    Returns:
        Resolved path that is guaranteed to be within base

    Raises:
        ValueError: If path traversal is detected

    Examples:
        >>> base = Path("/skills")
        >>> safe_path(base, "my-skill")
        PosixPath('/skills/my-skill')
        >>> safe_path(base, "../etc/passwd")
        Traceback (most recent call last):
        ...
        ValueError: Path traversal detected: ../etc/passwd
    """
    resolved = (base / user_input).resolve()
    try:
        resolved.relative_to(base.resolve())
    except ValueError:
        raise ValueError(f"Path traversal detected: {user_input}")
    return resolved


def parse_skill_file(content: str) -> Tuple[Dict[str, Any], str]:
    """Parse SKILL.md into frontmatter and body content.

    Args:
        content: Full content of SKILL.md file

    Returns:
        Tuple of (frontmatter_dict, body_content)

    Raises:
        SkillValidationError: If frontmatter is missing or invalid

    Examples:
        >>> content = "---\\nname: test\\n---\\nBody text"
        >>> fm, body = parse_skill_file(content)
        >>> fm['name']
        'test'
        >>> body
        'Body text'
    """
    if not content.strip():
        raise SkillValidationError("SKILL.md file is empty")

    if not content.startswith("---"):
        raise SkillValidationError(
            "SKILL.md must start with YAML frontmatter (---)"
        )

    # Match frontmatter between --- delimiters
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.DOTALL)
    if not match:
        raise SkillValidationError(
            "Invalid frontmatter format. Must be:\n"
            "---\n"
            "name: skill-name\n"
            "description: ...\n"
            "---\n"
            "Body content..."
        )

    frontmatter_str, body = match.groups()

    try:
        frontmatter = yaml.safe_load(frontmatter_str)
    except yaml.YAMLError as e:
        raise SkillValidationError(f"Invalid YAML in frontmatter: {e}")

    if not isinstance(frontmatter, dict):
        raise SkillValidationError(
            "Frontmatter must be a YAML dictionary/object"
        )

    return frontmatter, body.strip()


def validate_skill_name(name: str) -> Tuple[bool, str]:
    """Validate a skill name against Claude's naming requirements.

    Args:
        name: The skill name to validate

    Returns:
        Tuple of (is_valid, error_message). If valid, error_message is empty.

    Examples:
        >>> validate_skill_name("my-skill")
        (True, '')
        >>> validate_skill_name("My Skill")
        (False, 'Skill name must be lowercase with hyphens only...')
        >>> validate_skill_name("skill-with-anthropic")
        (False, 'Skill name cannot contain "anthropic" or "claude"')
    """
    if not name:
        return False, "Skill name is required"

    if len(name) > 64:
        return False, f"Skill name too long ({len(name)} chars, max 64)"

    # Check for lowercase, numbers, and hyphens only
    if not re.match(r"^[a-z0-9-]+$", name):
        return (
            False,
            "Skill name must be lowercase with hyphens only (a-z, 0-9, -)",
        )

    # Check for restricted terms
    if "anthropic" in name or "claude" in name:
        return False, 'Skill name cannot contain "anthropic" or "claude"'

    # Check for XML tags
    if "<" in name or ">" in name:
        return False, "Skill name cannot contain XML tags"

    return True, ""


def validate_skill_description(description: str) -> Tuple[bool, str]:
    """Validate a skill description against Claude's requirements.

    Args:
        description: The skill description to validate

    Returns:
        Tuple of (is_valid, error_message). If valid, error_message is empty.

    Examples:
        >>> validate_skill_description("A helpful skill")
        (True, '')
        >>> validate_skill_description("")
        (False, 'Description is required')
        >>> validate_skill_description("A" * 1025)
        (False, 'Description too long (1025 chars, max 1024)')
    """
    if not description:
        return False, "Description is required"

    if not description.strip():
        return False, "Description cannot be only whitespace"

    if len(description) > 1024:
        return (
            False,
            f"Description too long ({len(description)} chars, max 1024)",
        )

    # Check for XML tags
    if re.search(r"<[^>]+>", description):
        return False, "Description cannot contain XML tags"

    return True, ""


def find_skill_file(path: Path) -> Optional[Path]:
    """Find SKILL.md file in the given path.

    Args:
        path: Directory path or SKILL.md file path

    Returns:
        Path to SKILL.md if found, None otherwise

    Examples:
        >>> from pathlib import Path
        >>> find_skill_file(Path("/path/to/skill/SKILL.md"))
        PosixPath('/path/to/skill/SKILL.md')
        >>> find_skill_file(Path("/path/to/skill/"))
        PosixPath('/path/to/skill/SKILL.md')
    """
    if not path.exists():
        return None

    if path.is_file() and path.name == "SKILL.md":
        return path

    if path.is_dir():
        skill_file = path / "SKILL.md"
        if skill_file.exists():
            return skill_file

    return None


class ValidationResult:
    """Result of a validation check with errors and warnings."""

    def __init__(self):
        """Initialize an empty validation result."""
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def add_error(self, message: str) -> None:
        """Add an error message.

        Args:
            message: Error message to add
        """
        self.errors.append(message)

    def add_warning(self, message: str) -> None:
        """Add a warning message.

        Args:
            message: Warning message to add
        """
        self.warnings.append(message)

    @property
    def is_valid(self) -> bool:
        """Check if validation passed (no errors).

        Returns:
            True if no errors, False otherwise
        """
        return len(self.errors) == 0

    @property
    def has_warnings(self) -> bool:
        """Check if there are any warnings.

        Returns:
            True if warnings exist, False otherwise
        """
        return len(self.warnings) > 0

    def __str__(self) -> str:
        """Format validation results as a readable string.

        Returns:
            Formatted string with errors and warnings
        """
        lines = []

        if self.errors:
            lines.append("❌ Errors:")
            for error in self.errors:
                lines.append(f"  - {error}")

        if self.warnings:
            if lines:
                lines.append("")
            lines.append("⚠️  Warnings:")
            for warning in self.warnings:
                lines.append(f"  - {warning}")

        if not lines:
            lines.append("✅ Validation passed")

        return "\n".join(lines)

    def __bool__(self) -> bool:
        """Allow using ValidationResult in boolean context.

        Returns:
            True if valid (no errors), False otherwise
        """
        return self.is_valid


def read_file_safe(file_path: Path, max_size: int = 10 * 1024 * 1024) -> str:
    """Safely read a file with size limit and error handling.

    Args:
        file_path: Path to file to read
        max_size: Maximum file size in bytes (default 10MB)

    Returns:
        File contents as string

    Raises:
        SkillError: If file cannot be read or is too large

    Examples:
        >>> from pathlib import Path
        >>> content = read_file_safe(Path("SKILL.md"))
        >>> isinstance(content, str)
        True
    """
    if not file_path.exists():
        raise SkillError(f"File not found: {file_path}")

    if not file_path.is_file():
        raise SkillError(f"Not a file: {file_path}")

    size = file_path.stat().st_size
    if size > max_size:
        raise SkillError(
            f"File too large: {size} bytes (max {max_size} bytes)"
        )

    try:
        return file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise SkillError(f"File is not valid UTF-8: {file_path}")
    except Exception as e:
        raise SkillError(f"Error reading file {file_path}: {e}")


def format_path(path: Path, relative_to: Optional[Path] = None) -> str:
    """Format a path for display, optionally as relative path.

    Args:
        path: Path to format
        relative_to: Base path for relative display

    Returns:
        Formatted path string

    Examples:
        >>> from pathlib import Path
        >>> format_path(Path("/home/user/skills/my-skill"))
        '/home/user/skills/my-skill'
        >>> format_path(Path("/home/user/skills/my-skill"), Path("/home/user"))
        'skills/my-skill'
    """
    if relative_to:
        try:
            return str(path.relative_to(relative_to))
        except ValueError:
            pass
    return str(path)
