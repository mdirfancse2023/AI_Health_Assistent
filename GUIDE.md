# Complete Deployment Guide

---

## ⚡ FAST-TRACK: Reusing Your codexa-ai Infrastructure

**Since you already have:**
- ✅ GCP project with billing
- ✅ GKE cluster experience + NGINX Ingress + Let's Encrypt setup
- ✅ Docker Hub account
- ✅ GitHub Actions configured

**You only need (25 minutes):**

1. **Step 1**: Test locally with docker-compose (5 min) - just verify it works
2. **Step 4**: Create NEW cluster with setup.sh (10 min) - separate from codexa-ai
   ```bash
   ./setup.sh
   # Answer: Same GCP project ID
   # Answer: New cluster name (e.g., mental-health-cluster)
   ```
3. **Step 5**: Add GitHub Secrets (5 min) - if using same account, use same values
4. **Step 6**: Update k8s/app.yaml with new cluster IP (2 min)
5. **Step 7**: Deploy via git push (5 min)

**Result**: Mental Health Assistant running at `https://app.{NEW_IP}.sslip.io`

👉 **Start at Step 1 below** (skip 2 & 3)

---

## Prerequisites

### Install Required Tools
```bash
# macOS
brew install gcloud-sdk kubectl helm docker git

# Verify
gcloud --version && kubectl version --client && helm version && docker --version
```

### ⚠️ Security Note
**DO NOT commit your `.env` file with secrets to GitHub!**

```bash
# .env file should ONLY be used for LOCAL development
# Never push to GitHub

# .gitignore should contain:
.env                  # Your local secrets file

# Use GitHub Secrets (Step 5) for cloud deployment instead
```

---

## Step 1: Local Testing (5 minutes)

### 1.1 Start Services Locally
```bash
cd /Users/macbook/Documents/GitHub/AI_Powered_Mental_Health_Assistent

# Start all services
docker-compose up

# Wait 2-3 minutes for services to start
```

### 1.2 Test Services
Open browser:
- Frontend: http://localhost
- Backend API: http://localhost:8000/docs
- Home: http://localhost:8000

### 1.3 Verify Database
```bash
# Open new terminal
docker exec -it ai_powered_mental_health_assistent_db_1 psql -U postgres -d mental_health

# In PostgreSQL console
\l              # List databases
\dt             # List tables
\q              # Quit
```

### 1.4 Stop Services
```bash
# In docker-compose terminal
Ctrl+C

# Clean up
docker-compose down
```

✅ **If everything works locally, proceed to cloud deployment**

---

## Step 2: Create GCP Project (5 minutes)

### 2.1 Create Project
1. Go to: https://console.cloud.google.com/
2. Click "Select a Project" → "NEW PROJECT"
3. Name: `mental-health-app`
4. Click CREATE
5. Wait 1-2 minutes for creation

### 2.2 Copy Project ID
```
Your Project ID appears at top (example: mental-health-app-12345)
Save this - you'll need it!
```

### 2.3 Enable Billing
1. Click profile icon → Billing
2. LINK BILLING ACCOUNT
3. Select or create billing account
4. Link to your project

⚠️ **Billing is required for GKE!**

### 2.4 Enable APIs
```bash
# Set your project
gcloud config set project YOUR_PROJECT_ID
# Example: gcloud config set project mental-health-app-12345

# Enable required APIs
gcloud services enable container.googleapis.com
gcloud services enable compute.googleapis.com
gcloud services enable iam.googleapis.com

# Wait 1-2 minutes
```

---

## Step 3: Create Docker Hub Account (5 minutes)

