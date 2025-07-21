"use client";

export default function IceBreakerFeed({ icebreaker }) {
    return (
        <div className="p-4 space-y-6">
            {icebreaker && (
                <div className="bg-white p-4 rounded shadow">
                    <h2 className="text-2xl font-bold">LinkedIn Icebreaker</h2>
                    <div className="p-4 border rounded shadow">
                        <pre className="whitespace-pre-wrap"><strong>Icebreaker:</strong> {icebreaker}</pre>
                    </div>
                </div>
            )}

        </div>
    );
}