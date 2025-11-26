#!/bin/bash

# Multiple Disease Prediction App - Deployment Script
# This script helps deploy the app to various platforms

echo "=================================="
echo "Disease Prediction App Deployment"
echo "=================================="
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Menu
echo "Choose deployment platform:"
echo "1. Streamlit Cloud (Free)"
echo "2. Heroku"
echo "3. Render"
echo "4. Railway"
echo "5. Docker (Local)"
echo "6. Setup Git Repository"
echo "7. Exit"
echo ""
read -p "Enter choice [1-7]: " choice

case $choice in
    1)
        echo ""
        echo "📦 Streamlit Cloud Deployment"
        echo "==============================="
        echo ""
        echo "Steps:"
        echo "1. Push your code to GitHub"
        echo "2. Go to https://share.streamlit.io/"
        echo "3. Sign in with GitHub"
        echo "4. Click 'New app' and select your repository"
        echo "5. Set main file to: app.py"
        echo "6. Click 'Deploy'"
        echo ""
        echo "Note: Streamlit Cloud may have issues with the Flask API."
        echo "Consider deploying Flask separately or using serverless functions."
        ;;
    
    2)
        echo ""
        echo "📦 Heroku Deployment"
        echo "===================="
        echo ""
        
        if ! command_exists heroku; then
            echo "❌ Heroku CLI not found!"
            echo "Install from: https://devcenter.heroku.com/articles/heroku-cli"
            exit 1
        fi
        
        read -p "Enter your app name: " appname
        
        echo "Logging in to Heroku..."
        heroku login
        
        echo "Creating Heroku app..."
        heroku create $appname
        
        echo "Adding Python buildpack..."
        heroku buildpacks:add heroku/python
        
        echo "Setting up Git..."
        git init
        git add .
        git commit -m "Initial deployment to Heroku"
        
        echo "Deploying to Heroku..."
        git push heroku main
        
        echo "Opening app..."
        heroku open
        
        echo "✅ Deployment complete!"
        ;;
    
    3)
        echo ""
        echo "📦 Render Deployment"
        echo "===================="
        echo ""
        echo "Steps:"
        echo "1. Push your code to GitHub (run option 6 first)"
        echo "2. Go to https://render.com/"
        echo "3. Sign up/Login"
        echo "4. Click 'New +' > 'Web Service'"
        echo "5. Connect your GitHub repository"
        echo "6. Configure:"
        echo "   - Name: disease-prediction-app"
        echo "   - Environment: Python 3"
        echo "   - Build Command: pip install -r requirements-deploy.txt"
        echo "   - Start Command: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0"
        echo "7. Click 'Create Web Service'"
        echo ""
        echo "✅ Follow the steps above!"
        ;;
    
    4)
        echo ""
        echo "📦 Railway Deployment"
        echo "====================="
        echo ""
        echo "Steps:"
        echo "1. Push your code to GitHub (run option 6 first)"
        echo "2. Go to https://railway.app/"
        echo "3. Sign in with GitHub"
        echo "4. Click 'New Project' > 'Deploy from GitHub repo'"
        echo "5. Select your repository"
        echo "6. Railway will auto-detect and deploy"
        echo ""
        echo "✅ Follow the steps above!"
        ;;
    
    5)
        echo ""
        echo "🐳 Docker Deployment"
        echo "===================="
        echo ""
        
        if ! command_exists docker; then
            echo "❌ Docker not found!"
            echo "Install from: https://www.docker.com/get-started"
            exit 1
        fi
        
        echo "Building Docker image..."
        docker build -t disease-prediction-app .
        
        echo "Running Docker container..."
        docker run -d -p 8501:8501 -p 5001:5001 --name disease-app disease-prediction-app
        
        echo ""
        echo "✅ Docker container started!"
        echo "Access the app at: http://localhost:8501"
        echo ""
        echo "Useful commands:"
        echo "  Stop:    docker stop disease-app"
        echo "  Start:   docker start disease-app"
        echo "  Remove:  docker rm disease-app"
        echo "  Logs:    docker logs disease-app"
        ;;
    
    6)
        echo ""
        echo "📦 Git Repository Setup"
        echo "======================="
        echo ""
        
        if ! command_exists git; then
            echo "❌ Git not found!"
            echo "Install from: https://git-scm.com/downloads"
            exit 1
        fi
        
        read -p "Enter your GitHub repository URL: " repo_url
        
        echo "Initializing Git repository..."
        git init
        
        echo "Adding all files..."
        git add .
        
        echo "Creating initial commit..."
        git commit -m "Initial commit - Multiple Disease Prediction App"
        
        echo "Setting main branch..."
        git branch -M main
        
        echo "Adding remote repository..."
        git remote add origin $repo_url
        
        echo "Pushing to GitHub..."
        git push -u origin main
        
        echo ""
        echo "✅ Code pushed to GitHub!"
        echo "Repository: $repo_url"
        ;;
    
    7)
        echo "Goodbye!"
        exit 0
        ;;
    
    *)
        echo "❌ Invalid choice!"
        exit 1
        ;;
esac
