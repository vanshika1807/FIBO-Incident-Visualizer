import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export const fetchIncidents = async () => {
  const res = await axios.get(`${API_URL}/incidents`);
  return res.data.incidents;
};

export const fetchIncident = async (id) => {
  const res = await axios.get(`${API_URL}/incidents/${id}`);
  return res.data;
};

export const fetchIncidentImage = (id) => `${API_URL}/incidents/${id}/image`;

export const generateIncident = async (prompt) => {
  const res = await axios.post(`${API_URL}/generate`, { prompt });
  return res.data;
};
