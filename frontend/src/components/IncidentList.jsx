import React, { useEffect, useState } from "react";
import { fetchIncidents } from "../api/api";
import IncidentCard from "./IncidentCard";

export default function IncidentList() {
  const [incidents, setIncidents] = useState([]);

  useEffect(() => {
    fetchIncidents().then(setIncidents);
  }, []);

  return (
    <div className="incident-list">
      {incidents.map((id) => (
        <IncidentCard key={id} incident={id} />
      ))}
    </div>
  );
}
