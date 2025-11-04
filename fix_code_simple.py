#!/usr/bin/env python3
"""
Simple code quality fix script for ProfBrainRot
Fixes basic style issues without Unicode characters
"""

import os
import subprocess

def main():
    print("=" * 60)
    print("PROFBRAINROT CODE QUALITY FIX")
    print("=" * 60)

    # Get all Python files in tests directory
    test_files = []
    for root, dirs, files in os.walk('tests'):
        for file in files:
            if file.endswith('.py'):
                test_files.append(os.path.join(root, file))

    print(f"Found {len(test_files)} Python files to fix")

    # Fix each file with autopep8
    for filepath in test_files:
        print(f"Fixing {filepath}...")
        try:
            # Run autopep8
            result = subprocess.run([
                'python', '-m', 'autopep8',
                '--in-place',
                '--max-line-length=88',
                '--ignore=E203,W503',
                filepath
            ], capture_output=True, text=True)

            if result.returncode == 0:
                print(f"  OK: Fixed {filepath}")
            else:
                print(f"  Warning: {result.stderr}")

        except Exception as e:
            print(f"  Error: {e}")

    print("\n" + "=" * 60)
    print("Code quality fixes completed!")
    print("Run 'python -m flake8 tests/' to verify fixes")
    print("=" * 60)

if __name__ == "__main__":
    main()