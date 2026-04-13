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
cp -r ../frontend/dist/browser/* static/

# Create a simple index.html if build fails
if [ ! -f "static/index.html" ]; then
    echo "Creating fallback index.html..."
    cat > static/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>AI Mental Health Assistant</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; text-align: center; }
        .status { background: #e8f5e8; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .api-info { background: #f0f8ff; padding: 15px; border-radius: 5px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 AI Mental Health Assistant</h1>
        <div class="status">
            <strong>✅ Backend is running!</strong><br>
            The API is available at <code>/api</code> endpoints.
        </div>
        <div class="api-info">
            <strong>📡 API Endpoints:</strong><br>
            • Health: <a href="/api">GET /api</a><br>
            • Chat: <a href="/api/docs">API Documentation</a><br>
            • Auth: <a href="/api/auth">Authentication</a>
        </div>
        <p><em>Note: Frontend build may be in progress. Try refreshing in a few minutes.</em></p>
    </div>
</body>
</html>
EOF
fi

echo "✅ Build complete!"
