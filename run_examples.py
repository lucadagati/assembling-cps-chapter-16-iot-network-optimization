"""
Script to run all examples in the chapter16 package.

This script demonstrates the complete functionality of the IoT network
optimization package by running all available examples.
"""

import sys
import os
import subprocess
import time

def run_script(script_path, description):
    """Run a Python script and display results."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Script: {script_path}")
    print('='*60)
    
    try:
        start_time = time.time()
        result = subprocess.run([sys.executable, script_path], 
                               capture_output=True, text=True, cwd=os.getcwd())
        end_time = time.time()
        
        if result.returncode == 0:
            print("SUCCESS")
            print(f"Execution time: {end_time - start_time:.2f} seconds")
            if result.stdout:
                print("\nOutput:")
                print(result.stdout)
        else:
            print("FAILED")
            print(f"Error code: {result.returncode}")
            if result.stderr:
                print("\nError:")
                print(result.stderr)
            if result.stdout:
                print("\nOutput:")
                print(result.stdout)
                
    except Exception as e:
        print(f"EXCEPTION: {e}")
    
    print("\n" + "="*60)


def main():
    """Main function to run all examples."""
    print("Chapter 16 IoT Network Optimization - Example Runner")
    print("="*60)
    print("This script will run all available examples to demonstrate")
    print("the functionality of the IoT network optimization package.")
    print("="*60)
    
    # Define examples to run
    examples = [
        {
            "path": "examples/fire_detection/fire_detection_system.py",
            "description": "Fire Detection and Intervention System"
        },
        {
            "path": "examples/drone_network/drone_coordination.py", 
            "description": "Drone Network Coordination System"
        },
        {
            "path": "examples/iot_sensors/sensor_network.py",
            "description": "IoT Sensor Network System"
        },
        {
            "path": "data/sample_networks.py",
            "description": "Sample Networks Demo"
        }
    ]
    
    # Check if examples exist
    missing_examples = []
    for example in examples:
        if not os.path.exists(example["path"]):
            missing_examples.append(example["path"])
    
    if missing_examples:
        print("Missing example files:")
        for path in missing_examples:
            print(f"  - {path}")
        print("\nPlease ensure all example files are present.")
        return
    
    # Run examples
    total_start_time = time.time()
    
    for example in examples:
        run_script(example["path"], example["description"])
    
    total_end_time = time.time()
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print('='*60)
    print(f"Total execution time: {total_end_time - total_start_time:.2f} seconds")
    print(f"Examples run: {len(examples)}")
    print("\nAll examples completed!")
    print("Check the generated plots and output files for results.")
    
    # Additional information
    print(f"\n{'='*60}")
    print("ADDITIONAL INFORMATION")
    print('='*60)
    print("Generated files:")
    print("  - Network visualization plots (*.png)")
    print("  - Algorithm comparison charts")
    print("  - Performance analysis reports")
    print("\nNext steps:")
    print("  1. Review the generated visualizations")
    print("  2. Examine the console output for detailed results")
    print("  3. Try modifying parameters in the example scripts")
    print("  4. Run individual examples for focused testing")
    print("  5. Explore the documentation in the docs/ directory")


if __name__ == "__main__":
    main()
