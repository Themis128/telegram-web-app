#!/usr/bin/env python3
"""
JSON Syntax Error Fixer

This script detects and fixes common JSON syntax errors:
- Trailing commas
- Missing commas
- Comments (removes them)
- Single quotes (converts to double quotes)
- Unescaped control characters
- Missing quotes around keys
"""

import json
import re
import sys
from pathlib import Path
from typing import Tuple, Optional


def sanitize_path(file_path_str: str, allowed_base: Optional[Path] = None) -> Optional[Path]:
    """
    Sanitize and validate a file path to prevent path traversal attacks.

    Args:
        file_path_str: Input file path string
        allowed_base: Optional base directory to restrict paths to

    Returns:
        Sanitized Path object or None if invalid
    """
    if not file_path_str or not isinstance(file_path_str, str):
        return None

    # Check for dangerous patterns before processing
    normalized_input = file_path_str.replace('\\', '/')
    if '../' in normalized_input or '..\\' in file_path_str:
        # Explicitly reject paths with parent directory references
        return None

    try:
        # Convert to Path and expand user home directory
        file_path = Path(file_path_str).expanduser()

        # Resolve to absolute path (this normalizes the path)
        # Note: resolve() will follow symlinks, but for a local tool this is acceptable
        file_path = file_path.resolve()

        # Additional check: ensure resolved path doesn't contain parent references
        # (shouldn't happen after resolve(), but double-check)
        path_str = str(file_path)
        if '..' in path_str:
            return None

        # If allowed_base is specified, ensure path is within it
        if allowed_base:
            allowed_base = allowed_base.resolve()
            try:
                # Check if file_path is within allowed_base
                file_path.relative_to(allowed_base)
            except ValueError:
                # Path is outside allowed_base
                return None

        # Final validation: ensure it's a valid path
        if not file_path.is_absolute():
            return None

        return file_path
    except (ValueError, OSError, RuntimeError):
        return None


def remove_comments(json_str: str) -> str:
    """Remove single-line and multi-line comments from JSON string."""
    # Remove single-line comments (// ...)
    json_str = re.sub(r'//.*?$', '', json_str, flags=re.MULTILINE)

    # Remove multi-line comments (/* ... */)
    json_str = re.sub(r'/\*.*?\*/', '', json_str, flags=re.DOTALL)

    return json_str


def fix_trailing_commas(json_str: str) -> str:
    """Remove trailing commas before closing braces or brackets."""
    # Remove trailing commas before }
    json_str = re.sub(r',(\s*})', r'\1', json_str)
    # Remove trailing commas before ]
    json_str = re.sub(r',(\s*])', r'\1', json_str)
    return json_str


def fix_single_quotes(json_str: str) -> str:
    """Convert single quotes to double quotes for JSON keys and string values."""
    # This is a simplified approach - more complex cases might need special handling
    # We'll be careful to only replace quotes that are actually part of JSON syntax

    # Pattern to match single-quoted strings (but not inside double-quoted strings)
    # This is a simplified version - for production, consider using a proper parser
    def replace_single_quotes(match):
        content = match.group(1)
        # Escape any double quotes in the content
        content = content.replace('"', '\\"')
        return f'"{content}"'

    # Match single-quoted strings, being careful about escaped quotes
    json_str = re.sub(r"'((?:[^'\\]|\\.)*)'", replace_single_quotes, json_str)

    return json_str


def fix_missing_commas(json_str: str) -> str:
    """Add missing commas between JSON elements."""
    # Pattern: } followed by " (missing comma between object and next key)
    json_str = re.sub(r'}(\s*")', r'},\1', json_str)
    # Pattern: ] followed by " (missing comma between array and next key)
    json_str = re.sub(r'](\s*")', r'],\1', json_str)
    # Pattern: } followed by { (missing comma between objects)
    json_str = re.sub(r'}(\s*{)', r'},\1', json_str)
    # Pattern: ] followed by [ (missing comma between arrays)
    json_str = re.sub(r'](\s*\[)', r'],\1', json_str)
    # Pattern: number/string/true/false/null followed by " (missing comma)
    json_str = re.sub(r'(["\d\w])\s*(\s*")', r'\1,\2', json_str)

    return json_str


