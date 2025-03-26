import uvicorn
import os

if __name__ == "__main__":
    # Make sure we're running from the directory containing this file
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
