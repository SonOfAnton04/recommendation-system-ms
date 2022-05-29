import "./App.css";
import Nav from "./Nav.js";
import DashboardItem from "./Dashboard-item.js";
import DashboardUser from "./Dashboard-user";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Dashboard from "./Dashboard";

function App() {
  return (
    <Router>
      <div className="App">
        <Nav />
        <Routes>
          <Route exact path="/" element={<Dashboard />}></Route>
          <Route exact path="/" element={<DashboardItem />}></Route>
          <Route exact path="/about" element={<DashboardUser />}></Route>
        </Routes>
      </div>
    </Router>
  );
}

export default App;
