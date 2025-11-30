import React, { useState } from "react";
import { generateIncident } from "../api/api";

export default function GeneratePage() {
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState(null);

  const handleGenerate = async () => {
    const res = await generateIncident(prompt);
    setResult(res.image_path);
  };

  return (
    <div>
      <h1>Generate Incident</h1>
      <input
        type="text"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Enter issue description"
      />
      <button onClick={handleGenerate}>Generate</button>
      {result && <img src={result} alt="Generated" />}
    </div>
  );
}
