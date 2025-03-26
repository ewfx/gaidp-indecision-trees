import os
import requests
from PyPDF2 import PdfReader
import json

def extract_rules_from_pdfs(gemini_api_endpoint: str = 'http://gemini-api:3000/extract_rules'):
    """
    Extracts data profiling rules from PDF files and sends to Gemini API
    Returns JSON rules from Gemini API
    """
    # Directory containing PDF files
    pdf_dir = './pdfs/'
    
    # Iterate through all PDF files in directory
    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            # Read PDF file
            pdf_path = os.path.join(pdf_dir, filename)
            with open(pdf_path, 'rb') as file:
                pdf_reader = PdfReader(file)
                text = ''
                # Extract text from all pages
                for page in pdf_reader.pages:
                    text += page.extract_text()
                
                # Prepare request to Gemini API
                response = requests.post(
                    gemini_api_endpoint,
                    json={'text': text}
                )
                
                # Save JSON response
                if response.status_code == 200:
                    response_json = response.json()
                    output_filename = f'rules_{os.path.splitext(filename)[0]}.json'
                    with open(output_filename, 'w') as outfile:
                        json.dump(response_json, outfile, indent=2)
                    print(f"Successfully extracted rules from {filename}")
                else:
                    print(f"Failed to process {filename}. Status code: {response.status_code}")
