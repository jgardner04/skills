#!/usr/bin/env python3
"""
Validate Claude skill files against requirements.

This script validates SKILL.md files to ensure they meet Claude's
specifications for name, description, frontmatter format, and content.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from skill_utils import (
    ValidationResult,
    find_skill_file,
    parse_skill_file,
    read_file_safe,
    validate_skill_name,
    validate_skill_description,
    format_path,
    SkillError,
)


def validate_skill(
    skill_path: Path, strict: bool = False
) -> ValidationResult:
    """Validate a skill directory or SKILL.md file.

    Args:
        skill_path: Path to skill directory or SKILL.md file
        strict: Enable strict mode (warnings become errors)

    Returns:
        ValidationResult with errors and warnings

    Examples:
        >>> from pathlib import Path
        >>> result = validate_skill(Path("path/to/skill"))
        >>> if result.is_valid:
        ...     print("Skill is valid!")
    """
    result = ValidationResult()

    # Find SKILL.md file
    skill_file = find_skill_file(skill_path)
    if not skill_file:
        result.add_error(
            f"SKILL.md not found in {format_path(skill_path)}"
        )
        return result

    # Read file
    try:
        content = read_file_safe(skill_file)
    except SkillError as e:
        result.add_error(str(e))
        return result

    # Parse frontmatter and body
    try:
        frontmatter, body = parse_skill_file(content)
    except SkillError as e:
        result.add_error(str(e))
        return result

    # Validate required fields
    if "name" not in frontmatter:
        result.add_error('Required field "name" missing from frontmatter')
    else:
        is_valid, error_msg = validate_skill_name(frontmatter["name"])
        if not is_valid:
            result.add_error(f"Invalid skill name: {error_msg}")

    if "description" not in frontmatter:
        result.add_error(
            'Required field "description" missing from frontmatter'
        )
    else:
        is_valid, error_msg = validate_skill_description(
            frontmatter["description"]
        )
        if not is_valid:
            result.add_error(f"Invalid description: {error_msg}")

    # Check for unexpected frontmatter fields
    expected_fields = {"name", "description", "tools", "model"}
    unexpected = set(frontmatter.keys()) - expected_fields
    if unexpected:
        msg = f"Unexpected frontmatter fields: {', '.join(sorted(unexpected))}"
        if strict:
            result.add_error(msg)
        else:
            result.add_warning(msg)

    # Validate body content
    if not body:
        msg = "SKILL.md body is empty (no content after frontmatter)"
        if strict:
            result.add_error(msg)
        else:
            result.add_warning(msg)
    elif len(body) < 100:
        result.add_warning(
            f"SKILL.md body is very short ({len(body)} chars). "
            "Consider adding more detailed instructions."
        )

    # Check for common sections
    body_lower = body.lower()
    recommended_sections = [
        ("when to use", "when to use this skill"),
        ("instruction", "step-by-step instructions"),
        ("example", "concrete examples"),
    ]

    for keyword, description in recommended_sections:
        if keyword not in body_lower:
            result.add_warning(
                f"Missing recommended section: {description}"
            )

    # Validate tool references if present
    if "tools" in frontmatter:
        tools = frontmatter["tools"]
        if isinstance(tools, str):
            tools_list = [t.strip() for t in tools.split(",")]
            valid_tools = {
                "Bash",
                "Read",
                "Write",
                "Edit",
                "Glob",
                "Grep",
                "WebFetch",
                "WebSearch",
            }
            invalid_tools = [
                t for t in tools_list if t and t not in valid_tools
            ]
            if invalid_tools:
                result.add_warning(
                    f"Unknown tools specified: {', '.join(invalid_tools)}"
                )

    # Validate model if present
    if "model" in frontmatter:
        model = frontmatter["model"]
        valid_models = {"sonnet", "opus", "haiku", "inherit"}
        if model not in valid_models:
            result.add_warning(
                f"Unknown model '{model}'. Valid options: "
                f"{', '.join(sorted(valid_models))}"
            )

    # Check directory structure
    skill_dir = skill_file.parent
    scripts_dir = skill_dir / "scripts"
    references_dir = skill_dir / "references"

    if scripts_dir.exists():
        python_files = list(scripts_dir.glob("*.py"))
        if python_files:
            # Check for __init__.py
            if not (scripts_dir / "__init__.py").exists():
                result.add_warning(
                    "scripts/ directory contains Python files but no "
                    "__init__.py"
                )

            # Check script permissions (Unix-like systems)
            if sys.platform != "win32":
                for script in python_files:
                    if not script.stat().st_mode & 0o111:
                        result.add_warning(
                            f"Script {script.name} is not executable. "
                            f"Consider: chmod +x {script}"
                        )

    if references_dir.exists():
        md_files = list(references_dir.glob("*.md"))
        if not md_files:
            result.add_warning(
                "references/ directory exists but contains no .md files"
            )

    return result


def main() -> int:
    """Main entry point for the validator.

    Returns:
        Exit code: 0 for success, 1 for validation failure, 2 for error
    """
    parser = argparse.ArgumentParser(
        description="Validate Claude skill files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate a skill directory
  %(prog)s path/to/skill/

  # Validate SKILL.md directly
  %(prog)s path/to/skill/SKILL.md

  # Strict mode (warnings become errors)
  %(prog)s --strict path/to/skill/

  # Quiet mode (only errors)
  %(prog)s --quiet path/to/skill/
        """,
    )

    parser.add_argument(
        "skill_path",
        type=Path,
        help="Path to skill directory or SKILL.md file",
    )

    parser.add_argument(
        "--strict",
        action="store_true",
        help="Enable strict validation (warnings become errors)",
    )

    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Quiet mode (only show errors, not warnings)",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Verbose output with additional details",
    )

    args = parser.parse_args()

    # Validate the skill
    try:
        result = validate_skill(args.skill_path, strict=args.strict)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    # Display results
    if args.verbose:
        print(f"Validating: {format_path(args.skill_path)}")
        print()

    if result.errors:
        print(result)
        return 1

    if result.warnings and not args.quiet:
        print(result)
        if not args.strict:
            print("\n✅ Validation passed (with warnings)")
            return 0
        else:
            print("\n❌ Validation failed (strict mode)")
            return 1

    if not args.quiet:
        print("✅ Validation passed")

    return 0


if __name__ == "__main__":
    sys.exit(main())
