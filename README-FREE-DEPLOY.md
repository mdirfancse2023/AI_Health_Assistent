# 🆓 Completely Free Deployment Guide

## Option 1: Render (Single Service - No Payment Required)

Your project is now configured for **completely free** deployment on Render!

### Steps:
1. **Push to GitHub**: Make sure your code is on GitHub
2. **Go to Render**: https://render.com
3. **Create Web Service** (NOT Blueprint):
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository
   - Use these settings:
     - **Name**: mental-health-app
     - **Runtime**: Python
     - **Root Directory**: backend
     - **Build Command**: `./build.sh && pip install -r requirements.txt`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. **Environment Variables**:
   - `DATABASE_URL`: `sqlite:///./mental_health.db`
   - `OPENROUTER_API_KEY`: Your OpenRouter API key
   - `AUTH_SECRET_KEY`: Generate with `openssl rand -base64 32`
5. **Deploy**: Click "Create Web Service"

### What You Get:
- ✅ **Single service** (no payment required)
- ✅ **SQLite database** (no separate database needed)
- ✅ **Frontend + Backend** served together
- ✅ **Free tier**: 750 hours/month

### URL: `https://your-app-name.onrender.com`

---

## Option 2: Vercel + Railway (Alternative Free Stack)

### Frontend on Vercel:
```bash
# Deploy frontend to Vercel
cd frontend
npm install -g vercel
vercel --prod
```

### Backend on Railway:
```bash
# Deploy backend to Railway
cd backend
railway login
railway init
railway up
```

---

## Option 3: GitHub Pages + PythonAnywhere

### Frontend on GitHub Pages:
1. Push frontend to `gh-pages` branch
2. Enable GitHub Pages in repository settings

### Backend on PythonAnywhere:
1. Create free account on pythonanywhere.com
2. Upload backend files
3. Configure web app

---

## Why This Works

The key changes made:
- **Single service** instead of multiple services
- **SQLite** instead of PostgreSQL (no separate database)
- **Static file serving** from backend
- **No payment requirement** for single web service

## Free Tier Limitations

- **Render**: 750 hours/month, auto-suspension after 15min inactivity
- **Vercel**: Unlimited static hosting
- **Railway**: $5 credit monthly (enough for small apps)

Choose **Option 1** for the simplest completely free deployment!
