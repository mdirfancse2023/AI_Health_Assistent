# Render Deployment Guide

This guide walks you through deploying the AI Mental Health Assistant to Render.

## Prerequisites

- Render account (https://render.com)
- GitHub repository with this code
- OpenRouter API key
- A secure secret key for authentication

## Deployment Steps

### 1. Connect GitHub Repository

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" and select "Blueprint"
3. Connect your GitHub account
4. Select the repository containing this code

### 2. Configure Environment Variables

Before deploying, set these environment variables in Render:

#### Backend Service
- `PYTHONUNBUFFERED`: `1`
- `OPENROUTER_API_KEY`: Your OpenRouter API key
- `AUTH_SECRET_KEY`: A random 32+ character string (generate one: `openssl rand -base64 32`)
- `DATABASE_URL`: Will be auto-populated from PostgreSQL service

#### Frontend Service
- `NG_APP_API_URL`: `https://mental-health-backend.onrender.com/api` (update with your actual backend URL)

### 3. Deploy

1. Click "Deploy Blueprint"
2. Render will automatically:
   - Create a PostgreSQL database
   - Build and deploy the backend service
   - Build and deploy the frontend service
   - Set up networking between services

### 4. Post-Deployment

1. Wait for all services to finish deploying (5-10 minutes)
2. Visit your frontend URL (provided by Render)
3. The app should be fully functional

## Service Details

### Backend Service
- **Runtime**: Python 3.11
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Root Directory**: `backend`

### Frontend Service
- **Runtime**: Node 20
- **Build Command**: `npm install && npm run build`
- **Start Command**: `http-server dist/browser -p $PORT --gzip -c-1`
- **Root Directory**: `frontend`

### Database Service
- **Type**: PostgreSQL 15
- **Plan**: Free tier

## Troubleshooting

### Backend won't start
- Check that `OPENROUTER_API_KEY` and `AUTH_SECRET_KEY` are set
- Verify database connection string is correct
- Check logs in Render dashboard

### Frontend shows blank page
- Ensure `NG_APP_API_URL` points to correct backend URL
- Check browser console for CORS errors
- Verify backend is running and accessible

### Database connection issues
- Wait 2-3 minutes after database creation
- Verify `DATABASE_URL` environment variable is set
- Check that backend service can reach database

## Updating Deployment

To update your deployment:

1. Push changes to GitHub
2. Render will automatically rebuild and redeploy
3. Monitor deployment progress in Render dashboard

## Monitoring

- View logs: Click service → "Logs"
- Check metrics: Click service → "Metrics"
- Monitor database: Click database service → "Logs"

## Cost Considerations

- Free tier includes: 1 web service, 1 PostgreSQL database
- Paid plans available for production use
- Database backups available on paid plans

## Support

For issues:
1. Check Render documentation: https://render.com/docs
2. Review service logs in Render dashboard
3. Verify all environment variables are set correctly
