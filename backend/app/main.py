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

# Transcript request model
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

# LinkedIn Icebreaker 
class LinkedInIcebreaker(BaseModel):
    linkedInBio: str
    pitchDeck: object = None

@app.post("/api/generate-icebreaker")
async def generate_icebreaker(data: LinkedInIcebreaker):
    # print("Received LinkedIn bio:", data.linkedInBio)
    # print("Received pitch deck: ", data.pitchDeck)
    prompt = f"""You are an expert in crafting personalized LinkedIn icebreakers.
        Based on the following LinkedIn bio of a person and the pitch deck of our company: 
        1. Identify the LinkedIn profile's company and fetch:
        - Their official LinkedIn page
        - Their website URL
        2. From the pitch deck, extract and list:
        - Buying signals relevant to this person
        - Why each signal matters
        - Source of each signal (deck slide, metric, value prop, etc.)
        - Discovery triggers you noticed
        - Smart questions to ask in the next meeting
        3. Provide insights at two levels:
        - Company level (goals, pain points, buying readiness)
        - Role level (motivations, decision criteria, job pressures)
        4. Analyze their preferred buying style (e.g., analytical, visionary, price-sensitive, consensus-based) and explain how you inferred it.
        5. Give a 1-paragraph summary of:
        - What matters most to this person
        - How we should position ourselves in the next interaction
        6. Suggest 3 reflection questions for me to think about before engaging.
        7. Finally, from their perspective:
        - List Top 5 things they would find valuable in our deck
        - Identify what parts might be unclear, irrelevant, or weak, and explain why
        - Recommend how we can improve or reposition those parts

        Bio: {data.linkedInBio}"""

    if data.pitchDeck:
        prompt += f"\nPitch Deck: {data.pitchDeck}"

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    res = client.models.generate_content(
        model="gemini-1.5-flash", 
        contents=prompt,
    )

    # print(f"Gemini API response: {res.text}")

    return {"success": True, "icebreaker": res.text}