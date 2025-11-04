#!/usr/bin/env python3
"""
Targeted fix for specific remaining code quality issues
"""

import os
import re

def fix_specific_issues():
    """Fix the specific remaining issues identified by flake8"""

    # Define specific fixes for each file
    fixes = {
        'tests/check_task_status.py': {
            'unused_imports': ['time'],
            'long_lines': []
        },
        'tests/download_video.py': {
            'unused_imports': ['os'],
            'syntax_errors': True  # Has syntax error from previous fix
        },
        'tests/final_summary_clean.py': {
            'unused_imports': ['requests'],
            'long_lines': []
        },
        'tests/final_test_summary.py': {
            'unused_imports': ['json'],
            'long_lines': []
        },
        'tests/simple_test.py': {
            'unused_imports': ['json'],
            'long_lines': [(35, 104)]  # Line 35 is 104 chars
        },
        'tests/simple_test_clean.py': {
            'unused_imports': [],
            'long_lines': [(35, 104)]  # Line 35 is 104 chars
        },
        'tests/simple_test_final.py': {
            'unused_imports': [],
            'long_lines': [(35, 104)]  # Line 35 is 104 chars
        },
        'tests/test_wan25_api.py': {
            'unused_imports': ['json', 'os'],
            'long_lines': [(55, 218), (61, 157), (123, 98), (198, 103)]
        },
        'tests/test_wan25_api_fixed.py': {
            'syntax_errors': True,  # Has syntax error
            'long_lines': [(185, 105), (186, 100)]
        },
        'tests/test_wan25_api_windows.py': {
            'unused_imports': ['json', 'os'],
            'long_lines': [(59, 218), (65, 157), (127, 98), (202, 103)]
        }
    }

    print("=" * 60)
    print("FIXING SPECIFIC CODE QUALITY ISSUES")
    print("=" * 60)

    for filepath, issues in fixes.items():
        if os.path.exists(filepath):
            print(f"\nProcessing {filepath}...")

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                original_content = content

                # Fix unused imports
                if 'unused_imports' in issues:
                    content = fix_unused_imports_specific(content, issues['unused_imports'])

                # Fix long lines
                if 'long_lines' in issues:
                    content = fix_long_lines_specific(content, issues['long_lines'])

                # Fix syntax errors
                if 'syntax_errors' in issues and issues['syntax_errors']:
                    content = fix_syntax_errors_specific(content, filepath)

                # Fix f-string issues
                content = fix_fstring_issues_specific(content)

                # Only write if changes were made
                if content != original_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"  ✓ Fixed {filepath}")
                else:
                    print(f"  ✓ No changes needed for {filepath}")

            except Exception as e:
                print(f"  ✗ Error processing {filepath}: {e}")

def fix_unused_imports_specific(content, unused_modules):
    """Remove specific unused imports"""
    lines = content.split('\n')
    cleaned_lines = lines.copy()

    for module in unused_modules:
        for i, line in enumerate(cleaned_lines):
            if line.strip() == f'import {module}':
                cleaned_lines[i] = ''
                break
            elif line.strip().startswith(f'from {module} '):
                cleaned_lines[i] = ''
                break

    return '\n'.join(cleaned_lines)

def fix_long_lines_specific(content, long_lines):
    """Fix specific long lines"""
    lines = content.split('\n')

    for line_num, length in long_lines:
        if line_num <= len(lines):
            line = lines[line_num - 1]  # Convert to 0-based index
            if len(line) > 88:
                # Break at logical points
                if 'print(' in line and len(line) > 88:
                    # Break print statements
                    lines[line_num - 1] = break_up_print_line(line)
                elif '=' in line and ('"' in line or "'" in line):
                    # Break assignment strings
                    lines[line_num - 1] = break_up_assignment_line(line)
                else:
                    # Generic line break
                    lines[line_num - 1] = f"{line[:88]} \\\n    {line[88:]}"

    return '\n'.join(lines)

def break_up_print_line(line):
    """Break up long print statements"""
    if 'print(' in line and len(line) > 88:
        # Find the print statement
        if 'print(' in line:
            # Break after opening parenthesis
            parts = line.split('(', 1)
            if len(parts) == 2:
                before = parts[0] + '('
                after = parts[1]
                if len(after) > 60:
                    return f"{before}\n    {after}"
    return line

def break_up_assignment_line(line):
    """Break up long assignment lines"""
    if '=' in line and len(line) > 88:
        parts = line.split('=', 1)
        if len(parts) == 2:
            var_part = parts[0].strip()
            value_part = parts[1].strip()

            if len(value_part) > 60:
                # Use string concatenation for long strings
                if '"' in value_part or "'" in value_part:
                    # Find quote type
                    quote = '"' if '"' in value_part else "'"
                    content = value_part.strip(quote)

                    if len(content) > 60:
                        # Split at logical points
                        if ' ' in content:
                            words = content.split()
                            mid = len(words) // 2
                            first_half = ' '.join(words[:mid])
                            second_half = ' '.join(words[mid:])

                            return f"{var_part} = (\n    {quote}{first_half}{quote}\n    {quote}{second_half}{quote}\n)"

    return line

def fix_syntax_errors_specific(content, filepath):
    """Fix syntax errors from previous fixes"""
    # Fix common syntax errors
    content = content.replace('f"""', '"""')  # Fix triple quote f-strings
    content = content.replace("f'''", "'''")

    # Fix unterminated string literals
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.strip().endswith('"') and not line.strip().endswith('""'):
            # Check if this is part of a multi-line string
            if i > 0 and lines[i-1].strip().endswith('\\'):
                continue
            # This might be an unterminated string
            if len(line.strip()) > 10 and not line.strip().startswith('"'):
                lines[i] = line + '"'

    return '\n'.join(lines)

def fix_fstring_issues_specific(content):
    """Fix f-string issues"""
    lines = content.split('\n')

    for i, line in enumerate(lines):
        # Fix f-strings without placeholders
        if 'f"' in line and '{' not in line:
            lines[i] = line.replace('f"', '"')
        elif "f'" in line and '{' not in line:
            lines[i] = line.replace("f'", "'")

    return '\n'.join(lines)

def main():
    """Main function"""
    print("=" * 60)
    print("FIXING SPECIFIC CODE QUALITY ISSUES")
    print("=" * 60)

    fix_specific_issues()

    print("\n" + "=" * 60)
    print("Specific issues fixed!")
    print("Run 'python -m flake8 tests/' to verify fixes")
    print("=" * 60)

if __name__ == "__main__":
    main()