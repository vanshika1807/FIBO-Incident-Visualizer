import React from "react";
import { Link } from "react-router-dom";

export default function IncidentCard({ incident }) {
  return (
    <Link to={`/incident/${incident}`} className="card">
      <div>{incident}</div>
    </Link>
  );
}
