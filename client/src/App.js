import "./App.css";
import { BrowserRouter as Router } from "react-router-dom";
import AnimatedRoute from "./components/AnimatedRoute";

function App() {
  return (
    <Router>
      <AnimatedRoute />
    </Router>
  );
}

export default App;
