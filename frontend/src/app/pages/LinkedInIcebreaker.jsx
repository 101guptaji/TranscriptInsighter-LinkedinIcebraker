"use client";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import IceBreakerFeed from "../components/IcebreakerFeed";

const LinkedInIcebreaker = () => {
    const [linkedInBio, setLinkedInBio] = useState("");
    const [pitchDeck, setPitchDeck] = useState("");
    const [icebreaker, setIcebreaker] = useState(null);
    const [loading, setLoading] = useState(false);

    async function handleSubmit() {
        if (!linkedInBio || !pitchDeck) {
            alert("Please fill in both fields.");
            return;
        }
        console.log("Submitting LinkedIn bio:", linkedInBio);
        console.log("Submitting pitch deck:", pitchDeck);

        try {
            setLoading(true);
            setIcebreaker(null);
            const res = await fetch("http://127.0.0.1:8000/api/generate-icebreaker", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ linkedInBio, pitchDeck }),
            });
            const data = await res.json();
            console.log("API response:", data);

            setIcebreaker(data.icebreaker);
            setLinkedInBio("");
            setPitchDeck("");
            setLoading(false);
        } catch (error) {
            console.error("Error fetching icebreaker:", error);
            setLoading(false);
            alert("Failed to generate icebreaker. Please try again.");
        }
    }

    return (
        <div className="max-w-1/2 mx-auto p-6 bg-white rounded shadow">
            <h1 className="text-3xl font-bold text-center mb-6">
                LinkedIn Icebreaker
            </h1>
            <div className="p-4 max-w-xl mx-auto space-y-4">
                <textarea
                    value={linkedInBio}
                    onChange={(e) => setLinkedInBio(e.target.value)}
                    placeholder="Paste your LinkedIn bio here"
                    className="w-full h-40 p-2 border rounded"
                />
                <textarea
                    value={pitchDeck}
                    onChange={(e) => setPitchDeck(e.target.value)}
                    placeholder="Paste your pitch deck content here"
                    className="w-full h-40 p-2 border rounded"
                />
                <Button onClick={handleSubmit} disabled={loading}>
                    {loading ? "Analyzing..." : "Get Icebreaker"}
                </Button>
            </div>

            {icebreaker && <IceBreakerFeed icebreaker={icebreaker} />}
        </div>

    );
}

export default LinkedInIcebreaker