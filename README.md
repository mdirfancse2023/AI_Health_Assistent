# 🧠 AI-Powered Mental Health Assistant

An intelligent, AI-driven mental health assistant designed to support students by providing emotional insights, personalized responses, and analytics-based mental health tracking.

---

## 🚀 Project Overview

This project aims to leverage Artificial Intelligence and Data Science to assist students in managing their mental well-being. The system analyzes user inputs, detects emotional states, and provides empathetic responses using Large Language Models (LLMs).

In addition, the system tracks user interactions and visualizes emotional trends through a dashboard, enabling better awareness and decision-making.

---

## 🎯 Objectives

* Develop an AI-based chatbot for mental health support
* Implement emotion detection using machine learning techniques
* Provide personalized responses using LLMs
* Track and analyze user emotional patterns
* Visualize insights through an interactive dashboard
* Evaluate impact on student well-being and productivity

---

## 🏗️ System Architecture

```
Frontend (Angular)
        ↓
Backend (FastAPI)
        ↓
ML Layer (Emotion Detection + LLM)
        ↓
Database (PostgreSQL)
```

---

## 🧩 Features

### 💬 AI Chatbot

* Real-time conversation with users
* Emotion-aware responses
* Integrated with LLM (via OpenRouter API)

### 🧠 Emotion Detection

* Detects emotions like stress, sadness, neutral
* Enhances response personalization

### 📊 Dashboard Analytics

* Emotion distribution (Pie Chart)
* Chat activity trend (Line Chart)
* Visual insights for mental health tracking

### 🗂️ Data Storage

* Stores chat history
* Tracks user interactions
* Enables future personalization

### 🎨 Modern UI

* Responsive Angular frontend
* Clean navigation (Chat + Dashboard)
* Styled components with professional layout

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

* Transformers
* Torch
* OpenRouter API (LLM integration)

### 🔹 Database

* PostgreSQL

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/AI_Powered_Mental_Health_Assistent.git
cd AI_Powered_Mental_Health_Assistent
```

---

### 2️⃣ Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
```

Create `.env` file:

```
OPENROUTER_API_KEY=your_api_key
DATABASE_URL=postgresql://username:password@localhost:5432/dbname
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

---

## 📈 Future Enhancements

* User authentication system
* Advanced emotion detection models
* Recommendation engine (coping strategies)
* PDF report generation
* Dark mode UI
* Mobile responsiveness

---

## 🎓 Academic Relevance (MBA Data Science)

This project demonstrates:

* Application of AI in real-world problems
* Data-driven decision-making
* User behavior analytics
* Integration of ML with full-stack systems

---

## 📌 Conclusion

The AI-Powered Mental Health Assistant provides a scalable, intelligent solution for student well-being by combining AI, analytics, and user-centric design.

---

## 👨‍💻 Author

**Md Irfan**
MBA (Data Science)
Software Developer | AI Enthusiast

---

## ⭐ If you like this project

Give it a ⭐ on GitHub and share your feedback!
