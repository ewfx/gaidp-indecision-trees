# 🚀 Project Name

## 📌 Table of Contents

- [Introduction](#introduction)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction

This project extracts, interprets, and refines regulatory reporting instructions to identify key data validation requirements. It ensures compliance with financial regulations by automating the identification of data quality issues before submission. The system helps reduce manual effort, minimize reporting errors, and improve the consistency of regulatory filings.

Key features include:

- A JSON file defining validation rules for each column and allowable values.

- A sample dataset adhering to the defined schema.

- A Python script to validate the dataset against the rules.

- Comprehensive error reporting and logging to facilitate troubleshooting.

- Extensible rule definitions, allowing new regulatory requirements to be incorporated seamlessly.

🖼️ Screenshots:

![Screenshot 1](link-to-image)

## ⚙️ What It Does

Explain the key features and functionalities of your project.

## 🛠️ How We Built It

This project leverages a range of technologies and tools to ensure accurate and efficient regulatory data validation:

- Python: The core programming language used for processing and validating datasets.

- JSON: Defines the schema and validation rules for regulatory reporting.

- GitHub: Version control and collaboration platform for tracking changes and contributions.

## 🏃 How to Run

1. Clone the repository  
   ```sh
   git clone https://github.com/your-repo.git
   ```

2. Install Python dependencies for the FastAPI backend:
   ```sh
   cd code/src
   pip install -r requirements.txt
   ```

3. Install Node.js dependencies for the React frontend:
   ```sh
   cd ../ui
   npm install
   ```

4. Start the FastAPI backend:
   ```sh
   cd ../../code/src
   uvicorn api:app --reload
   ```

5. In a separate terminal, start the React frontend:
   ```sh
   cd ../ui
   npm start
   ```

Note: Make sure you have Python and Node.js installed on your system before running these commands. The backend runs on port 8000 and the frontend runs on port 3000.

## 🏗️ Tech Stack
- 🔹 Frontend: React 
- 🔹 Backend: FastAPI
- 🔹 Database: 
- 🔹 Other: OpenAI API

## 📈 Scalability
Our solution is designed with scalability in mind, using FastAPI for high-performance backend processing and React for efficient frontend rendering. The system demonstrates linear scalability in both processing time and memory usage as shown in our stress test results below.

```
Starting stress test...
--------------------------------------------------------------------------------
Base dataset rows: 11
Using schema: /Users/ashish/Desktop/Projects/gaidp-indecision-trees/code/src/cre-json-schema.json
--------------------------------------------------------------------------------

Simulating dataset with 11 rows...
  Completed in 0.0059 seconds
  Memory usage: 0.12 MB
  Processed rows: 11
  Valid rows: 5
  Invalid rows: 6

Simulating dataset with 110 rows...
  Completed in 0.0343 seconds
  Memory usage: 0.06 MB
  Processed rows: 110
  Valid rows: 50
  Invalid rows: 60

Simulating dataset with 1100 rows...
  Completed in 0.3309 seconds
  Memory usage: 0.41 MB
  Processed rows: 1100
  Valid rows: 500
  Invalid rows: 600

Simulating dataset with 11000 rows...
  Completed in 3.3055 seconds
  Memory usage: 8.58 MB
  Processed rows: 11000
  Valid rows: 5000
  Invalid rows: 6000

Simulating dataset with 110000 rows...
  Completed in 34.4670 seconds
  Memory usage: 54.88 MB
  Processed rows: 110000
  Valid rows: 50000
  Invalid rows: 60000

Stress test completed.
```

## 👥 Team
- **Pravanya Amirishetty** - [GitHub](#) | [LinkedIn](#)
- **Deepak R. Naik** - [GitHub](#) | [LinkedIn](#)
- **Vignesh Srinivasan** - [GitHub](#) | [LinkedIn](#)
- **Ashish Reddy** - [GitHub](#) | [LinkedIn](#)
- **Atreya Majumdar** - [GitHub](#) | [LinkedIn](#)
