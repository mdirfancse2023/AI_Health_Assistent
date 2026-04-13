# 🚀 Blueprint Deployment with PostgreSQL

## Important Note About Payment

Render requires **payment information** for Blueprint deployments, even with free tier services. However, you get:
- ✅ **$5/month free credit** (enough for small apps)
- ✅ **Free PostgreSQL database** (up to 256MB)
- ✅ **Free web service** (750 hours/month)

The $1 authorization is just a hold - you won't be charged if you stay within free limits.

---

## Deployment Steps

### 1. Prepare Your Repository
```bash
git add .
git commit -m "Configure for Blueprint deployment"
git push origin main
```

### 2. Create Render Blueprint
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub account
4. Select your repository
5. Click **"Deploy Blueprint"**

### 3. Add Payment Information
- Click **"Add Card"** when prompted
- Enter your card details (temporary $1 hold)
- This enables the free tier services

### 4. Set Environment Variables
After deployment starts, add these in the Render dashboard:

**For the Web Service** (`mental-health-backend`):
- `OPENROUTER_API_KEY`: Your OpenRouter API key
- `AUTH_SECRET_KEY`: Generate with `openssl rand -base64 32`

### 5. Wait for Deployment
- **Database**: Creates PostgreSQL database (2-3 minutes)
- **Backend**: Builds and deploys (5-8 minutes)
- **Total**: 5-10 minutes

---

## What You Get

### Services Created:
- **Web Service**: `mental-health-backend` (FastAPI + Frontend)
- **Database**: `mental-health-db` (PostgreSQL)

### URLs:
- **App**: `https://mental-health-backend.onrender.com`
- **API Docs**: `https://mental-health-backend.onrender.com/docs`

### Features:
- ✅ **PostgreSQL database** (persistent data)
- ✅ **Automatic HTTPS**
- ✅ **Auto-deployment** on git push
- ✅ **Free tier within limits**

---

## Free Tier Limits

### Web Service:
- **750 hours/month** runtime
- **Auto-suspension** after 15 minutes inactivity
- **Cold starts** (30-60 seconds to wake up)

### PostgreSQL:
- **256MB storage**
- **90 days inactivity limit**
- **Automatic backups**

### Monthly Cost:
- **Web Service**: $0 (free tier)
- **PostgreSQL**: $0 (free tier)
- **Total**: $0 within limits

---

## Troubleshooting

### If Deployment Fails:
1. Check logs in Render dashboard
2. Verify `OPENROUTER_API_KEY` is set
3. Check build logs for frontend issues

### If Database Connection Fails:
1. Verify database is created
2. Check `DATABASE_URL` environment variable
3. Look at database logs

### To Avoid Payment:
- Monitor usage in Render dashboard
- Stay within free tier limits
- Delete services if not needed

---

## Alternative: No Payment Required

If you prefer **no payment information at all**, use the single-service approach:
- SQLite database (no separate database)
- Single web service
- See `README-FREE-DEPLOY.md`

---

## Ready to Deploy?

1. **Push code to GitHub**
2. **Create Blueprint on Render**
3. **Add payment info** (for free tier)
4. **Set environment variables**
5. **Deploy!** 🚀

Your AI Mental Health Assistant will be live with PostgreSQL!
