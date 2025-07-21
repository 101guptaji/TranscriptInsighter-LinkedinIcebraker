# MVP – Transcript Insight & LinkedIn Icebreaker
    - A minimal viable product that helps users:
    - Analyze meeting transcripts and generate actionable insights
    - Generate personalized, AI-powered LinkedIn cold outreach icebreakers

## Tech Stack
Frontend:	Next.js, TailwindCSS, Shadcn UI
Backend:	FastAPI
Database:	Supabase
AI:	OpenAI / Gemini
Deployment:	Vercel (Frontend), Render(Backend)

## Features
1. Transcript Insight
        Paste a meeting transcript

        Enter metadata: Company name, Attendees, Date

        Get AI-generated:

        What you did well

        How you can improve

        Suggestions for next time

        Stored and retrieved via Supabase

2. LinkedIn Icebreaker
        Paste a LinkedIn bio and optional pitch deck

        Get cold outreach insights and discovery questions

        Stored using Supabase

        Results displayed in a feed-style layout

## Project Structure
    root/
    ├── frontend/     # Next.js app (UI) 
    ├── backend/      # FastAPI app (API + Supabase)
    ├── README.md     # This file

## Setup Instructions
🖥️ Frontend (Next.js)
    1. Navigate to frontend/ and install dependencies:
        cd frontend
        npm install
    2. Set up environment variables in .env.local:
        NEXT_PUBLIC_SUPABASE_URL=https://yourproject.supabase.co
        NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
        NEXT_PUBLIC_API_URL=http://localhost:8000
    3. Run the development server:
        npm run dev
        Open http://localhost:3000 to view the app.

🔌 Backend (FastAPI)
    1. Navigate to backend/ and create a Python virtual environment:
        cd backend
        python -m venv venv
        source venv/bin/activate  # Windows: venv\Scripts\activate
        pip install -r requirements.txt
    2. Create a .env file:
        SUPABASE_URL=https://yourproject.supabase.co
        SUPABASE_KEY=your-service-role-key
        OPENAI_API_KEY=your-openai-key  # optional
    3. Start the FastAPI server:
        uvicorn main:app --reload --port 8000
        Server will run at: http://localhost:8000

🗃️ Supabase Schema
    1. transcripts
        Field	Type
        id	UUID (PK)
        company_name	text
        attendees	text
        date	text
        transcript	text
        insight	text
        created_at	timestamptz (default: now())

📸 Screenshots
