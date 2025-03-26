import json
import pandas as pd
import jsonschema
from jsonschema import Draft7Validator
from datetime import datetime
import csv

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
    errors = []
    try:
        validator = Draft7Validator(schema)
        error_list = list(validator.iter_errors(record))
        
        if not error_list:
            return True, "Valid record", []
        
        for error in error_list:
            failed_column = error.path[0] if error.path else "Unknown Column"
            error_message = f"Invalid record in column '{failed_column}': {error.message}"
            errors.append(error_message)
            print(f"Validation error in column '{failed_column}': {error.message}")
        
        return False, "Multiple validation errors", errors
    except Exception as e:
        return False, f"Validation failed: {str(e)}", [str(e)]

# Function to process and validate a dataframe
def validate_dataframe(df, schema):
    validation_results = []
    for _, row in df.iterrows():  # Iterate without using index
        record = row.to_dict()

        # Convert fields based on schema type while ignoring empty values
        for field, properties in schema.get("properties", {}).items():
            if field in record and record[field] not in ["", "NA", "NONE"]:
                try:
                    # Safely get the type name as a string
                    if isinstance(properties["type"], list):
                        type_name = properties["type"][0]
                    else:
                        type_name = properties["type"]
                    
                    if type_name == "integer":
                        record[field] = int(record[field])
                    elif type_name == "number":
                        record[field] = float(record[field])
                    elif properties.get("format") == "date":
                        record[field] = convert_date(record[field])
                except (ValueError, KeyError, TypeError) as e:
                    print(f"Error processing field {field}: {record[field]}")
                    print(f"Error details: {str(e)}")
                    
                    # Ensure type_name is a string before calling upper()
                    if 'type_name' not in locals():
                        if isinstance(properties.get("type"), list):
                            type_name = properties["type"][0]
                        else:
                            type_name = str(properties.get("type", "unknown"))
                    
                    record[field] = f"INVALID_{type_name.upper()}"

        is_valid, message, errors = validate_data(record, schema)

        result = {
            "Status": "Valid" if is_valid else "Invalid",
            "Message": message,
            "Errors": errors if errors else []
        }
        validation_results.append(result)
    
    return validation_results
