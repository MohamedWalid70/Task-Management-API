#!/usr/bin/env python3
"""
Test runner for the Task Management API
"""

import subprocess
import sys
import os


def run_tests():
    """Run the test suite"""
    print("🧪 Running Task Management API Tests")
    print("=" * 50)
    
    try:
        # Run pytest with verbose output
        result = subprocess.run([
            "python", "-m", "pytest", 
            "tests/", 
            "-v", 
            "--tb=short"
        ], capture_output=True, text=True, check=True)
        
        print("✅ All tests passed!")
        print("\nTest Results:")
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        print("❌ Some tests failed!")
        print("\nTest Results:")
        print(e.stdout)
        print("\nErrors:")
        print(e.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("❌ pytest not found. Please install it with:")
        print("   pip install pytest")
        sys.exit(1)


if __name__ == "__main__":
    run_tests() 