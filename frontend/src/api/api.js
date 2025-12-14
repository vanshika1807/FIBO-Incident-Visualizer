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

export const generateIncident = async (payload) => {
  // payload should be an object like { prompt: "..." }
  const response = await axios.post(`${API_URL}/generate`, payload, {
    headers: {
      "Content-Type": "application/json"
    }
  });
  return response.data;
};
