import time
import sys
import psutil
import os
import pandas as pd
import json
import logging
from pathlib import Path

# Configure logging to suppress validation errors
logging.basicConfig(
    level=logging.WARNING,  # Set to WARNING to suppress lower level messages
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('validation.log'),  # Log errors to file
        # Removed StreamHandler to suppress console output
    ]
)

# Import the validation function from the parent directory
sys.path.append(str(Path(__file__).parent.parent))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from validation_utils import validate_dataframe

def run_validation(df, schema_path, scale_factor=1):
    """Run the validation and return performance metrics"""
    start_time = time.time()
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / 1024 / 1024  # MB
    
    # Scale the dataset by duplicating rows
    scaled_df = pd.concat([df] * scale_factor, ignore_index=True)
    
    # Load the schema
    with open(schema_path, "r") as schema_file:
        schema = json.load(schema_file)
    
    # Run validation
    validation_results = validate_dataframe(scaled_df, schema)
    
    end_time = time.time()
    mem_after = process.memory_info().rss / 1024 / 1024  # MB
    duration = end_time - start_time
    mem_usage = mem_after - mem_before
    
    return {
        'duration': duration,
        'mem_usage': mem_usage,
        'rows_processed': len(scaled_df),
        'valid_rows': sum(1 for r in validation_results if r['Status'] == 'Valid'),
        'invalid_rows': sum(1 for r in validation_results if r['Status'] == 'Invalid'),
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
    
    # Load the base dataset
    df = pd.read_csv(file_path, dtype=str, keep_default_na=False)
    
    # Define the scale factors for each run
    scale_factors = [1, 10, 100, 1000]
    
    print("\nStarting stress test...")
    print("-" * 80)
    print(f"Base dataset rows: {len(df)}")
    print(f"Using schema: {schema_path}")
    print("-" * 80)
    
    for scale_factor in scale_factors:
        total_rows = len(df) * scale_factor
        print(f"\nSimulating dataset with {total_rows} rows...")
        
        start_time = time.time()
        metrics = run_validation(df, schema_path, scale_factor)
        end_time = time.time()
        
        print(f"  Completed in {metrics['duration']:.4f} seconds")
        print(f"  Memory usage: {metrics['mem_usage']:.2f} MB")
        print(f"  Processed rows: {metrics['rows_processed']}")
        print(f"  Valid rows: {metrics['valid_rows']}")
        print(f"  Invalid rows: {metrics['invalid_rows']}")
    
    print("\nStress test completed.")

if __name__ == "__main__":
    main()
