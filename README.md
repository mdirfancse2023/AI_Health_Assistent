# 🧠 AI-Powered Mental Health Assistent

An intelligent, AI-driven mental health assistant designed to support students by providing emotional insights, personalized responses, and analytics-based mental health tracking. Built as a Capstone/MBA Data Science project demonstrating end-to-end Machine Learning, NLP, and Full-Stack capability.

---

## 📋 Quick Start

**Run or access the project quickly:**

1. **Local full stack**: `docker-compose up`
2. **Frontend local dev**: `cd frontend && npm install && ng serve`
3. **Backend local dev**: `cd backend && pip install -r requirements.txt && uvicorn main:app --reload`
4. **Cloud deployment guide**: See [GUIDE.md](GUIDE.md)

Current deployed URL:

```text
https://app.136.115.35.202.sslip.io/
```

The complete GKE setup and deployment flow is documented in [GUIDE.md](GUIDE.md).

---

## 🚀 Project Overview

This project aims to leverage Artificial Intelligence and Data Science to assist students in managing their mental well-being. The system analyzes user inputs, detects emotional states, and provides empathetic responses using Large Language Models (LLMs) via OpenRouter.

In addition, the system tracks user interactions and visualizes emotional trends through a dashboard, enabling better awareness and decision-making. 

---

## 🎯 Objectives

* Develop an AI-based chatbot for mental health support
* Implement emotion detection using machine learning techniques (Hugging Face)
* Provide personalized responses using LLMs
* Track and analyze user emotional patterns
* Visualize insights through an interactive dashboard
* Evaluate impact on student well-being and productivity

---

## 🏗️ System Architecture

```
Frontend (Angular 21 + Glassmorphism UI)
        ↓
Backend (FastAPI)
        ↓
ML Layer:
 ├── Emotion Detection: Hugging Face (distilbert-base-uncased-emotion)
 ├── RAG Vector Search: Hugging Face (all-MiniLM-L6-v2) + PyTorch
 └── LLM Generation: OpenRouter API (openai/gpt-3.5-turbo)
        ↓
Database (PostgreSQL)
```

---

## 🧩 Features

### 💬 AI Chatbot

* Real-time conversation with users
* Emotion-aware responses 
* Integrated with LLM (via OpenRouter API - utilizing openai/gpt-3.5-turbo model)

### 🧠 Emotion Detection

* Detects emotions like stress, sadness, neutral using local NLP models.
* Enhances response personalization dynamically.

### 📚 Retrieval-Augmented Generation (RAG)
* Built a custom, zero-dependency Vector Engine using PyTorch.
* Computes dense 384-dimensional tensor embeddings locally for over 130+ academic coping mechanisms.
* Utilizes Cosine Similarity to fetch empirical coping strategies based on query meaning.

### 📊 Dashboard Analytics

* Emotion distribution (Pie Chart)
* Chat activity trend (Line Chart)
* Evaluates AI Effectiveness via user feedback tracking.
* Visual insights for Mental Health tracking (Stress vs. Academic Focus)

### 🔐 Authentication & User Accounts

* Login and signup flow backed by FastAPI + PostgreSQL
* Chats, dashboard data, feedback, and check-ins are tied to the logged-in user
* Bearer-token based frontend session handling
* Protected Chat and Dashboard routes

### 🗂️ Data Storage

* Stores chat history
* Tracks user longitudinal interactions
* Enables future personalization

### 🎨 Modern UI

* Responsive Angular frontend built with Glassmorphism 
* Fully functional Dark Mode/Light Mode toggle
* Clean navigation with Login / Sign Up in navbar for guests
* Inline form validation on invalid auth input
* Clean navigation (Chat + Dashboard) for authenticated users
* Styled components with professional layout and structured ChatGPT-style markdown rendering.

---

## 🛠️ Tech Stack

### 🔹 Frontend

* Angular (Standalone Components)
* TypeScript
* Chart.js (Data Visualization)

