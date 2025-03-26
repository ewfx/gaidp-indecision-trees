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
csv_file_path = "sample_dataset_cre.csv"  # Replace with your actual file path
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
    try:
        validate(instance=record, schema=schema)
        return True, "Valid record"
    except jsonschema.exceptions.ValidationError as err:
        print(err.message)
        return False, f"Invalid record: {err.message}"

# Convert DataFrame rows to dictionary and validate each record
validation_results = []
print(df)
for _, row in df.iterrows():  # Iterate without using index
    record = row.to_dict()

    # Convert fields based on schema type while ignoring empty values
    for field, properties in schema.get("properties", {}).items():
        if field in record and record[field] not in ["", "NA", "NONE"]:
            try:
                if "integer" in properties["type"]:
                    record[field] = int(record[field])
                elif "number" in properties["type"]:
                    record[field] = float(record[field])
                elif properties.get("format") == "date":
                    record[field] = convert_date(record[field])
            except ValueError:
                # print(field, record[field])
                record[field] = f"INVALID_{properties['type'].upper()}"

    is_valid, message = validate_data(record, schema)

    # Append the original row with validation results
    record["Status"] = "Valid" if is_valid else "Invalid"
    record["Message"] = message
    # print(record)
    if is_valid == False:
        break
    validation_results.append(record["Status"])

# Convert results to DataFrame and save to CSV
results_df = pd.DataFrame(validation_results)
results_df.to_csv("validation_results.csv", index=False)

print("Validation completed. Results saved to validation_results.csv")
