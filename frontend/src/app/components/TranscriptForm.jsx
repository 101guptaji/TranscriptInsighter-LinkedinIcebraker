"use client";
import { useState } from "react";
import { Button } from "@/components/ui/button";

export default function TranscriptForm({ setInsight, setMetadata }) {
  const [transcript, setTranscript] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit() {
    console.log("Submitting transcript:", transcript);

    setLoading(true);
    const res = await fetch("http://127.0.0.1:8000/api/generate-insight", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ transcript }),
    });
    const data = await res.json();
    console.log("API response:", data);
    
    setInsight(data.insight);
    setMetadata(data.metadata);
    setTranscript("");
    setLoading(false);
  }

  return (
    <div className="p-4 max-w-xl mx-auto space-y-4">
      <textarea
        value={transcript}
        onChange={(e) => setTranscript(e.target.value)}
        placeholder="Paste your transcript here"
        className="w-full h-40 p-2 border rounded"
      />
      <Button onClick={handleSubmit} disabled={loading}>
        {loading ? "Analyzing..." : "Get Insight"}
      </Button>
    </div>
  );
}
