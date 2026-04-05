#!/bin/bash

set -e

echo "🚀 Setup GKE Cluster"

read -p "Enter GCP Project ID: " PROJECT_ID
read -p "Enter Cluster Name (default: mental-health-cluster): " CLUSTER_NAME
CLUSTER_NAME=${CLUSTER_NAME:-mental-health-cluster}
read -p "Enter Region (default: us-central1): " REGION
REGION=${REGION:-us-central1}

# Set project
gcloud config set project $PROJECT_ID

# Enable APIs
gcloud services enable container.googleapis.com compute.googleapis.com

# Create cluster (Autopilot mode - fully managed by GCP)
echo "Creating Autopilot cluster..."
gcloud container clusters create-auto $CLUSTER_NAME \
  --region $REGION \
  --project $PROJECT_ID || echo "Cluster already exists"

# Get credentials
gcloud container clusters get-credentials $CLUSTER_NAME --region $REGION

# Install NGINX Ingress
echo "Installing NGINX Ingress..."
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo add jetstack https://charts.jetstack.io --force-update
helm repo update
helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
  -n ingress-nginx --create-namespace \
  --set controller.service.type=LoadBalancer

# Install cert-manager for Let's Encrypt certificates
echo "Installing cert-manager..."
helm upgrade --install cert-manager jetstack/cert-manager \
  -n cert-manager --create-namespace \
  --set crds.enabled=true

echo "Waiting for cert-manager..."
kubectl rollout status deployment/cert-manager -n cert-manager --timeout=180s
kubectl rollout status deployment/cert-manager-cainjector -n cert-manager --timeout=180s
kubectl rollout status deployment/cert-manager-webhook -n cert-manager --timeout=180s

# Wait for external IP
echo "Waiting for external IP..."
sleep 30

EXTERNAL_IP=$(kubectl get svc -n ingress-nginx ingress-nginx-controller \
  -o jsonpath='{.status.loadBalancer.ingress[0].ip}' || echo "pending")

echo ""
echo "✅ Cluster Ready!"
echo "External IP: $EXTERNAL_IP"
echo "Access: https://health.$EXTERNAL_IP.sslip.io"
echo ""
echo "Next steps:"
echo "1. Add GitHub Secrets:"
echo "   - DOCKER_PASSWORD"
echo "   - OPENROUTER_API_KEY"
echo "   - LETSENCRYPT_EMAIL"
echo "2. If you are using a different project or repo, update .github/workflows/deploy.yml"
echo "3. Push to GitHub to trigger deployment"
