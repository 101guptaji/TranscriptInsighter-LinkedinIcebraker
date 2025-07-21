"use client";

export default function Feed({ insight, metadata }) {
    return (
        <div className="p-4 space-y-6">
            {insight && (
                <div className="bg-white p-4 rounded shadow">
                    <h2 className="text-2xl font-bold">Transcript Insight</h2>
                    <div className="p-4 border rounded shadow">
                        {metadata && (
                            <div className="mb-4">
                                <p><strong>Company:</strong> {metadata.company}</p>
                                <p><strong>Attendees:</strong> {metadata.attendees.join(", ")}</p>
                                <p><strong>Date:</strong> {metadata.date}</p>
                            </div>
                        )}

                        <p><strong>Insight:</strong> {insight}</p>
                    </div>
                </div>
            )}

        </div>
    );
}
