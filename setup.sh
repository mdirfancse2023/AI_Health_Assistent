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
helm repo update
helm install nginx ingress-nginx/ingress-nginx \
  -n ingress-nginx --create-namespace \
  --set controller.service.type=LoadBalancer || echo "NGINX already installed"

# Wait for external IP
echo "Waiting for external IP..."
sleep 30

EXTERNAL_IP=$(kubectl get svc -n ingress-nginx ingress-nginx-controller \
  -o jsonpath='{.status.loadBalancer.ingress[0].ip}' || echo "pending")

echo ""
echo "✅ Cluster Ready!"
echo "External IP: $EXTERNAL_IP"
echo "Access: http://app.$EXTERNAL_IP.sslip.io"
echo ""
echo "Next steps:"
echo "1. Add GitHub Secrets:"
echo "   - DOCKER_USERNAME"
echo "   - DOCKER_PASSWORD"
echo "   - GCP_PROJECT=$PROJECT_ID"
echo "   - WIF_PROVIDER"
echo "   - WIF_SERVICE_ACCOUNT"
echo "2. Update k8s/app.yaml with your Docker username and IP"
echo "3. Push to GitHub to trigger deployment"
