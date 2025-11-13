#!/usr/bin/env python3
"""
Package Claude skills for distribution.

This script packages skills into distributable formats for sharing
across different Claude surfaces (Claude.ai, API, Claude Code).
"""

import argparse
import json
import shutil
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

from skill_utils import (
    ValidationResult,
    find_skill_file,
    parse_skill_file,
    read_file_safe,
    format_path,
    SkillError,
    SkillPackagingError,
)

from validate_skill import validate_skill


def create_manifest(
    skill_dir: Path, frontmatter: Dict[str, Any]
) -> Dict[str, Any]:
    """Create a manifest file for the skill package.

    Args:
        skill_dir: Path to skill directory
        frontmatter: Parsed YAML frontmatter from SKILL.md

    Returns:
        Manifest dictionary with metadata

    Examples:
        >>> from pathlib import Path
        >>> manifest = create_manifest(Path("skill"), {"name": "test"})
        >>> "name" in manifest
        True
    """
    manifest = {
        "name": frontmatter.get("name", ""),
        "description": frontmatter.get("description", ""),
        "version": "1.0.0",
        "packaged_at": datetime.utcnow().isoformat() + "Z",
        "format": "claude-skill",
        "format_version": "1.0",
    }

    # Add optional fields if present
    if "tools" in frontmatter:
        manifest["tools"] = frontmatter["tools"]
    if "model" in frontmatter:
        manifest["model"] = frontmatter["model"]

    # Check for additional resources
    scripts_dir = skill_dir / "scripts"
    references_dir = skill_dir / "references"

    manifest["includes_scripts"] = scripts_dir.exists() and any(
        scripts_dir.iterdir()
    )
    manifest["includes_references"] = references_dir.exists() and any(
        references_dir.iterdir()
    )

    return manifest


def collect_files(skill_dir: Path) -> List[Path]:
    """Collect all files to include in the package.

    Args:
        skill_dir: Path to skill directory

    Returns:
        List of file paths to include

    Raises:
        SkillPackagingError: If SKILL.md is not found
    """
    files: List[Path] = []

    # Required: SKILL.md
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        raise SkillPackagingError(f"SKILL.md not found in {skill_dir}")
    files.append(skill_file)

    # Optional: scripts directory
    scripts_dir = skill_dir / "scripts"
    if scripts_dir.exists() and scripts_dir.is_dir():
        for file in scripts_dir.rglob("*"):
            if file.is_file():
                files.append(file)

    # Optional: references directory
    references_dir = skill_dir / "references"
    if references_dir.exists() and references_dir.is_dir():
        for file in references_dir.rglob("*"):
            if file.is_file():
                files.append(file)

    # Optional: README.md at skill root
    readme = skill_dir / "README.md"
    if readme.exists():
        files.append(readme)

    return files


def package_as_zip(
    skill_dir: Path,
    output_path: Path,
    manifest: Optional[Dict[str, Any]] = None,
) -> None:
    """Package skill as a ZIP file.

    Args:
        skill_dir: Path to skill directory
        output_path: Path for output ZIP file
        manifest: Optional manifest dict to include

    Raises:
        SkillPackagingError: If packaging fails
    """
    files = collect_files(skill_dir)

    try:
        with zipfile.ZipFile(
            output_path, "w", zipfile.ZIP_DEFLATED
        ) as zf:
            # Add manifest if provided
            if manifest:
                manifest_json = json.dumps(manifest, indent=2)
                zf.writestr("manifest.json", manifest_json)

            # Add all skill files
            for file in files:
                arcname = file.relative_to(skill_dir)
                zf.write(file, arcname)

    except Exception as e:
        raise SkillPackagingError(f"Failed to create ZIP: {e}")


def package_as_directory(
    skill_dir: Path,
    output_path: Path,
    manifest: Optional[Dict[str, Any]] = None,
) -> None:
    """Package skill as a directory structure.

    Args:
        skill_dir: Path to skill directory
        output_path: Path for output directory
        manifest: Optional manifest dict to include

    Raises:
        SkillPackagingError: If packaging fails
    """
    files = collect_files(skill_dir)

    try:
        # Create output directory
        output_path.mkdir(parents=True, exist_ok=True)

        # Write manifest if provided
        if manifest:
            manifest_file = output_path / "manifest.json"
            manifest_json = json.dumps(manifest, indent=2)
            manifest_file.write_text(manifest_json, encoding="utf-8")

        # Copy all skill files
        for file in files:
            rel_path = file.relative_to(skill_dir)
            dest = output_path / rel_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, dest)

    except Exception as e:
        raise SkillPackagingError(f"Failed to create directory: {e}")


