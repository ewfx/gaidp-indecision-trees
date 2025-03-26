from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import json
import csv
from io import StringIO
import os
from validation_utils import validate_dataframe

app = FastAPI(
    title="CSV Validation API",
    description="API for validating CSV files against a JSON schema",
    version="1.0.0"
)

# Load the JSON schema
schema_path = os.path.join(os.path.dirname(__file__), "cre-json-schema.json")
try:
    with open(schema_path, "r") as schema_file:
        schema = json.load(schema_file)
except FileNotFoundError:
    # For development, we'll set a placeholder
    # In production, this should raise an error or use a default schema
    schema = {"properties": {}}
    print(f"Warning: Schema file {schema_path} not found")

@app.get("/")
async def root():
    return {"message": "CSV Validation API is running. Go to /docs for the API documentation."}

@app.post("/validate", summary="Validate a CSV file")
async def validate_csv(file: UploadFile = File(...)):
    """
    Upload a CSV file to validate against the CRE JSON schema.
    
    Returns validation results for each row in the CSV.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    try:
        # Read the file content
        contents = await file.read()
        # Convert bytes to string
        s = contents.decode('utf-8')
        
        # Read the CSV into a pandas DataFrame
        df = pd.read_csv(
            StringIO(s),
            dtype=str,
            keep_default_na=False,
            quoting=csv.QUOTE_NONE,
            sep=",",
            header=0,
            index_col=False
        )
        
        # Validate the data
        validation_results = validate_dataframe(df, schema)
        
        # Return the validation results
        return JSONResponse(
            content={
                "filename": file.filename,
                "row_count": len(df),
                "results": validation_results
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.get("/schema", summary="Get the current validation schema")
async def get_schema():
    """
    Returns the JSON schema currently being used for validation.
    """
    return JSONResponse(content=schema)
