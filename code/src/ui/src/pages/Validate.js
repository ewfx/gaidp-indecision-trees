import { useState } from "react";
import axios from "axios";
import { FiUploadCloud } from "react-icons/fi";

function Validate() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleValidate = async () => {
    if (!file) return alert("Please upload a CSV file.");
    
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://localhost:8000/validate", formData);
      
      // Add debug logging to see the response structure
      console.log("API Response:", response.data);
      
      // Extract and transform the results
      if (response.data && response.data.results) {
        const resultsWithFirstColumn = response.data.results.map(result => ({
          ...result,
          firstColumn: result.firstColumn || result.TransactionID
        }));
        setResults(resultsWithFirstColumn);
      } else {
        setResults([]); // Set empty array if no results
      }
    } catch (error) {
      console.error("Error validating data:", error);
      setResults([]); // Clear results on error
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
          <div className="space-y-4">
            {results
              .filter(result => result.Status === "Invalid") // Only show invalid rows
              .map((validation, index) => (
                <div key={index} className="bg-red-100 p-4 my-3 rounded-lg shadow">
                  <p className="font-semibold">
                    ID: {validation.id}  {/* Display the id field */}
                  </p>
                  <ul className="list-disc pl-5 text-red-600">
                    {validation.Errors.map((error, i) => (
                      <li key={i}>{error}</li>
                    ))}
                  </ul>
                </div>
              ))}
          </div>
          
          {/* Show statistics */}
          <div className="mt-6 p-4 bg-gray-100 rounded-lg">
            <h3 className="text-lg font-semibold">Validation Statistics:</h3>
            <p className="text-gray-700">
              Total Valid Rows: {results.filter(result => result.Status === "Valid").length}
            </p>
            <p className="text-gray-700">
              Total Rows with Errors: {results.filter(result => result.Status === "Invalid").length}
            </p>
            <p className="text-gray-700">
              Total Rows Processed: {results.length}
            </p>
          </div>
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