def package_skill(
    skill_path: Path,
    output: Optional[Path] = None,
    format: str = "zip",
    validate: bool = True,
    include_manifest: bool = True,
) -> Path:
    """Package a skill for distribution.

    Args:
        skill_path: Path to skill directory or SKILL.md
        output: Output path (defaults to skill-name.zip or skill-name/)
        format: Package format ("zip" or "directory")
        validate: Whether to validate before packaging
        include_manifest: Whether to include manifest.json

    Returns:
        Path to created package

    Raises:
        SkillPackagingError: If packaging fails
        SkillError: If validation fails
    """
    # Find skill directory
    skill_file = find_skill_file(skill_path)
    if not skill_file:
        raise SkillPackagingError(
            f"SKILL.md not found in {format_path(skill_path)}"
        )

    skill_dir = skill_file.parent

    # Validate if requested
    if validate:
        result = validate_skill(skill_dir, strict=False)
        if not result.is_valid:
            raise SkillError(
                f"Skill validation failed:\n{result}\n\n"
                "Use --no-validate to skip validation"
            )

    # Parse skill file for manifest
    content = read_file_safe(skill_file)
    frontmatter, _ = parse_skill_file(content)

    # Create manifest
    manifest = None
    if include_manifest:
        manifest = create_manifest(skill_dir, frontmatter)

    # Determine output path
    skill_name = frontmatter.get("name", skill_dir.name)
    if output is None:
        if format == "zip":
            output = Path(f"{skill_name}.zip")
        else:
            output = Path(skill_name)

    # Package based on format
    if format == "zip":
        package_as_zip(skill_dir, output, manifest)
    elif format == "directory":
        package_as_directory(skill_dir, output, manifest)
    else:
        raise SkillPackagingError(f"Unknown format: {format}")

    return output


def main() -> int:
    """Main entry point for the packager.

    Returns:
        Exit code: 0 for success, 1 for failure
    """
    parser = argparse.ArgumentParser(
        description="Package Claude skills for distribution",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Package as ZIP
  %(prog)s path/to/skill/

  # Package to specific output
  %(prog)s path/to/skill/ --output my-skill.zip

  # Package as directory
  %(prog)s path/to/skill/ --format directory

  # Skip validation
  %(prog)s path/to/skill/ --no-validate

  # Package without manifest
  %(prog)s path/to/skill/ --no-manifest
        """,
    )

    parser.add_argument(
        "skill_path",
        type=Path,
        help="Path to skill directory or SKILL.md file",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output path (defaults to skill-name.zip or skill-name/)",
    )

    parser.add_argument(
        "-f",
        "--format",
        choices=["zip", "directory"],
        default="zip",
        help="Package format (default: zip)",
    )

    parser.add_argument(
        "--no-validate",
        action="store_true",
        help="Skip validation before packaging",
    )

    parser.add_argument(
        "--no-manifest",
        action="store_true",
        help="Do not include manifest.json",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Verbose output",
    )

    args = parser.parse_args()

    try:
        if args.verbose:
            print(f"Packaging: {format_path(args.skill_path)}")

        output_path = package_skill(
            skill_path=args.skill_path,
            output=args.output,
            format=args.format,
            validate=not args.no_validate,
            include_manifest=not args.no_manifest,
        )

        print(f"✅ Successfully packaged to: {format_path(output_path)}")

        if args.verbose:
            # Show package size
            if output_path.is_file():
                size = output_path.stat().st_size
                size_kb = size / 1024
                print(f"   Size: {size_kb:.1f} KB")
            else:
                # Count files in directory
                files = list(output_path.rglob("*"))
                file_count = len([f for f in files if f.is_file()])
                print(f"   Files: {file_count}")

        return 0

    except SkillError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback

            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
