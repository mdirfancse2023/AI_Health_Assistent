# Deploy to Render

## Quick Deploy to Render

### Option 1: One-Click Deploy
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/your-username/your-repo)

### Option 2: Manual Deployment

1. **Create a Render account** at [render.com](https://render.com)

2. **Create a new Blueprint**:
   - Go to Render Dashboard
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will detect the `render.yaml` file

3. **Set environment variables**:
   - `OPENROUTER_API_KEY`: Your OpenRouter API key
   - `AUTH_SECRET_KEY`: Generate with: `openssl rand -base64 32`

4. **Deploy**:
   - Click "Apply" to deploy all services
   - Wait for all services to be "Live"

### Environment Variables

Set these in Render dashboard:

1. **Backend Service**:
   - `OPENROUTER_API_KEY`: Your OpenRouter API key
   - `AUTH_SECRET_KEY`: Random 32+ character string
   - `DATABASE_URL`: Auto-set by Render

2. **Frontend Service**:
   - `NG_APP_API_URL`: Auto-set to backend URL

### Services Created
- **Backend**: FastAPI application
- **Frontend**: Angular application  
- **Database**: PostgreSQL database

### URLs After Deployment
- Frontend: `https://mental-health-frontend.onrender.com`
- Backend API: `https://mental-health-backend.onrender.com`
- API Documentation: `https://mental-health-backend.onrender.com/docs`

### Troubleshooting
- Check logs in Render dashboard
- Verify environment variables are set
- Check database connection in logs
- Verify API keys are correct

### Support
For issues, check Render's documentation or contact support.