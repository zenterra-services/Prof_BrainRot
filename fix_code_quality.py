#!/usr/bin/env python3
"""
Code quality fix script for ProfBrainRot
Automatically fixes common style and quality issues
"""

import os
import re
import autopep8

def fix_file(filepath):
    """Fix common issues in a Python file"""
    print(f"Fixing {filepath}...")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Apply autopep8 for style fixes
        fixed_content = autopep8.fix_code(
            content,
            options={
                'max_line_length': 88,
                'ignore': ['E203', 'W503'],
                'aggressive': 2
            }
        )

        # Remove unused imports (basic version)
        lines = fixed_content.split('\n')
        cleaned_lines = []

        for line in lines:
            # Skip obvious unused imports
            if re.match(r'^import (json|time|os)$', line.strip()) and 'json' not in fixed_content[fixed_content.find(line):fixed_content.find(line)+1000]:
                continue
            cleaned_lines.append(line)

        # Ensure file ends with newline
        if cleaned_lines and not cleaned_lines[-1].endswith('\n'):
            cleaned_lines.append('')

        # Write back to file
        fixed_content = '\n'.join(cleaned_lines)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)

        print(f"✓ Fixed {filepath}")

    except Exception as e:
        print(f"✗ Error fixing {filepath}: {e}")

def main():
    """Fix all Python files in tests directory"""
    print("=" * 60)
    print("PROFBRAINROT CODE QUALITY FIX")
    print("=" * 60)

    # Check if autopep8 is available
    try:
        import autopep8
    except ImportError:
        print("Installing autopep8...")
        os.system("pip install autopep8")
        import autopep8

    # Get all Python files in tests directory
    test_files = []
    for root, dirs, files in os.walk('tests'):
        for file in files:
            if file.endswith('.py'):
                test_files.append(os.path.join(root, file))

    print(f"Found {len(test_files)} Python files to fix")

    # Fix each file
    for filepath in test_files:
        fix_file(filepath)

    print("\n" + "=" * 60)
    print("Code quality fixes completed!")
    print("Run 'python -m flake8 tests/' to verify fixes")
    print("=" * 60)

if __name__ == "__main__":
    main()