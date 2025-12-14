import React from "react";
import IncidentCard from "./IncidentCard";

export default function IncidentList({ incidents }) {
  return (
    <div className="incident-list">
      {incidents.map((id) => (
        <IncidentCard key={id} incident={id} />
      ))}
    </div>
  );
}
