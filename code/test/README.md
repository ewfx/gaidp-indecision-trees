# Test Scripts for CSV Validation System

This directory contains test scripts for validating the performance and functionality of the CSV validation system.

## Available Tests

### 1. Stress Test (`stress_test.py`)

Tests the performance of the validation logic by running it multiple times and measuring:
- Execution time
- Memory usage
- Number of rows processed
- Validation results

**Usage:**
```bash
# Install dependencies
pip install psutil matplotlib

# Run the test
python test/stress_test.py
```

### 2. API Test (`api_test.py`)

Tests the API endpoints by making HTTP requests and measuring:
- Response time
- Success rate
- Validation results

**Usage:**
```bash
# Make sure the API server is running
# In another terminal: uvicorn api:app --reload

# Install dependencies
pip install requests matplotlib

# Run the test
python test/api_test.py
```

## Requirements

- Python 3.7+
- pandas
- psutil (for memory usage tracking)
- requests (for API testing)
- matplotlib (for visualizations)

## Adding New Tests

When adding new test scripts, please follow these guidelines:

1. Create a descriptive filename (e.g., `performance_test.py`)
2. Add documentation at the top of the file explaining its purpose
3. Update this README with information about the new test
4. Include any specific requirements or setup instructions
