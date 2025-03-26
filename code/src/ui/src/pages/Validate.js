import { useState } from "react";
import axios from "axios";
import { FiUploadCloud } from "react-icons/fi";

function Validate() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState([
    {
      transactionId: 1001,
      errors: [
        "Invalid date format (expected YYYY-MM-DD, got 03/24/2025).",
        "Amount exceeds limit ($12,000 > $10,000)."
      ]
    },
    {
      transactionId: 1002,
      errors: [
        "User authentication missing.",
        "Email format incorrect (missing '@')."
      ]
    },
    {
      transactionId: 1003,
      errors: [
        "Transaction ID missing.",
        "Negative amount is not allowed."
      ]
    }
  ]);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleValidate = async () => {
    if (!file) return alert("Please upload a CSV file.");
    
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("https://api.example.com/validate", formData);
      setResults(response.data.validations);
    } catch (error) {
      console.error("Error validating data:", error);
    }
    setLoading(false);
  };

  return (
    <div className="flex flex-col items-center p-10 min-h-screen bg-gradient-to-br from-green-500 to-teal-600">
      <div className="bg-white shadow-lg rounded-lg p-6 w-96 text-center">
        <label className="block text-gray-700 font-semibold mb-2">Upload CSV</label>
        <div className="flex items-center justify-center w-full mb-4">
          <label className="flex flex-col items-center px-4 py-6 bg-green-50 text-green-500 rounded-lg cursor-pointer border border-green-300 hover:bg-green-100">
            <FiUploadCloud className="text-3xl" />
            <span className="mt-2 text-sm">{file ? file.name : "Choose a file"}</span>
            <input type="file" accept=".csv" onChange={handleFileChange} className="hidden" />
          </label>
        </div>
        <button 
          onClick={handleValidate} 
          className="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition"
          disabled={loading}
        >
          {loading ? "Validating..." : "Validate"}
        </button>
      </div>

       {/* Show Loader */}
       {loading && (
        <div className="flex justify-center mt-4">
          <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
        </div>
      )}

      

      {results.length > 0 && (
        <div className="mt-6">
          <h2 className="text-lg font-bold">Validation Results</h2>
          {results.map((validation, index) => (
            <div key={index} className="bg-red-100 p-4 my-3 rounded-lg shadow">
              <p className="font-semibold">Transaction ID: {validation.transactionId}</p>
              <ul className="list-disc pl-5 text-red-600">
                {validation.errors.map((error, i) => (
                  <li key={i}>{error}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}

      {/* Validation Results */}
      {/* <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-4">
        {results.map((result, index) => (
          <div key={index} className="bg-white p-4 rounded-lg shadow-lg w-80">
            <p className="text-gray-700">{result}</p>
          </div>
        ))}
        
      </div> */}
    </div>
  );
}

export default Validate;
