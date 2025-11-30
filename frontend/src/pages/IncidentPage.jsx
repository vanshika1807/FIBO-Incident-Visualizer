import React from "react";
import { useParams } from "react-router-dom";
import IncidentDetails from "../components/IncidentDetails";

export default function IncidentPage() {
  const { id } = useParams();
  return <IncidentDetails id={id} />;
}
