import json
import pandas as pd
import jsonschema
from jsonschema import validate
from datetime import datetime
import csv

# Load the JSON schema
with open("cre-json-schema.json", "r") as schema_file:
    schema = json.load(schema_file)

# Load the CSV file
csv_file_path = "new.csv"  # Replace with your actual file path
df = pd.read_csv(
    csv_file_path,
    dtype=str,               # Read all data as strings initially
    keep_default_na=False,   # Prevent automatic NaN conversion
    quoting=csv.QUOTE_NONE,  # Handle quoted fields properly
    sep=",",                 # Ensure proper CSV parsing
    header=0,                # Ensure first row is treated as headers
    index_col=False          # Prevent LoanNumber from being misused as an index
)

# Function to convert date fields to the correct format
def convert_date(value):
    try:
        if value in ["", "NA", "NONE", "9999-12-31"]:
            return value  # Keep empty or special values as-is
        return datetime.strptime(value, "%Y-%m-%d").strftime("%Y-%m-%d")  # Validate format
    except ValueError:
        return "INVALID_DATE"  # Mark invalid dates


# Function to validate data against schema
def validate_data(record, schema):
    # errors = []
    # try:
    #     validate(instance=record, schema=schema)
    #     return True, "Valid record"
    # except jsonschema.exceptions.ValidationError as err:
    #     failed_column = err.path[0] if err.path else "Unknown Column"
    #     print(f"Validation error in column '{failed_column}': {err.message}")
    #     return False, f"Invalid record in column '{failed_column}': {err.message}"

    errors = []
    try:
        validator = jsonschema.Draft7Validator(schema)
        error_list = list(validator.iter_errors(record))
        
        if not error_list:
            return True, "Valid record", []
        
        for error in error_list:
            failed_column = error.path[0] if error.path else "Unknown Column"
            error_message = f"Invalid record in column '{failed_column}': {error.message}"
            errors.append(error_message)
            print(f"Validation error in column '{failed_column}': {error.message}")
        
        return False, "Multiple validation errors found", errors
    except Exception as e:
        return False, f"Validation failed: {str(e)}", [str(e)]


# Convert DataFrame rows to dictionary and validate each record
validation_results = []
for _, row in df.iterrows():  # Iterate without using index
    record = row.to_dict()

    # Convert fields based on schema type while ignoring empty values
    for field, properties in schema.get("properties", {}).items():
        if field in record and record[field] not in ["", "NA", "NONE"]:
            try:
                # Handle the case where type might be a list (e.g., ["integer", "string"])
                type_name = properties["type"] if isinstance(properties["type"], str) else properties["type"][0]
                
                if type_name == "integer":
                    record[field] = int(record[field])
                elif type_name == "number":
                    record[field] = float(record[field])
                elif properties.get("format") == "date":
                    record[field] = convert_date(record[field])
            except (ValueError, KeyError):
                print(field, record[field])
                # Use the actual type name from the schema
                type_name = properties["type"] if isinstance(properties["type"], str) else properties["type"][0]
                record[field] = f"INVALID_{type_name.upper()}"

    is_valid, message, errors = validate_data(record, schema)

    result = {
        "Status": "Valid" if is_valid else "Invalid",
        "Message": message,
        "Errors": errors if errors else []
    }
    validation_results.append(result)
    results_df = pd.DataFrame(validation_results)
    csv_result = results_df.to_csv(index=False)



# Convert results to DataFrame and save to CSV
results_df = pd.DataFrame(validation_results)
results_df.to_csv("validation_results.csv", index=False)
print("Validation completed. Results saved to validation_results.csv")
