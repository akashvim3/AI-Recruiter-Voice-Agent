# 🤖 AI Recruiter Voice Agent

[![License](https://img.shields.io/github/license/yourusername/ai-recruiter-voice-agent)](LICENSE)
[![Build](https://img.shields.io/github/actions/workflow/status/yourusername/ai-recruiter-voice-agent/build.yml)](https://github.com/yourusername/ai-recruiter-voice-agent/actions)
[![Issues](https://img.shields.io/github/issues/yourusername/ai-recruiter-voice-agent)](https://github.com/yourusername/ai-recruiter-voice-agent/issues)
[![Stars](https://img.shields.io/github/stars/yourusername/ai-recruiter-voice-agent)](https://github.com/yourusername/ai-recruiter-voice-agent/stargazers)
[![Forks](https://img.shields.io/github/forks/yourusername/ai-recruiter-voice-agent)](https://github.com/yourusername/ai-recruiter-voice-agent/network/members)

> 💼 Conversational AI agent for recruiters: Voice-based, intelligent, and fully automated candidate screening powered by Django & React.

---

## 🧠 Features

- 🗣️ Natural, real-time voice conversations with candidates
- 📋 Customizable screening scripts and interview logic
- 📊 Candidate evaluation and scoring
- 📨 Notifications and report generation
- 🌍 Multi-language and accent support
- 🔗 API integration with ATS platforms
- 🖥️ Admin dashboard to review interviews and results

---

## 🛠️ Tech Stack

### Frontend (🎨 React)
- React 18
- Tailwind CSS
- Axios for API communication
- Web Audio API for microphone access

### Backend (🧩 Django)
- Django 4+
- Django REST Framework
- PostgreSQL / SQLite
- OpenAI (for NLP logic)
- Whisper / DeepSpeech (for STT)
- ElevenLabs / Google TTS

---

## Features

- 🎤 Voice-based candidate screening and interviews
- 🤖 AI-powered job matching
- 📊 Real-time analytics dashboard
- 💬 Interactive voice interface
- 🔍 Advanced candidate search
- 📅 Interview scheduling
- 📱 Responsive design

## Tech Stack

- **Frontend**: Next.js, React, Tailwind CSS
- **Backend**: Django REST Framework
- **Voice Integration**: Vapi
- **Database**: Supabase
- **Authentication**: JWT, OAuth2
- **Deployment**: Docker, AWS

## Getting Started

### Prerequisites

- Node.js (v18+)
- Python (v3.9+)
- Docker
- Supabase account
- Vapi API key

### Installation

1. Clone the repository
```bash
git clone [ https://github.com/akashvim3/AI-Recruiter-Voice-Agent.git]
```

2. Install frontend dependencies
```bash
cd frontend
npm install
```

3. Install backend dependencies
```bash
cd backend
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp .env.example .env
```

5. Start the development servers
```bash
# Frontend
cd frontend
npm run dev

# Backend
cd backend
python manage.py runserver
```

## Project Structure

```
ai-recruiter/
├── frontend/           # Next.js frontend
├── backend/           # Django backend
├── docker/           # Docker configuration
└── docs/            # Documentation
```
🔐 Environment Variables

Create a .env file in both backend/ and frontend/ folders.
Backend .env.example
      DEBUG=True
      SECRET_KEY=your-secret-key
      OPENAI_API_KEY=your-openai-key
      TTS_PROVIDER=elevenlabs
      STT_PROVIDER=whisper
      ALLOWED_HOSTS=localhost,127.0.0.1
      
🔌 API Endpoints

Method | Endpoint | Description
GET | /api/interviews/ | List all interviews
POST | /api/interviews/ | Start a new interview session
GET | /api/interviews/:id/ | Get interview details
POST | /api/transcribe/ | Upload audio for STT
POST | /api/respond/ | Get AI response from LLM

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

🌟 Show Your Support

If this project helped you, please ⭐ the repo and share it with others!
 
---

Let me know if you want:

- A **custom project logo** or banner
- Auto-generated `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, or CI/CD GitHub Actions
- Docker setup for simplified deployment
- ATS integration examples (Greenhouse, Lever, etc.)

Happy building! 🚀


This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details. 
