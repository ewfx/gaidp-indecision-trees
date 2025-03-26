import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Validate from "./pages/Validate";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/validate" element={<Validate />} />
      </Routes>
    </Router>
  );
}

export default App;
