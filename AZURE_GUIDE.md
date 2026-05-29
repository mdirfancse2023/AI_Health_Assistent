# Azure Deployment Guide

This guide details how to deploy the AI-Powered Mental Health Assistant to **Azure App Service** and connect it to **Azure Database for PostgreSQL**.

---

## 🏗️ System Architecture on Azure

On Azure, we run the frontend and backend consolidated into a single Web App. The FastAPI backend serves the Angular frontend dynamically from the `/` route and other static asset paths, while routing `/api/*` endpoints to the FastAPI application.

```
                  ┌──────────────────────────────────────────┐
                  │          Azure App Service               │
                  │   ┌──────────────────────────────────┐   │
  User Browser ───┼──►│  FastAPI (Serving static files)   │   │
                  │   └────────────────▲─────────────────┘   │
                  └────────────────────┼─────────────────────┘
                                       │ (Port 8000 / Int. Network)
                  ┌────────────────────▼─────────────────────┐
                  │   Azure Database for PostgreSQL          │
                  │   (Flexible Server)                      │
                  └──────────────────────────────────────────┘
```

---

## 📋 Prerequisites

Before deploying, ensure you have:
1. **Azure CLI** installed:
   ```bash
   brew install azure-cli
   ```
2. **LoggedIn status**:
   Ensure you are logged in to your Azure Account (we verified you are currently on the **Azure for Students** subscription):
   ```bash
   az account show
   ```
   *If you are not logged in, run `az login` first.*

---

## Step 1: Deploy to Azure App Service (Manual CLI)

We have provided a deployment script [deploy-to-azure.sh](deploy-to-azure.sh) to build the frontend and deploy the FastAPI backend package.

1. Run the script:
   ```bash
   ./deploy-to-azure.sh
   ```
2. Follow the interactive prompts to define your **Web App Name**, **Resource Group**, **Location** (e.g. `eastus`), and **Pricing SKU** (default is `F1` which is the Free tier).
3. The script will:
   - Compile the Angular frontend for production.
   - Copy built static assets to the `backend/static/` directory.
   - Zip the `backend` folder and run `az webapp up` to create the App Service and push the code.

---

## Step 2: Provision Azure Database for PostgreSQL (Flexible Server)

Azure App Service requires a PostgreSQL database to store user details, chat history, and analytics logs.

1. **Create the PostgreSQL instance**:
   Run the following CLI command to provision a flexible server.
   Replace `<strong-password>` with a secure password (must be at least 8 characters and include uppercase, lowercase, numbers, and symbols).
   ```bash
   az postgres flexible-server create \
     --name mental-health-db-server \
     --resource-group ai-mental-health-rg \
     --location eastus \
     --admin-user postgres \
     --admin-password "<strong-password>" \
     --sku-name Standard_B1ms \
     --tier Burstable \
     --database-name mental_health \
     --active-directory-auth Disabled
   ```
   *Note: Standard_B1ms is a low-cost burstable instance ideal for development/student credit budgets.*

2. **Allow access from Azure App Service**:
   Azure Database for PostgreSQL Flexible Server restricts traffic by default. Run the following command to allow internal connections from other Azure services (like our App Service):
   ```bash
   az postgres flexible-server firewall-rule create \
     --name AllowAzureIPs \
     --rule-name AllowAllAzureServicesAndResourcesWithinFromAzureIPs \
     --resource-group ai-mental-health-rg \
     --server-name mental-health-db-server \
     --start-ip-address 0.0.0.0 \
     --end-ip-address 0.0.0.0
   ```

---

## Step 3: Configure Web App Environment Variables (App Settings)

Azure App Service requires configuration settings (environment variables) to run.

Configure the settings using the Azure CLI. Replace the placeholders with your actual values:
```bash
az webapp config appsettings set \
  --name ai-mental-health-assistant \
  --resource-group ai-mental-health-rg \
  --settings \
    OPENROUTER_API_KEY="sk-or-v1-xxxxxxxxxxxxxxxx" \
    AUTH_SECRET_KEY="generate-with-openssl-rand-base64-32" \
    DATABASE_URL="postgresql://postgres:<password>@mental-health-db-server.postgres.database.azure.com/mental_health?sslmode=require"
```

---

## Step 4: Configure App Service Startup File

By default, Azure's Python container looks for Gunicorn to start Python web servers. Since Gunicorn is not added to our direct dependencies, we will instruct Azure to run the application using Uvicorn directly:

1. **Set Startup Command**:
   ```bash
   az webapp config set \
     --name ai-mental-health-assistant \
     --resource-group ai-mental-health-rg \
     --startup-file "uvicorn main:app --host 0.0.0.0 --port 8000"
   ```

2. **Restart the Web App**:
   ```bash
   az webapp restart \
     --name ai-mental-health-assistant \
     --resource-group ai-mental-health-rg
   ```

3. **Verify Deployment**:
   Your app will be live at:
   `https://<webapp-name>.azurewebsites.net` (e.g. `https://ai-mental-health-assistant.azurewebsites.net`)

---

## Step 5: Setup Automated CI/CD via GitHub Actions

Pushes to the `main` branch run [.github/workflows/deploy-azure.yml](.github/workflows/deploy-azure.yml), which:

1. Builds the Angular frontend (`/aimentalhealth/` base path).
2. Builds and pushes the Docker image to `myportfolioregistry.azurecr.io`.
3. Updates the `ai-mental-health` Container App in `myportfolio-rg`.
4. Rebuilds the portfolio Caddy proxy only when `docker/Caddyfile.myportfolio` changes.

**Live URL after deploy:** `https://virtualgyans.tech/aimentalhealth/`

### 1. Create Azure credentials for GitHub

Run (after `az login`):

```bash
chmod +x scripts/setup-azure-github-cicd.sh
./scripts/setup-azure-github-cicd.sh
```

Copy the printed JSON.

### 2. Add GitHub repository secrets

In your repo: **Settings → Secrets and variables → Actions → New repository secret**

| Secret | Description |
|--------|-------------|
| `AZURE_CREDENTIALS` | Full JSON from the setup script |
| `OPENROUTER_API_KEY` | From your `.env` |
| `DATABASE_URL` | PostgreSQL URL, e.g. `postgresql://postgres:<password>@mh-db-server-2513.postgres.database.azure.com/mental_health?sslmode=require` |
| `AUTH_SECRET_KEY` | Random secret for JWT (e.g. `openssl rand -base64 32`) |

### 3. Trigger a deployment

```bash
git add .
git commit -m "Your change"
git push origin main
```

Track progress under the **Actions** tab on GitHub.

You can also run the workflow manually from **Actions → Deploy to Azure Container Apps → Run workflow**.

---

## 🔍 Monitoring & Troubleshooting

### View Application Logs
To watch the live log stream of the Container App:
```bash
az containerapp logs show \
  --name ai-mental-health \
  --resource-group myportfolio-rg \
  --follow
```

### SSH Into App Service
You can open an SSH terminal inside the running container:
- Go to the Azure Portal -> **Web App** -> **SSH** (under Development Tools) -> click **Go**.
- Or access via Kudu: `https://<webapp-name>.scm.azurewebsites.net/webssh/host`

### Restart Container App
If the app doesn't load or is stuck in startup:
```bash
az containerapp revision restart \
  --name ai-mental-health \
  --resource-group myportfolio-rg \
  --revision $(az containerapp revision list -n ai-mental-health -g myportfolio-rg --query "[0].name" -o tsv)
```
