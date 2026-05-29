#!/bin/bash
set -euo pipefail

# Creates an Azure service principal for GitHub Actions and prints the JSON
# for the AZURE_CREDENTIALS repository secret.
#
# Usage:
#   ./scripts/setup-azure-github-cicd.sh [github-repo-name]
# Example:
#   ./scripts/setup-azure-github-cicd.sh mdirfancse2023/AI_Powered_Mental_Health_Assistent

REPO_NAME="${1:-mdirfancse2023/AI_Powered_Mental_Health_Assistent}"
SP_NAME="github-ai-mental-health-deploy"
RG_NAME="myportfolio-rg"
ACR_NAME="myportfolioregistry"
SUBSCRIPTION_ID="${AZURE_SUBSCRIPTION_ID:-477a9591-e616-49d0-972b-b2e53c906ad1}"

echo "Using subscription: $SUBSCRIPTION_ID"
az account set --subscription "$SUBSCRIPTION_ID"

SP_JSON=$(az ad sp create-for-rbac \
  --name "$SP_NAME" \
  --role contributor \
  --scopes "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RG_NAME" \
  --sdk-auth)

ACR_ID=$(az acr show --name "$ACR_NAME" --resource-group "$RG_NAME" --query id -o tsv)
SP_APP_ID=$(echo "$SP_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['clientId'])")

az role assignment create \
  --assignee "$SP_APP_ID" \
  --role AcrPush \
  --scope "$ACR_ID" \
  --only-show-errors || true

echo ""
echo "Add this JSON as GitHub secret AZURE_CREDENTIALS:"
echo ""
echo "$SP_JSON"
echo ""
echo "Also add repository secrets:"
echo "  OPENROUTER_API_KEY"
echo "  DATABASE_URL"
echo "  AUTH_SECRET_KEY"
echo ""
echo "Grant workflow access for branch $REPO_NAME in GitHub:"
echo "  Settings -> Actions -> General -> Workflow permissions"
