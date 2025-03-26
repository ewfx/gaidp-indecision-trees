# Rules Engine Stress Test

This directory contains stress test scripts for validating the performance of the rules engine.

## Available Tests

### 1. Stress Test (`stress_test.py`)

Tests the performance of the rules engine by running validation multiple times and measuring:
- Execution time
- Memory usage
- Number of rows processed
- Validation results

**Usage:**
```bash
pip install psutil

python test/stress_test.py
```

## Requirements

- Python 3.7+
- pandas
- psutil (for memory usage tracking)

## Adding New Tests

When adding new test scripts, please follow these guidelines:

1. Create a descriptive filename (e.g., `performance_test.py`)
2. Add documentation at the top of the file explaining its purpose
3. Update this README with information about the new test
4. Include any specific requirements or setup instructions