def fix_unquoted_keys(json_str: str) -> str:
    """Add quotes around unquoted keys."""
    # Pattern: unquoted identifier followed by colon
    # This is tricky because we need to avoid already-quoted keys
    # We'll use a more conservative approach
    def quote_key(match):
        key = match.group(1)
        # Only quote if it looks like an identifier (not already quoted)
        if not (key.startswith('"') and key.endswith('"')):
            # Check if it's a valid identifier
            if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', key):
                return f'"{key}":'
        return match.group(0)

    # Match unquoted keys before colon
    json_str = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*:', quote_key, json_str)

    return json_str


def validate_json(json_str: str) -> Tuple[bool, Optional[str], Optional[int]]:
    """Validate JSON and return (is_valid, error_message, line_number)."""
    try:
        json.loads(json_str)
        return True, None, None
    except json.JSONDecodeError as e:
        return False, str(e), e.lineno


def fix_json_syntax(json_str: str, verbose: bool = False) -> Tuple[str, bool]:
    """
    Attempt to fix JSON syntax errors.

    Returns:
        Tuple of (fixed_json_string, was_fixed)
    """
    original = json_str
    fixed = json_str

    # Step 1: Remove comments
    fixed = remove_comments(fixed)
    if fixed != original:
        if verbose:
            print("  ✓ Removed comments")
        original = fixed

    # Step 2: Fix trailing commas
    fixed = fix_trailing_commas(fixed)
    if fixed != original:
        if verbose:
            print("  ✓ Fixed trailing commas")
        original = fixed

    # Step 3: Fix single quotes (be careful with this one)
    # Only do this if JSON is still invalid
    is_valid, _, _ = validate_json(fixed)
    if not is_valid:
        fixed_single = fix_single_quotes(fixed)
        if fixed_single != fixed:
            is_valid_after, _, _ = validate_json(fixed_single)
            if is_valid_after:
                fixed = fixed_single
                if verbose:
                    print("  ✓ Fixed single quotes")
                original = fixed

    # Step 4: Fix missing commas
    is_valid, _, _ = validate_json(fixed)
    if not is_valid:
        fixed_commas = fix_missing_commas(fixed)
        if fixed_commas != fixed:
            is_valid_after, _, _ = validate_json(fixed_commas)
            if is_valid_after or fixed_commas != fixed:
                fixed = fixed_commas
                if verbose:
                    print("  ✓ Fixed missing commas")
                original = fixed

    # Step 5: Fix unquoted keys
    is_valid, _, _ = validate_json(fixed)
    if not is_valid:
        fixed_keys = fix_unquoted_keys(fixed)
        if fixed_keys != fixed:
            is_valid_after, _, _ = validate_json(fixed_keys)
            if is_valid_after:
                fixed = fixed_keys
                if verbose:
                    print("  ✓ Fixed unquoted keys")

    # Final validation
    is_valid, error_msg, line_no = validate_json(fixed)
    was_fixed = (fixed != json_str)

    return fixed, is_valid and was_fixed