### 🔹 Backend

* FastAPI
* Python
* SQLAlchemy (ORM)

### 🔹 AI / ML

* Transformers (Hugging Face Models)
* Torch (PyTorch Cosine Similarity)
* OpenRouter API (LLM integration: openai/gpt-3.5-turbo)

### 🔹 Database

* PostgreSQL

### 🔹 DevOps / Quality

* Docker + Docker Hub
* Kubernetes (GKE Autopilot)
* GitHub Actions CI/CD
* JetBrains Qodana (backend community scan, optional cloud dashboard upload)

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/mdirfancse2023/AI_Health_Assistent.git AI_Powered_Mental_Health_Assistent
cd AI_Powered_Mental_Health_Assistent
```

---

### 2️⃣ Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
python3 -m pip install markdown
```

Create `.env` file:

```
OPENROUTER_API_KEY=your_api_key
DATABASE_URL=postgresql://username:password@localhost:5432/dbname
AUTH_SECRET_KEY=replace_with_a_long_random_secret
```

Run backend:

```bash
uvicorn main:app --reload
```

---

### 3️⃣ Frontend Setup

```bash
cd frontend
npm install
ng serve
```

Access app:

```
http://localhost:4200
```

---

## 🔌 API Endpoints

### Authentication API

```
POST /auth/signup
POST /auth/login
GET /auth/me
```

### Chat API

```
POST /chat
```

Request:

```json
{
  "message": "I feel stressed"
}
```

Response:

```json
{
  "emotion": "stress",
  "response": "I'm here for you..."
}
```

---

### Analytics APIs

```
GET /analytics/emotions
GET /analytics/trend
GET /analytics/effectiveness
GET /analytics/stress_academic
```

### Daily Check-In API

```
POST /daily-checkin
```

---

## 📊 Dashboard Insights

* Emotion distribution across user conversations
* Daily chat trends
* Behavioral patterns 

---

## 🧠 Personalization & Memory

* Stores previous interactions
* Enables context-aware responses
* Improves AI understanding over time

---

## 🧪 Testing

* API tested using Swagger UI and cURL
* Frontend tested with Angular dev server
* Database verified via PostgreSQL logs
* Auto-deploy configured through GitHub Actions to GKE
* Qodana workflow added for backend static analysis

---

## 🚢 Deployment & CI

### GitHub Actions Deployment

The repo includes:

* [deploy.yml](.github/workflows/deploy.yml) for Docker build, push, and GKE deployment
* Workload Identity Federation for keyless GitHub Actions authentication to Google Cloud
* Immutable image rollout using `github.sha` tags during deployment

Required GitHub secrets:

* `DOCKER_PASSWORD`
* `OPENROUTER_API_KEY`

### Qodana

The repo also includes:

* [qodana.yml](.github/workflows/qodana.yml)
* [qodana.yaml](qodana.yaml)

This setup currently keeps Qodana simple by scanning the Python backend with `qodana-python-community`.

If you want Qodana Cloud dashboard uploads, add the GitHub secret:

* `QODANA_TOKEN`

This must be the Qodana **project token** used for dashboard uploads.

---

## 📈 Future Enhancements

* Advanced emotion detection models
* Recommendation engine (coping strategies)
* PDF report generation
* Mobile responsiveness improvements
* Role-based admin / counselor views

---

## 🎓 Academic Relevance (MBA Data Science)

This project demonstrates:

* Application of AI in real-world problems
* Data-driven decision-making
* User behavior analytics
* Integration of ML with full-stack systems

---

## 📌 Conclusion

The AI-Powered Mental Health Assistent provides a scalable, intelligent solution for student well-being by combining AI, analytics, and user-centric design.

---

## 👨‍💻 Author

**Md Irfan**
MBA (Data Science)
Software Developer | AI Enthusiast

---

## ⭐ If you like this project

Give it a ⭐ on GitHub and share your feedback!
