import os
import sys
import subprocess

def run_script(script_path):
    print(f"\nRunning: {script_path}")
    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.stderr:
        print("ERROR:", result.stderr)

def main():
    print("=== Global Seismic Trends Pipeline Started ===")

    run_script("src/api_fetch.py")
    run_script("src/data_cleaning.py")
    run_script("src/mysql_loader.py")

    print("\n=== Pipeline Completed Successfully ===")

if __name__ == "__main__":
    main()
