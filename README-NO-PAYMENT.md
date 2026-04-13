# 🆓 Deploy Without Payment Information

You're absolutely right! You can deploy completely free without payment info - just like your portfolio.

## Why This Works

- **Single web service** (no Blueprint)
- **SQLite database** (no separate database)
- **No payment information required**
- **Same as your portfolio deployment**

---

## Step-by-Step Deployment

### 1. Push to GitHub
```bash
git add .
git commit -m "Configure for free deployment"
git push origin main
```

### 2. Create Web Service (NOT Blueprint)
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account
4. Select your repository
5. **Important**: Choose these settings:

#### Basic Settings:
- **Name**: `mental-health-app`
- **Region**: Default (closest to you)
- **Branch**: `main`

#### Build Settings:
- **Runtime**: `Python`
- **Root Directory**: `backend`
- **Build Command**: `./build.sh && pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

#### Advanced Settings:
- **Instance Type**: `Free` (default)

### 3. Add Environment Variables
Click "Environment" tab and add:
- `DATABASE_URL`: `sqlite:///./mental_health.db`
- `OPENROUTER_API_KEY`: Your OpenRouter API key
- `AUTH_SECRET_KEY`: Generate with `openssl rand -base64 32`
- `PYTHONUNBUFFERED`: `1`

### 4. Deploy!
Click **"Create Web Service"**

**No payment information required!** 🎉

---

## What You Get

### Free Tier Features:
- ✅ **750 hours/month** runtime
- ✅ **SQLite database** (persistent storage)
- ✅ **Frontend + Backend** combined
- ✅ **Automatic HTTPS**
- ✅ **Custom URL**: `https://mental-health-app.onrender.com`

### Limitations:
- Auto-suspension after 15 minutes inactivity
- Cold start (30-60 seconds to wake up)
- Perfect for personal projects and demos

---

## URLs After Deployment

- **Main App**: `https://mental-health-app.onrender.com`
- **API Docs**: `https://mental-health-app.onrender.com/docs`
- **API Endpoints**: `https://mental-health-app.onrender.com/api/*`

---

## Troubleshooting

### If Build Fails:
1. Check the build logs in Render dashboard
2. Make sure `build.sh` is executable
3. Verify frontend builds correctly

### If App Doesn't Start:
1. Check the service logs
2. Verify environment variables are set
3. Check database connection in logs

### To Update:
```bash
git add .
git commit -m "Update"
git push
# Render auto-redeploys!
```

---

## Comparison with Your Portfolio

| Feature | Your Portfolio | Mental Health App |
|---------|----------------|-------------------|
| Payment Info | ❌ Not Required | ❌ Not Required |
| Database | None | SQLite (free) |
| Frontend | Static | Angular + API |
| Backend | None | FastAPI |
| Deployment | Single Service | Single Service |

**Same deployment method, just with backend functionality!**

---

## Ready to Deploy?

1. **Push code to GitHub** ✅
2. **Create Web Service** (NOT Blueprint) ✅
3. **Add environment variables** ✅
4. **Deploy for FREE** 🚀

Your AI Mental Health Assistant will be live without any payment information - just like your portfolio!
