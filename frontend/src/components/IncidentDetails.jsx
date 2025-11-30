import React, { useEffect, useState } from "react";
import { fetchIncident, fetchIncidentImage } from "../api/api";

export default function IncidentDetails({ id }) {
  const [metadata, setMetadata] = useState(null);
  const [imageUrl, setImageUrl] = useState("");

  useEffect(() => {
    fetchIncident(id).then(setMetadata);
    setImageUrl(fetchIncidentImage(id));
  }, [id]);

  if (!metadata) return <div>Loading...</div>;

  return (
    <div>
      <h2>Incident: {id}</h2>
      <pre>{JSON.stringify(metadata, null, 2)}</pre>
      <img src={imageUrl} alt="Incident" style={{ maxWidth: "600px" }} />
    </div>
  );
}
