import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import IncidentPage from "./pages/IncidentPage";
import GeneratePage from "./pages/GeneratePage";

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/incident/:id" element={<IncidentPage />} />
        <Route path="/generate" element={<GeneratePage />} />
      </Routes>
    </Router>
  );
}
