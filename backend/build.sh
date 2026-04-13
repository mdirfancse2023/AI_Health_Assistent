#!/bin/bash

echo "🏗️  Building AI Mental Health Assistant for Render"

# Build frontend
echo "Building frontend..."
cd ../frontend
npm install
npm run build

# Create static directory in backend
cd ../backend
mkdir -p static

# Copy built frontend files to backend static directory
echo "Copying frontend files to backend..."
cp -r ../frontend/dist/frontend/browser/* static/

echo "✅ Build complete!"
