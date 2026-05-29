#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "🚀 Starting Azure App Service Deployment setup"

# 1. Check Azure CLI
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI (az) is not installed. Please install it first (e.g. 'brew install azure-cli')."
    exit 1
fi

# 2. Check login status
echo "Checking Azure authentication status..."
if ! az account show &> /dev/null; then
    echo "🔑 You are not logged in to Azure. Launching browser to log in..."
    az login
else
    AZ_USER=$(az account show --query "user.name" -o tsv)
    AZ_SUB=$(az account show --query "name" -o tsv)
    echo "✅ Authenticated as: $AZ_USER ($AZ_SUB)"
fi

# 3. Build Angular frontend
echo "🏗️  Step 1: Building Angular Frontend..."
cd frontend
npm install
npm run build -- --configuration=production
cd ..

# 4. Prepare backend static directory
echo "📂 Step 2: Preparing backend static directory..."
mkdir -p backend/static
# Clean old files first
rm -rf backend/static/*
cp -r frontend/dist/frontend/browser/* backend/static/
echo "✅ Frontend copied to backend static directory!"

# 5. Prompt for deployment details
echo ""
echo "📝 Step 3: Configure Azure App Service details"
read -p "Enter Azure Web App Name (default: ai-mental-health-assistant): " APP_NAME
APP_NAME=${APP_NAME:-ai-mental-health-assistant}

read -p "Enter Resource Group Name (default: ai-mental-health-rg): " RG_NAME
RG_NAME=${RG_NAME:-ai-mental-health-rg}

read -p "Enter Azure Location (default: eastus): " LOCATION
LOCATION=${LOCATION:-eastus}

read -p "Enter Pricing Tier/SKU (F1 for Free, B1 for Basic. default: F1): " SKU
SKU=${SKU:-F1}

echo ""
echo "Deploying with the following configuration:"
echo "  - Web App Name: $APP_NAME"
echo "  - Resource Group: $RG_NAME"
echo "  - Location: $LOCATION"
echo "  - SKU: $SKU"
echo "  - Runtime: Python 3.11"
echo ""

# 6. Deploy backend folder to Azure App Service
echo "🚀 Step 4: Deploying backend application to Azure..."
cd backend

# Use az webapp up to build, zip, and deploy the application
az webapp up \
    --name "$APP_NAME" \
    --resource-group "$RG_NAME" \
    --location "$LOCATION" \
    --sku "$SKU" \
    --runtime "PYTHON:3.11"

echo "✅ App deployed to Azure App Service!"
echo ""
echo "⚠️  Important next steps:"
echo "1. Configure your environment variables (App Settings) on Azure App Service:"
echo "   - OPENROUTER_API_KEY"
echo "   - DATABASE_URL (for your Azure Database for PostgreSQL)"
echo "   - AUTH_SECRET_KEY"
echo ""
echo "   You can set these via the Azure Portal or using the CLI command:"
echo "   az webapp config appsettings set --name $APP_NAME --resource-group $RG_NAME \\"
echo "     --settings OPENROUTER_API_KEY=\"<key>\" DATABASE_URL=\"<db_url>\" AUTH_SECRET_KEY=\"<secret>\""
echo ""
echo "2. Configure the Startup Command in Azure App Service Configuration:"
echo "   Startup Command: uvicorn main:app --host 0.0.0.0 --port 8000"
echo ""
echo "   You can set this in Portal under Configuration -> General Settings -> Startup Command"
echo "   Or using the CLI command:"
echo "   az webapp config set --name $APP_NAME --resource-group $RG_NAME \\"
echo "     --startup-file \"uvicorn main:app --host 0.0.0.0 --port 8000\""
echo ""
echo "3. Restart the web app to apply changes:"
echo "   az webapp restart --name $APP_NAME --resource-group $RG_NAME"
echo ""
echo "🎉 Done! Access your application at: https://$APP_NAME.azurewebsites.net"
