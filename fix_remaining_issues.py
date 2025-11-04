#!/usr/bin/env python3
"""
Comprehensive fix for remaining code quality issues
Addresses unused imports, long lines, and f-string formatting
"""

import os
import re

def fix_unused_imports(content, filepath):
    """Remove unused imports from Python code"""
    lines = content.split('\n')

    # Find all imports
    import_lines = []
    used_modules = set()

    for i, line in enumerate(lines):
        if line.strip().startswith('import ') or line.strip().startswith('from '):
            import_lines.append((i, line.strip()))

        # Check if modules are used later in the file
        if 'import ' in line and not line.strip().startswith('import ') and not line.strip().startswith('from '):
            # This is a usage, not an import
            continue

        # Extract module names from imports
        if line.strip().startswith('import '):
            module = line.strip().replace('import ', '').split()[0]
            used_modules.add(module)
        elif line.strip().startswith('from '):
            module = line.strip().replace('from ', '').split()[0]
            used_modules.add(module)

    # Remove unused imports
    cleaned_lines = lines.copy()

    # Common unused imports in our test files
    unused_imports = {
        'tests/check_task_status.py': ['time'],
        'tests/download_video.py': ['os'],
        'tests/final_summary_clean.py': ['requests'],
        'tests/final_test_summary.py': ['json'],
        'tests/simple_test.py': ['json'],
        'tests/simple_test_clean.py': [],
        'tests/simple_test_final.py': [],
        'tests/test_wan25_api.py': ['json', 'os'],
        'tests/test_wan25_api_fixed.py': ['json', 'time', 'os'],
        'tests/test_wan25_api_windows.py': ['json', 'os']
    }

    # Remove specific unused imports
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
    """Break up long lines while preserving functionality"""
    lines = content.split('\n')

    for i, line in enumerate(lines):
        if len(line) > 88 and not line.strip().startswith('#'):
            # Handle different types of long lines

            # Long strings
            if '"' in line or "'" in line:
                # Break up long strings
                if 'print(' in line and 'f"' in line:
                    # Break up f-strings
                    lines[i] = break_up_fstring(line)
                elif 'print(' in line and "'" in line:
                    # Break up regular strings in print
                    lines[i] = break_up_print_string(line)
                elif '=' in line and ('"' in "'" in line):
                    # Break up long assignment strings
                    lines[i] = break_up_assignment_string(line)

            # Long function calls
            elif '(' in line and len(line.split('(')) > 1:
                lines[i] = break_up_function_call(line)

            # Long URLs or paths
            elif 'http' in line and len(line) > 88:
                lines[i] = break_up_url(line)

    return '\n'.join(lines)

def break_up_fstring(line):
    """Break up long f-strings"""
    # Find the f-string part
    if 'f"' in line:
        parts = line.split('f"')
        if len(parts) > 1:
            before = parts[0]
            fstring_content = parts[1].split('"')[0]
            after = '"'.join(parts[1].split('"')[1:])

            # Break up the content
            if len(fstring_content) > 60:
                # Split at logical points
                if ' ' in fstring_content:
                    words = fstring_content.split()
                    mid = len(words) // 2
                    first_half = ' '.join(words[:mid])
                    second_half = ' '.join(words[mid:])

                    return f"{before}f\"{first_half}\" \\\n    f\"{second_half}\"{after}"

    return line

def break_up_print_string(line):
    """Break up long strings in print statements"""
    if 'print(' in line and "'" in line:
        # Find the string content
        match = re.search(r"print\((.*)\)", line)
        if match:
            content = match.group(1)
            if len(content) > 60:
                # Split into multiple print statements
                return f"{line[:88]} \\\n    {line[88:]}"
    return line

def break_up_assignment_string(line):
    """Break up long assignment strings"""
    if '=' in line and ('"' in line or "'" in line):
        parts = line.split('=', 1)
        if len(parts) == 2:
            var_part = parts[0].strip()
            value_part = parts[1].strip()

            if len(value_part) > 60:
                # Use implicit string concatenation
                if '"' in value_part:
                    quote = '"'
                else:
                    quote = "'"

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

def break_up_function_call(line):
    """Break up long function calls"""
    if '(' in line and len(line.split('(')) > 1:
        # Find the opening parenthesis
        paren_pos = line.find('(')
        if paren_pos > 0:
            before_paren = line[:paren_pos]
            after_paren = line[paren_pos:]

            if len(after_paren) > 60:
                # Break after opening parenthesis
                return f"{before_paren}(\n    {after_paren[1:]}"

    return line

def break_up_url(line):
    """Break up long URLs"""
    if 'http' in line and len(line) > 88:
        # Find URL boundaries
        url_match = re.search(r'https?://[^\s]+', line)
        if url_match:
            url = url_match.group(0)
            if len(url) > 60:
                # Break URL at query parameters
                if '?' in url:
                    base_url = url.split('?')[0]
                    query = '?' + url.split('?')[1]

                    # Replace in original line
                    new_line = line.replace(url, f"{base_url}\n        {query}")
                    return new_line

    return line

def fix_fstring_placeholders(line):
    """Fix f-strings without placeholders"""
    # Find f-strings that don't have any {variables}
    if 'f"' in line and '{' not in line:
        # Remove f prefix if no placeholders
        return line.replace('f"', '"')
    elif "f'" in line and '{' not in line:
        return line.replace("f'", "'")

    return line

def process_file(filepath):
    """Process a single file"""
    print(f"Processing {filepath}...")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Apply fixes
        content = fix_unused_imports(content, filepath)
        content = fix_long_lines(content)
        content = fix_fstring_placeholders(content)

        # Only write if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✓ Fixed {filepath}")
        else:
            print(f"  ✓ No changes needed for {filepath}")

    except Exception as e:
        print(f"  ✗ Error processing {filepath}: {e}")

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
        process_file(filepath)

    print("\n" + "=" * 60)
    print("Remaining issues fixed!")
    print("Run 'python -m flake8 tests/' to verify fixes")
    print("=" * 60)

if __name__ == "__main__":
    main()