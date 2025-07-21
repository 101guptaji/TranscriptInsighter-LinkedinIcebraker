from fastapi import FastAPI
from supabase import create_client
from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel
import os
import re
from google import genai
from fastapi.middleware.cors import CORSMiddleware

# Load .env variables
load_dotenv(find_dotenv())

# Setup Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Confirm they're not None
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL or SUPABASE_KEY is not set. Check your .env file.")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


class TranscriptRequest(BaseModel):
    transcript: str

async def extract_metadata(text):
    company = re.search(r"(?:Company|Client) Name[:\-]?\s*(.*)", text)
    attendees = re.findall(r"(?:Attendees|Participants)[:\-]?\s*(.*)", text)
    date = re.search(r"(?:Date|Meeting Date)[:\-]?\s*(.*)", text)
    return {
        "company": company.group(1).strip() if company else "Unknown",
        "attendees": attendees[0].split(",") if attendees else [],
        "date": date.group(1).strip() if date else "Unknown"
    }

@app.post("/api/generate-insight")
async def generate_insight(data: TranscriptRequest):
    print("Received transcript data:", data.transcript)
    metadata = await extract_metadata(data.transcript)
    prompt = f"""You're an expert in communication and leadership coaching.
        Review the following transcript of a business discussion. Identify:
        - What was done well and why
        - What could be improved with specific reasoning
        - Actionable recommendations or experiments to try next time
        Give a concise, structured insight.
        Transcript:{data.transcript}"""

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    res = client.models.generate_content(
        model="gemini-1.5-flash", 
        contents=prompt,
    )

    print(f"Gemini API response: {res.text}")

    # Save to Supabase
    supabase.table("transcripts").insert({
        "company_name": metadata["company"],
        "attendees": metadata["attendees"],
        "date": metadata["date"],
        "transcript": data.transcript,
        "insight": res.text
    }).execute()

    return {"success": True, "insight": res.text, "metadata": metadata}