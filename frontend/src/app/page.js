import LinkedInIcebreaker from "./pages/LinkedInIcebreaker";
import TranscriptInsighter from "./pages/TranscriptInsighter";

export default function Home() {
  return (
    <main className="flex justify-around flex-wrap w-screen min-h-screen bg-gray-100 p-6">
      <TranscriptInsighter className="flex-1" />
      <LinkedInIcebreaker className="flex-1" />
    </main>
  );
}
