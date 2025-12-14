import React, { useState } from "react";
import Navbar from "../components/Navbar";
import { generateIncident } from "../api/api";

export default function GeneratePage() {
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleGenerate() {
    if (!prompt.trim()) return;

    setLoading(true);
    setError("");
    setResponse(null);

    try {
      const data = await generateIncident({ prompt });
      setResponse(data);
    } catch (err) {
      console.error(err);
      setError("Failed to generate incident. Check console for details.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <Navbar />
      <h2 style={{ padding: "20px" }}>Generate Manual Incident</h2>

      <input
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Enter something..."
        style={{
          padding: "10px",
          width: "60%",
          fontSize: "16px"
        }}
      />

      <button
        onClick={handleGenerate}
        disabled={loading}
        style={{
          marginLeft: "10px",
          padding: "10px 20px",
          fontSize: "16px",
          cursor: loading ? "not-allowed" : "pointer"
        }}
      >
        {loading ? "Generating..." : "Generate"}
      </button>

      {error && <p style={{ color: "red", marginTop: "10px" }}>{error}</p>}

      {response && (
        <div style={{ marginTop: "20px" }}>
          {/* Display JSON response */}
          <pre style={{ padding: "20px", background: "#eee" }}>
            {JSON.stringify(response, null, 2)}
          </pre>

          {/* Display generated image */}
          {response.image_path && (
            <div style={{ marginTop: "20px" }}>
              <h3>Generated Image:</h3>
              <img
                src={`http://127.0.0.1:8000${response.image_path}`}
                alt="Generated Incident"
                style={{ maxWidth: "100%", borderRadius: "8px", border: "1px solid #ccc" }}
              />
            </div>
          )}
        </div>
      )}
    </div>
  );
}
