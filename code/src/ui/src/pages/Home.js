import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { FiUploadCloud } from "react-icons/fi";

function Home() {
  const [file, setFile] = useState(null);
  const [rules, setRules] = useState([
    "Rule 1: All transactions above $10,000 must be reported.",
    "Rule 2: User authentication is required before processing payments.",
    "Rule 3: Transactions can only be performed within banking hours.",
    "Rule 4: A risk assessment is mandatory for international transfers."
  ]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleGenerateRules = async () => {
    if (!file) return alert("Please upload a PDF file.");
    
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://localhost:8000/extract_rules", formData);
      setRules(response.data.rules);
    } catch (error) {
      console.error("Error generating rules:", error);
    }
    setLoading(false);
  };

  return (
    <div className="flex flex-col items-center p-10 min-h-screen bg-gradient-to-br from-blue-500 to-purple-600">
      <div className="bg-white shadow-lg rounded-lg p-6 w-96 text-center">
        <label className="block text-gray-700 font-semibold mb-2">Upload PDF</label>
        <div className="flex items-center justify-center w-full mb-4">
          <label className="flex flex-col items-center px-4 py-6 bg-blue-50 text-blue-500 rounded-lg cursor-pointer border border-blue-300 hover:bg-blue-100">
            <FiUploadCloud className="text-3xl" />
            <span className="mt-2 text-sm">{file ? file.name : "Choose a file"}</span>
            <input type="file" accept="application/pdf" onChange={handleFileChange} className="hidden" />
          </label>
        </div>
        <button 
          onClick={handleGenerateRules} 
          className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition"
          disabled={loading}
        >
          {loading ? "Processing..." : "Generate Rules"}
        </button>
      </div>


      {/* Show Loader */}
      {loading && (
        <div className="flex justify-center mt-4">
          <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
        </div>
      )}


      {/* Rules Display */}
      <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-4">
        {rules.map((rule, index) => (
          <div key={index} className="bg-white p-4 rounded-lg shadow-lg w-80">
            <p className="text-gray-700">{rule}</p>
          </div>
        ))}
      </div>

      <button 
        onClick={() => navigate("/validate")} 
        className="mt-8 bg-green-500 text-white px-6 py-2 rounded-lg hover:bg-green-600 transition"
      >
        Validate
      </button>
    </div>
  );
}

export default Home;
