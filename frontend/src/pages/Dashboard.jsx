import React, { useEffect, useState } from "react";
import Navbar from "../components/Navbar.jsx";
import IncidentList from "../components/IncidentList";
import { fetchIncidents } from "../api/api";

export default function Dashboard() {
  const [incidents, setIncidents] = useState([]);

  useEffect(() => {
    loadIncidents();
  }, []);

  async function loadIncidents() {
    try {
      const data = await fetchIncidents(); 
      setIncidents(data);
    } catch (err) {
      console.error("Error loading incidents:", err);
    }
  }

  return (
    <div>
      <Navbar />
      <h1 style={{ padding: "20px" }}>Incident Dashboard</h1>
      <IncidentList incidents={incidents} />
    </div>
  );
}
