import time
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import os

def test_validate_endpoint(file_path, api_url="http://localhost:8000/validate", num_requests=5):
    """Test the /validate endpoint with a CSV file"""
    
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found")
        return None
    
    results = []
    
    print(f"\nTesting /validate endpoint with {file_path}")
    print(f"Making {num_requests} requests...")
    
    for i in range(num_requests):
        print(f"  Request {i+1}/{num_requests}...", end="", flush=True)
        
        start_time = time.time()
        
        # Prepare the file for upload
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, 'text/csv')}
            
            # Make the request
            try:
                response = requests.post(api_url, files=files)
                response_time = time.time() - start_time
                
                # Process the response
                if response.status_code == 200:
                    data = response.json()
                    row_count = data.get('row_count', 0)
                    valid_count = sum(1 for r in data.get('results', []) if r.get('Status') == 'Valid')
                    invalid_count = sum(1 for r in data.get('results', []) if r.get('Status') == 'Invalid')
                    
                    result = {
                        'request_num': i+1,
                        'status_code': response.status_code,
                        'response_time': response_time,
                        'row_count': row_count,
                        'valid_count': valid_count,
                        'invalid_count': invalid_count
                    }
                    results.append(result)
                    print(f" completed in {response_time:.4f}s")
                else:
                    print(f" failed with status code {response.status_code}")
                    results.append({
                        'request_num': i+1,
                        'status_code': response.status_code,
                        'response_time': response_time,
                        'error': response.text
                    })
            except requests.exceptions.RequestException as e:
                print(f" error: {str(e)}")
                results.append({
                    'request_num': i+1,
                    'error': str(e),
                    'response_time': time.time() - start_time
                })
    
    # Print summary
    if results:
        successful_requests = [r for r in results if r.get('status_code') == 200]
        
        if successful_requests:
            avg_time = sum(r['response_time'] for r in successful_requests) / len(successful_requests)
            print("\nSummary:")
            print(f"  Successful requests: {len(successful_requests)}/{num_requests}")
            print(f"  Average response time: {avg_time:.4f} seconds")
            print(f"  Rows processed per request: {successful_requests[0].get('row_count', 'N/A')}")
            print(f"  Valid rows: {successful_requests[0].get('valid_count', 'N/A')}")
            print(f"  Invalid rows: {successful_requests[0].get('invalid_count', 'N/A')}")
            
            # Create a simple visualization
            if len(successful_requests) > 1:
                plt.figure(figsize=(10, 6))
                plt.plot([r['request_num'] for r in successful_requests], 
                         [r['response_time'] for r in successful_requests], 
                         marker='o')
                plt.title('API Response Time')
                plt.xlabel('Request Number')
                plt.ylabel('Response Time (seconds)')
                plt.grid(True)
                
                # Save the plot
                plot_path = os.path.join(os.path.dirname(file_path), 'api_response_times.png')
                plt.savefig(plot_path)
                print(f"\nResponse time plot saved to: {plot_path}")
        else:
            print("\nNo successful requests to analyze.")
    
    return results

def main():
    # Get the path to the sample CSV file
    base_dir = Path(__file__).parent.parent
    file_path = base_dir / "sample_dataset_cre.csv"
    
    # Test the API
    test_validate_endpoint(file_path, num_requests=3)
    
    print("\nAPI testing completed.")

if __name__ == "__main__":
    main()