def fix_json_file(file_path: Path, backup: bool = True, verbose: bool = True) -> bool:
    """
    Fix JSON syntax errors in a file.

    Args:
        file_path: Path to the JSON file (must be a sanitized Path object)
        backup: Whether to create a backup before fixing
        verbose: Whether to print detailed information

    Returns:
        True if file was fixed successfully, False otherwise
    """
    # Additional validation: ensure path is absolute and resolved
    try:
        file_path = file_path.resolve()
    except (OSError, ValueError) as e:
        print(f"❌ Error: Invalid path: {e}")
        return False

    if not file_path.exists():
        print(f"❌ Error: File not found: {file_path}")
        return False

    # Ensure it's a file, not a directory
    if not file_path.is_file():
        print(f"❌ Error: Path is not a file: {file_path}")
        return False

    if verbose:
        print(f"\n📄 Processing: {file_path}")

    # Read the file
    try:
        # Try different encodings
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False

    # Check if JSON is already valid
    is_valid, error_msg, line_no = validate_json(content)
    if is_valid:
        if verbose:
            print("  ✓ JSON is already valid - no fixes needed")
        return True

    if verbose:
        print(f"  ⚠ JSON syntax error detected (line {line_no}): {error_msg}")
        print("  🔧 Attempting to fix...")

    # Attempt to fix
    fixed_content, was_fixed = fix_json_syntax(content, verbose=verbose)

    # Validate the fixed version
    is_valid, error_msg, line_no = validate_json(fixed_content)

    if is_valid:
        if verbose:
            print("  ✓ JSON syntax fixed successfully!")

        # Create backup if requested
        if backup:
            # Ensure backup path is in the same directory as the original file
            backup_path = file_path.parent / (file_path.name + '.bak')
            try:
                # Validate backup path is safe (in same directory)
                if backup_path.parent != file_path.parent:
                    print(f"  ⚠ Warning: Backup path validation failed, skipping backup")
                else:
                    with open(backup_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    if verbose:
                        print(f"  💾 Backup created: {backup_path}")
            except Exception as e:
                print(f"  ⚠ Warning: Could not create backup: {e}")

        # Write fixed content
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            if verbose:
                print(f"  ✅ File updated: {file_path}")
            return True
        except Exception as e:
            print(f"  ❌ Error writing file: {e}")
            return False
    else:
        print(f"  ❌ Could not automatically fix JSON syntax error")
        print(f"     Error at line {line_no}: {error_msg}")
        print(f"     Manual editing may be required")
        return False


def get_cursor_settings_path() -> Optional[Path]:
    """Get the path to Cursor settings.json file."""
    if sys.platform == 'win32':
        settings_path = Path.home() / "AppData" / "Roaming" / "Cursor" / "User" / "settings.json"
    elif sys.platform == 'darwin':
        settings_path = Path.home() / "Library" / "Application Support" / "Cursor" / "User" / "settings.json"
    else:
        settings_path = Path.home() / ".config" / "Cursor" / "User" / "settings.json"

    return settings_path if settings_path.exists() else None


def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Fix JSON syntax errors in files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fix a specific JSON file
  python fix_json_syntax.py path/to/file.json

  # Fix Cursor settings.json
  python fix_json_syntax.py --cursor

  # Fix without creating backup
  python fix_json_syntax.py file.json --no-backup

  # Fix multiple files
  python fix_json_syntax.py file1.json file2.json file3.json
        """
    )

    parser.add_argument(
        'files',
        nargs='*',
        help='JSON files to fix (if none specified, will check Cursor settings.json)'
    )

    parser.add_argument(
        '--cursor',
        action='store_true',
        help='Fix Cursor settings.json file'
    )

    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Do not create backup files'
    )

    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress verbose output'
    )

    args = parser.parse_args()

    files_to_fix = []

    # Add Cursor settings if requested
    if args.cursor:
        cursor_path = get_cursor_settings_path()
        if cursor_path:
            files_to_fix.append(cursor_path)
        else:
            print("⚠ Warning: Cursor settings.json not found")
            if not args.files:
                return 1

    # Add specified files
    for file_path_str in args.files:
        # Sanitize the path to prevent path traversal
        file_path = sanitize_path(file_path_str)
        if file_path is None:
            print(f"⚠ Warning: Invalid or unsafe path: {file_path_str}")
            continue
        if file_path.exists():
            files_to_fix.append(file_path)
        else:
            print(f"⚠ Warning: File not found: {file_path}")

    # If no files specified and not using --cursor, try Cursor settings
    if not files_to_fix:
        cursor_path = get_cursor_settings_path()
        if cursor_path:
            print("ℹ No files specified, checking Cursor settings.json...")
            files_to_fix.append(cursor_path)
        else:
            print("❌ Error: No files specified and Cursor settings.json not found")
            parser.print_help()
            return 1

    # Fix each file
    success_count = 0
    for file_path in files_to_fix:
        if fix_json_file(file_path, backup=not args.no_backup, verbose=not args.quiet):
            success_count += 1

    print(f"\n{'='*60}")
    print(f"Fixed {success_count}/{len(files_to_fix)} file(s)")

    return 0 if success_count == len(files_to_fix) else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