### 3.1 Create Account
1. Go to: https://hub.docker.com/
2. Click Sign Up
3. Email: your-email
4. Username: choose-username (you'll use this later!)
5. Password: strong password
6. Verify email

### 3.2 Create Access Token
1. Login to Docker Hub
2. Profile icon → Account Settings
3. Left menu: Security
4. New Access Token
5. Name: `github-actions`
6. Click Generate
7. **Copy the token** (you'll only see it once!)
   ```
   dckr_pat_xxxxxxxxxxxxx
   ```

**Save these:**
```
Username: your-username
Token: dckr_pat_xxxxxxxxxxxxx
```

---

## Step 4: Create GKE Cluster (10 minutes)

⚠️ **Creating a NEW cluster** (separate from your codexa-ai cluster)

### 4.1 Run Setup Script
```bash
cd /Users/macbook/Documents/GitHub/AI_Powered_Mental_Health_Assistent

chmod +x setup.sh

./setup.sh
```

### 4.2 Answer Prompts

**Question 1: Enter GCP Project ID**
```
> YOUR_SAME_PROJECT_ID
# Use the same GCP project as codexa-ai
```

**Question 2: Enter Cluster Name**
```
> mental-health-cluster
# NEW cluster name (separate from "codexa-ai")
```

**Question 3: Enter Region**
```
> (press Enter to use default)
us-central1
```

### 4.3 Wait for Completion
Script will:
- Create cluster (3-5 min)
- Get credentials
- Install NGINX Ingress (1-2 min)
- Get external IP

### 4.4 Save Output
You'll see:
```
✅ Cluster Ready!
External IP: 34.123.45.67
Access: https://app.34.123.45.67.sslip.io
```

**Copy the External IP - you need it for Step 6!**

### 4.5 Verify Cluster
```bash
gcloud container clusters list
# Should show: mental-health-cluster with STATUS "RUNNING"
```

---

## Step 5: Add GitHub Secrets (5 minutes)

ℹ️ **If you're using the same Docker Hub account and GitHub repo as codexa-ai, some values should already exist.** 
- If secrets exist: Update `OPENROUTER_API_KEY` if missing ✓
- If new repo: Create all required secrets below

### 5.1 Go to Github
1. Open your GitHub repo
2. Click Settings tab
3. Left menu: Secrets and variables → Actions

### 5.2 Create Secrets

Click "New repository secret" for each:

**Secret 1: DOCKER_PASSWORD** (required)
```
Name: DOCKER_PASSWORD
Value: dckr_pat_xxxxxxxxxxxxx
```

**Secret 2: OPENROUTER_API_KEY** ⭐ (required for LLM)
```
Name: OPENROUTER_API_KEY
Value: sk-or-v1-xxxxxxxxxxxxxxxx
```
**How to get it:**
1. Go to: https://openrouter.ai/
2. Sign up or login
3. Click "Keys" in sidebar
4. Create new key
5. Copy the key (looks like: sk-or-v1-...)
6. Paste into GitHub Secret

**Secret 3: LETSENCRYPT_EMAIL** ⭐ (required for valid HTTPS certificate)
```
Name: LETSENCRYPT_EMAIL
Value: your-email@example.com
```
**Why this is needed:**
1. cert-manager uses this email when requesting the Let's Encrypt certificate
2. The deployed app will then get a browser-trusted TLS certificate for `app.{IP}.sslip.io`
3. Without it, HTTPS falls back to the ingress controller's default self-signed cert and browsers show a warning

This repo's workflow already contains the configured values for:
- Docker Hub username
- GCP project ID
- Workload Identity provider
- Workload Identity service account

If you move this repo to a different Docker Hub account, GCP project, or GitHub repository, update [deploy.yml](/Users/macbook/Documents/GitHub/AI_Powered_Mental_Health_Assistent/.github/workflows/deploy.yml).

### 5.3 Verify
You should see all secrets in GitHub Settings.

---

## Step 6: Update Configuration (2 minutes)

### 6.1 Update Docker Username

For this repo, GitHub Actions replaces `DOCKER_USERNAME` automatically during deployment using the workflow env value.

Only edit `k8s/app.yaml` manually if you plan to run `kubectl apply -f k8s/app.yaml` yourself outside GitHub Actions.

```bash
cd /Users/macbook/Documents/GitHub/AI_Powered_Mental_Health_Assistent

# Replace manually only if you are not using the GitHub Actions workflow
sed -i '' 's/DOCKER_USERNAME/your-docker-username/g' k8s/app.yaml

# Example with real username:
# sed -i '' 's/DOCKER_USERNAME/john-doe/g' k8s/app.yaml
```

Verify:
```bash
grep "john-doe" k8s/app.yaml
# Should show 2 lines with your username
```

### 6.2 Update External IP

Replace `CLUSTER_IP` with your External IP from Step 4:

```bash
# Your IP (example: 34.123.45.67)
sed -i '' 's/CLUSTER_IP/34.123.45.67/g' k8s/app.yaml
```

Verify:
```bash
grep "sslip.io" k8s/app.yaml
# Should show: app.34.123.45.67.sslip.io
```

### 6.3 Update Let's Encrypt Email For Manual `kubectl` Deploys

If you are deploying manually instead of using GitHub Actions, replace the placeholder in [cert-manager-clusterissuer.yaml](/Users/macbook/Documents/GitHub/AI_Powered_Mental_Health_Assistent/k8s/cert-manager-clusterissuer.yaml):

```bash
sed -i '' 's/PLACEHOLDER_LETSENCRYPT_EMAIL/your-email@example.com/g' k8s/cert-manager-clusterissuer.yaml
kubectl apply -f k8s/cert-manager-clusterissuer.yaml
kubectl apply -f k8s/app.yaml
```

---

## Step 7: Deploy to GKE (15 minutes)

### 7.1 Push to GitHub

```bash
# Navigate to project
cd /Users/macbook/Documents/GitHub/AI_Powered_Mental_Health_Assistent

# Check changes
git status

# Add changes
git add .

# Commit
git commit -m "Configure for GKE deployment"

# Push
git push origin main
```

### 7.2 GitHub Actions Deploys Automatically

1. Go to your GitHub repo
2. Click Actions tab
3. Watch workflow: "Deploy to GKE"

Progress:
```
✓ Checkout
✓ Build and push backend        (2-3 min)
✓ Build and push frontend       (2-3 min)
✓ Authenticate to Google Cloud  (30 sec)
✓ Deploy to GKE                 (1-2 min)
✓ Get service info              (10 sec)
```

### 7.3 Verify Deployment

```bash
# Check deployments
kubectl get deployments

# Should show:
# NAME       READY   UP-TO-DATE   AVAILABLE
# backend    2/2     2            2
# frontend   1/1     1            1

# Check pods
kubectl get pods

# All should show STATUS: Running
```

---

## Step 8: Access Your Application (5 minutes)

### 8.1 Get URL
```
https://app.34.123.45.67.sslip.io
```
(Replace 34.123.45.67 with your External IP from Step 4)

### 8.2 Open in Browser
1. Open: `https://app.34.123.45.67.sslip.io`
2. Wait 1-5 minutes for cert-manager to finish the initial Let's Encrypt HTTP-01 challenge
3. Refresh the page and you should see your Angular frontend without a browser warning

### 8.3 Test Backend API
1. Open: `https://app.34.123.45.67.sslip.io/api/docs`
2. You should see Swagger UI
3. Try some endpoints

### 8.4 Verify Database
```bash
# Connect to database
kubectl exec -it postgres-0 -- psql -U postgres -d mental_health

# Inside PostgreSQL
\dt              # List tables
SELECT 1;        # Test query
\q               # Quit
```

---

## Making Changes (Going Forward)

### Deploy New Changes

```bash
# Edit your code (backend or frontend)

# Commit and push
git add .
git commit -m "Your message"
git push origin main

# GitHub Actions automatically deploys!
# Watch in GitHub Actions tab
```

---

## Monitoring & Troubleshooting

### Check Pod Status
```bash
# All resources
kubectl get all

# Specific deployments
kubectl get deployments

# Specific pods
kubectl get pods

# Specific services
kubectl get svc

# Ingress
kubectl get ingress
```

### View Logs
```bash
# Backend logs (live)
kubectl logs -f deployment/backend

# Frontend logs
kubectl logs -f deployment/frontend

# Database logs
kubectl logs postgres-0

# Specific pod
kubectl logs pod-name
```

### Describe Issues
```bash
# What's wrong with a pod?
kubectl describe pod pod-name

# What's wrong with deployment?
kubectl describe deployment backend
```

### Port Forward (Test Locally)
```bash
# Access backend locally
kubectl port-forward svc/backend 8000:80
# Then: curl http://localhost:8000

# Access frontend locally
kubectl port-forward svc/frontend 3000:80
# Then: http://localhost:3000

# Access database locally
kubectl port-forward svc/postgres 5432:5432
# Then: psql -h localhost -U postgres
```

### Restart Services
```bash
# Restart backend
kubectl rollout restart deployment/backend

# Restart frontend
kubectl rollout restart deployment/frontend

# Restart database
kubectl rollout restart statefulset/postgres
```

---

## Common Issues & Solutions

### Issue 1: Pods Not Running
```bash
# Check what's wrong
kubectl describe pod <pod-name>

# View logs
kubectl logs <pod-name>

# Restart
kubectl rollout restart deployment/backend
```

### Issue 2: Can't Access Application
**Symptom**: Connection timeout

**Solution**:
```bash
# Check ingress IP
kubectl get ingress

# If no IP, wait 2-3 minutes for the load balancer
# If HTTPS still shows a warning, wait a few more minutes for cert-manager
# to finish issuing the Let's Encrypt certificate
```

### Issue 3: Docker Images Failed to Push
**Symptom**: GitHub Actions workflow fails at "Build and push"

**Solution**:
1. Check `DOCKER_USERNAME` in [deploy.yml](/Users/macbook/Documents/GitHub/AI_Powered_Mental_Health_Assistent/.github/workflows/deploy.yml)
2. Check `DOCKER_PASSWORD` in GitHub Secrets
3. Verify the Docker Hub account can push to that namespace

### Issue 4: Database Can't Connect
**Symptom**: Backend logs show connection error

**Solution**:
```bash
# Check database pod
kubectl get pods -l app=postgres

# Check logs
kubectl logs postgres-0

# Verify it's running
kubectl describe statefulset postgres
```

### Issue 5: LLM Responses Error (Chat Not Working)
**Symptom**: 401 Unauthorized error when trying to chat

**Solution**:
1. Check that `OPENROUTER_API_KEY` secret is added in GitHub Settings
2. Verify the API key is valid at: https://openrouter.ai/keys
3. Check backend logs:
   ```bash
   kubectl logs -l app=backend
   # Should show if OPENROUTER_API_KEY is missing
   ```
4. If missing, add to GitHub Secrets and redeploy:
   ```bash
   git push origin main  # Triggers new deployment
   ```

### Issue 6: Need to Start Over
```bash
# Delete everything from cluster
kubectl delete -f k8s/app.yaml

# Wait for deletion
kubectl get all

# Deploy again
kubectl apply -f k8s/app.yaml
```

---

## Cleanup & Deletion

### Delete from Cluster (Keep Cluster)
```bash
kubectl delete -f k8s/app.yaml

# Verify all deleted
kubectl get all
```

### Delete Cluster (Full Cleanup)
```bash
gcloud container clusters delete mental-health-cluster \
  --region us-central1
```

---

## File Overview

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Local development - all services |
| `docker/Dockerfile.backend` | FastAPI container recipe |
| `docker/Dockerfile.frontend` | Angular container recipe |
| `k8s/app.yaml` | Cloud deployment config (UPDATE THIS!) |
| `k8s/cert-manager-clusterissuer.yaml` | Let's Encrypt issuer used by cert-manager |
| `setup.sh` | Creates GKE cluster |
| `.github/workflows/deploy.yml` | Auto-deployment on push |

---

## Timeline Summary

| Step | Time |
|------|------|
| Local testing | 5 min |
| GCP project creation | 5 min |
| Docker Hub setup | 5 min |
| Cluster creation | 10 min |
| GitHub configuration | 5 min |
| File configuration | 2 min |
| Deployment | 15 min |
| **Total** | **~45 minutes** |

---

## What's Running

```
Your Application (GKE Cluster)
├── PostgreSQL Database
│   ├── 10GB persistent storage
│   └── Auto-restarts if fails
├── Backend API (FastAPI)
│   ├── 2 replicas
│   └── Auto-scales & restarts
├── Frontend (Angular)
│   ├── 1 replica
│   └── Auto-restarts if fails
└── NGINX Ingress Controller
    ├── Load balancer
    ├── SSL certificates (Let's Encrypt)
    └── Routes traffic
```

---

## What Secrets Are Used For

| Secret | Used By | Purpose |
|--------|---------|---------|
| `DOCKER_PASSWORD` | GitHub Actions | Password/token for Docker Hub |
| `OPENROUTER_API_KEY` | Backend container | LLM API calls for chatbot responses |
| `LETSENCRYPT_EMAIL` | cert-manager / GitHub Actions | Email used for Let's Encrypt certificate registration |
| `DOCKER_USERNAME` | Workflow env | Docker Hub namespace used for image tags |
| `GCP_PROJECT` | Workflow env | Google Cloud project used for deployment |
| `WIF_PROVIDER` | Workflow env | Keyless GitHub Actions to Google Cloud authentication |
| `WIF_SERVICE_ACCOUNT` | Workflow env | Service account impersonated by GitHub Actions |

**Key Secret: OPENROUTER_API_KEY**
- Used by backend for AI-powered chat responses
- Enables the mental health assistant to generate empathetic responses
- Create at: https://openrouter.ai/

---

## Important Notes

✅ **Before deploying:**
- Test locally with `docker-compose up`
- All secrets added to GitHub
- k8s/app.yaml updated with your username and IP
- Code committed to GitHub

✅ **After deploying:**
- Check GitHub Actions workflow succeeds
- All pods show "Running"
- Confirm `LETSENCRYPT_EMAIL` secret is set
- Wait 2-5 minutes for the first SSL certificate issuance
- Test frontend and backend access

✅ **Going forward:**
- Code changes auto-deploy on git push
- Logs available via `kubectl logs`
- Easy to scale (edit k8s/app.yaml replicas)

---

## Cost

- **GKE Cluster**: ~$110/month (3 nodes)
- **Compute**: ~$150/month
- **Load Balancer**: ~$18/month
- **Storage**: ~$10/month
- **Total**: ~$290/month

**Free for first 3 months** with $300 Google Cloud credit!

---

## Quick Commands Reference

```bash
# Local
docker-compose up                   # Start local
docker-compose down                 # Stop local

# Cluster creation
./setup.sh                           # Create cluster

# Deployment
git push origin main                 # Trigger deploy

# Status
kubectl get all                      # See all resources
kubectl get pods                     # See pods only
kubectl get deployments              # See deployments

# Logs
kubectl logs -f deployment/backend   # Watch backend logs
kubectl logs pod-name                # See pod logs

# Database
kubectl exec -it postgres-0 -- psql -U postgres -d mental_health

# Port forward
kubectl port-forward svc/postgres 5432:5432

# Restart
kubectl rollout restart deployment/backend

# Delete
kubectl delete -f k8s/app.yaml       # Delete app
gcloud container clusters delete mental-health-cluster --region us-central1  # Delete cluster
```

---

## Success Checklist

- [ ] Local testing works
- [ ] GCP project created
- [ ] Billing enabled
- [ ] Docker Hub account created
- [ ] APIs enabled on GCP
- [ ] GKE cluster created (./setup.sh)
- [ ] OpenRouter API key obtained (https://openrouter.ai/)
- [ ] GitHub secrets added, including `DOCKER_PASSWORD`, `OPENROUTER_API_KEY`, and `LETSENCRYPT_EMAIL`
- [ ] k8s/app.yaml updated (username and IP)
- [ ] Pushed to GitHub
- [ ] GitHub Actions workflow passed
- [ ] All pods running: `kubectl get pods`
- [ ] Application accessible: `https://app.{IP}.sslip.io`
- [ ] Database connection works
- [ ] Backend API responds
- [ ] Chat/AI features work
- [ ] Frontend loads properly

**🎉 All done! Your app is live in the cloud!**

---

## Need Help?

1. **Check logs**: `kubectl logs -f deployment/backend`
2. **Describe pod**: `kubectl describe pod pod-name`
3. **Check secrets**: Verify GitHub Secrets are correct
4. **Wait for certificate**: the first Let's Encrypt issuance usually takes 2-5 minutes
5. **Check syntax**: Verify k8s/app.yaml has your username and IP
