#!/usr/bin/env python3
"""
Simple fix for remaining code quality issues
"""

import os
import re

def fix_file(filepath):
    """Fix issues in a single file"""
    print(f"Processing {filepath}...")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Fix unused imports
        content = fix_unused_imports(content, filepath)

        # Fix long lines
        content = fix_long_lines(content)

        # Fix f-string issues
        content = fix_fstring_placeholders(content)

        # Only write if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  OK: Fixed {filepath}")
        else:
            print(f"  OK: No changes needed for {filepath}")

    except Exception as e:
        print(f"  ERROR: {e}")

def fix_unused_imports(content, filepath):
    """Remove unused imports"""
    # Specific unused imports for our test files
    unused_imports = {
        'tests/check_task_status.py': ['time'],
        'tests/download_video.py': ['os'],
        'tests/final_summary_clean.py': ['requests'],
        'tests/final_test_summary.py': ['json'],
        'tests/simple_test.py': ['json'],
        'tests/test_wan25_api.py': ['json', 'os'],
        'tests/test_wan25_api_fixed.py': ['json', 'time', 'os'],
        'tests/test_wan25_api_windows.py': ['json', 'os']
    }

    lines = content.split('\n')
    cleaned_lines = lines.copy()

    if filepath in unused_imports:
        for module in unused_imports[filepath]:
            for i, line in enumerate(cleaned_lines):
                if line.strip() == f'import {module}':
                    cleaned_lines[i] = ''
                    break
                elif line.strip().startswith(f'from {module} '):
                    cleaned_lines[i] = ''
                    break

    return '\n'.join(cleaned_lines)

def fix_long_lines(content):
    """Break up long lines"""
    lines = content.split('\n')

    for i, line in enumerate(lines):
        if len(line) > 88 and not line.strip().startswith('#'):
            # Handle specific long lines we know about
            if 'https://dashscope-result-sh.oss-accelerate.aliyuncs.com' in line:
                # Break at query parameters
                if '?' in line:
                    base_url = line.split('?')[0]
                    query = '?' + line.split('?')[1]
                    lines[i] = f"{base_url}\n        {query}"
            elif 'print(' in line and len(line) > 88:
                # Break print statements
                lines[i] = f"{line[:88]} \\\n    {line[88:]}"

    return '\n'.join(lines)

def fix_fstring_placeholders(content):
    """Fix f-strings without placeholders"""
    # Find f-strings that don't have any {variables}
    lines = content.split('\n')

    for i, line in enumerate(lines):
        if 'f"' in line and '{' not in line:
            # Remove f prefix if no placeholders
            lines[i] = line.replace('f"', '"')
        elif "f'" in line and '{' not in line:
            lines[i] = line.replace("f'", "'")

    return '\n'.join(lines)

def main():
    """Main function"""
    print("=" * 60)
    print("PROFBRAINROT REMAINING ISSUES FIX")
    print("=" * 60)

    # Get all Python files in tests directory
    test_files = []
    for root, dirs, files in os.walk('tests'):
        for file in files:
            if file.endswith('.py'):
                test_files.append(os.path.join(root, file))

    print(f"Found {len(test_files)} Python files to fix")

    # Process each file
    for filepath in test_files:
        fix_file(filepath)

    print("\n" + "=" * 60)
    print("Remaining issues fixed!")
    print("Run 'python -m flake8 tests/' to verify fixes")
    print("=" * 60)

if __name__ == "__main__":
    main()