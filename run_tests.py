"""
Script to run all tests in the chapter16 package.

This script runs the comprehensive test suite to verify the correctness
and performance of the IoT network optimization algorithms.
"""

import sys
import os
import subprocess
import time

def run_tests():
    """Run all tests using pytest."""
    print("Chapter 16 IoT Network Optimization - Test Runner")
    print("="*60)
    print("Running comprehensive test suite...")
    print("="*60)
    
    try:
        start_time = time.time()
        
        # Run pytest with verbose output
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/", 
            "-v", 
            "--tb=short",
            "--durations=10"
        ], capture_output=True, text=True, cwd=os.getcwd())
        
        end_time = time.time()
        
        print("Test Results:")
        print("="*60)
        
        if result.returncode == 0:
            print("ALL TESTS PASSED")
        else:
            print("SOME TESTS FAILED")
        
        print(f"Execution time: {end_time - start_time:.2f} seconds")
        
        if result.stdout:
            print("\nTest Output:")
            print(result.stdout)
        
        if result.stderr:
            print("\nError Output:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"EXCEPTION: {e}")
        return False


def run_individual_tests():
    """Run individual test modules."""
    test_modules = [
        "tests.test_algorithms"
    ]
    
    print("\n" + "="*60)
    print("INDIVIDUAL TEST MODULES")
    print("="*60)
    
    for module in test_modules:
        print(f"\nRunning {module}...")
        try:
            result = subprocess.run([
                sys.executable, "-m", "pytest", 
                module, 
                "-v"
            ], capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                print(f"{module} PASSED")
            else:
                print(f"{module} FAILED")
                if result.stdout:
                    print(result.stdout)
                if result.stderr:
                    print(result.stderr)
                    
        except Exception as e:
            print(f"EXCEPTION in {module}: {e}")


def check_dependencies():
    """Check if required dependencies are installed."""
    print("Checking dependencies...")
    
    required_packages = [
        "numpy", "matplotlib", "networkx", "scipy", 
        "pandas", "plotly", "pytest"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"{package} - OK")
        except ImportError:
            print(f"{package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install -r requirements.txt")
        return False
    
    print("All dependencies available")
    return True


def main():
    """Main function to run all tests."""
    print("Chapter 16 IoT Network Optimization - Test Suite")
    print("="*60)
    
    # Check dependencies
    if not check_dependencies():
        print("\nCannot run tests due to missing dependencies")
        return
    
    # Run main test suite
    success = run_tests()
    
    # Run individual test modules
    run_individual_tests()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    if success:
        print("All tests completed successfully!")
        print("\nThe IoT network optimization package is working correctly.")
        print("You can now use the algorithms and examples with confidence.")
    else:
        print("Some tests failed!")
        print("\nPlease check the error messages above and fix any issues.")
        print("The package may not work correctly until all tests pass.")
    
    print("\nTest coverage includes:")
    print("  - MST algorithms (Kruskal's, Prim's, Constrained)")
    print("  - Steiner Tree algorithms")
    print("  - Graph generation utilities")
    print("  - Network visualization")
    print("  - Edge cases and error handling")
    print("  - Performance validation")


if __name__ == "__main__":
    main()
