import time
import sys
import psutil
import os
import pandas as pd
import json
from pathlib import Path

# Import the validation function from the parent directory
sys.path.append(str(Path(__file__).parent.parent))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from validation_utils import validate_dataframe

def run_validation(file_path, schema_path):
    """Run the validation and return performance metrics"""
    start_time = time.time()
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / 1024 / 1024  # MB
    
    # Load the schema
    with open(schema_path, "r") as schema_file:
        schema = json.load(schema_file)
    
    # Load the CSV file
    df = pd.read_csv(file_path, dtype=str, keep_default_na=False)
    
    # Run validation
    results = validate_dataframe(df, schema)
    
    end_time = time.time()
    mem_after = process.memory_info().rss / 1024 / 1024  # MB
    duration = end_time - start_time
    mem_usage = mem_after - mem_before
    
    return {
        'duration': duration,
        'mem_usage': mem_usage,
        'rows_processed': len(results),
        'valid_rows': sum(1 for r in results if r['Status'] == 'Valid'),
        'invalid_rows': sum(1 for r in results if r['Status'] == 'Invalid'),
        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
    }

def main():
    # Get the paths relative to this script
    base_dir = Path(__file__).parent.parent
    file_path = base_dir / "src" / "sample_dataset_cre.csv"  # Fixed path
    schema_path = base_dir / "src" / "cre-json-schema.json"  # Fixed path
    
    if not file_path.exists():
        print(f"Error: CSV file not found at {file_path}")
        return
    
    if not schema_path.exists():
        print(f"Error: Schema file not found at {schema_path}")
        return
    
    # Define the number of runs for each test
    run_counts = [1, 5, 10]
    
    print("\nStarting stress test...")
    print("-" * 80)
    print(f"Testing file: {file_path}")
    print(f"Using schema: {schema_path}")
    print("-" * 80)
    
    for run_count in run_counts:
        print(f"\nRunning validation {run_count} times...")
        
        total_start_time = time.time()
        metrics = []
        
        for i in range(run_count):
            print(f"  Run {i+1}/{run_count}...", end="", flush=True)
            metric = run_validation(file_path, schema_path)
            metrics.append(metric)
            print(f" completed in {metric['duration']:.4f}s")
        
        total_duration = time.time() - total_start_time
        avg_duration = sum(m['duration'] for m in metrics) / run_count
        avg_mem_usage = sum(m['mem_usage'] for m in metrics) / run_count
        
        # Print summary statistics
        print("\nSummary Statistics:")
        print(f"  Total time for {run_count} runs: {total_duration:.4f} seconds")
        print(f"  Average duration per run: {avg_duration:.4f} seconds")
        print(f"  Average memory usage: {avg_mem_usage:.2f} MB")
        print(f"  Average rows processed: {metrics[0]['rows_processed']}")
        print(f"  Valid rows: {metrics[0]['valid_rows']}")
        print(f"  Invalid rows: {metrics[0]['invalid_rows']}")
        
        # Print detailed metrics for first few runs
        if run_count > 5:
            print("\nDetailed metrics for first 5 runs:")
            for i, metric in enumerate(metrics[:5]):
                print(f"  Run {i+1}:")
                print(f"    Timestamp: {metric['timestamp']}")
                print(f"    Duration: {metric['duration']:.4f} seconds")
                print(f"    Memory Usage: {metric['mem_usage']:.2f} MB")
    
    print("\nStress test completed.")

if __name__ == "__main__":
    main()
