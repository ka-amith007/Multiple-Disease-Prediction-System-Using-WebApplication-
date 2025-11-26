# Multiple Disease Prediction App - Windows Deployment Script
# PowerShell script for deploying the app

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Disease Prediction App Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Menu
Write-Host "Choose deployment platform:" -ForegroundColor Yellow
Write-Host "1. Streamlit Cloud (Free)"
Write-Host "2. Heroku"
Write-Host "3. Render"
Write-Host "4. Railway"
Write-Host "5. Docker (Local)"
Write-Host "6. Setup Git Repository"
Write-Host "7. Generate requirements.txt"
Write-Host "8. Test locally"
Write-Host "9. Exit"
Write-Host ""

$choice = Read-Host "Enter choice [1-9]"

switch ($choice) {
    1 {
        Write-Host ""
        Write-Host "📦 Streamlit Cloud Deployment" -ForegroundColor Green
        Write-Host "===============================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Steps:"
        Write-Host "1. Push your code to GitHub (use option 6)"
        Write-Host "2. Go to https://share.streamlit.io/"
        Write-Host "3. Sign in with GitHub"
        Write-Host "4. Click 'New app' and select your repository"
        Write-Host "5. Set main file to: app.py"
        Write-Host "6. Click 'Deploy'"
        Write-Host ""
        Write-Host "⚠️  Note: You may need to deploy Flask API separately" -ForegroundColor Yellow
    }
    
    2 {
        Write-Host ""
        Write-Host "📦 Heroku Deployment" -ForegroundColor Green
        Write-Host "====================" -ForegroundColor Green
        Write-Host ""
        
        $appname = Read-Host "Enter your app name"
        
        Write-Host "Logging in to Heroku..." -ForegroundColor Cyan
        heroku login
        
        Write-Host "Creating Heroku app..." -ForegroundColor Cyan
        heroku create $appname
        
        Write-Host "Adding Python buildpack..." -ForegroundColor Cyan
        heroku buildpacks:add heroku/python
        
        Write-Host "Setting up Git..." -ForegroundColor Cyan
        git init
        git add .
        git commit -m "Initial deployment to Heroku"
        
        Write-Host "Deploying to Heroku..." -ForegroundColor Cyan
        git push heroku main
        
        Write-Host "Opening app..." -ForegroundColor Cyan
        heroku open
        
        Write-Host "✅ Deployment complete!" -ForegroundColor Green
    }
    
    3 {
        Write-Host ""
        Write-Host "📦 Render Deployment" -ForegroundColor Green
        Write-Host "====================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Steps:"
        Write-Host "1. Push code to GitHub (run option 6)"
        Write-Host "2. Go to https://render.com/"
        Write-Host "3. Sign up/Login with GitHub"
        Write-Host "4. Click 'New +' > 'Web Service'"
        Write-Host "5. Connect your repository"
        Write-Host "6. Configure:"
        Write-Host "   Build: pip install -r requirements-deploy.txt"
        Write-Host "   Start: streamlit run app.py --server.port=$PORT"
        Write-Host ""
        Write-Host "✅ Follow steps above!" -ForegroundColor Green
    }
    
    4 {
        Write-Host ""
        Write-Host "📦 Railway Deployment" -ForegroundColor Green
        Write-Host "=====================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Steps:"
        Write-Host "1. Push to GitHub (run option 6)"
        Write-Host "2. Go to https://railway.app/"
        Write-Host "3. Sign in with GitHub"
        Write-Host "4. Click 'New Project' > 'Deploy from GitHub'"
        Write-Host "5. Select your repository"
        Write-Host "6. Railway auto-deploys!"
        Write-Host ""
        Write-Host "✅ Follow steps above!" -ForegroundColor Green
    }
    
    5 {
        Write-Host ""
        Write-Host "🐳 Docker Deployment" -ForegroundColor Green
        Write-Host "====================" -ForegroundColor Green
        Write-Host ""
        
        Write-Host "Building Docker image..." -ForegroundColor Cyan
        docker build -t disease-prediction-app .
        
        Write-Host "Running Docker container..." -ForegroundColor Cyan
        docker run -d -p 8501:8501 -p 5001:5001 --name disease-app disease-prediction-app
        
        Write-Host ""
        Write-Host "✅ Docker container started!" -ForegroundColor Green
        Write-Host "Access at: http://localhost:8501" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Commands:"
        Write-Host "  Stop:   docker stop disease-app"
        Write-Host "  Start:  docker start disease-app"
        Write-Host "  Remove: docker rm disease-app"
        Write-Host "  Logs:   docker logs disease-app"
    }
    
    6 {
        Write-Host ""
        Write-Host "📦 Git Repository Setup" -ForegroundColor Green
        Write-Host "=======================" -ForegroundColor Green
        Write-Host ""
        
        $repo_url = Read-Host "Enter GitHub repository URL"
        
        Write-Host "Initializing Git..." -ForegroundColor Cyan
        git init
        
        Write-Host "Adding files..." -ForegroundColor Cyan
        git add .
        
        Write-Host "Creating commit..." -ForegroundColor Cyan
        git commit -m "Initial commit - Disease Prediction App"
        
        Write-Host "Setting main branch..." -ForegroundColor Cyan
        git branch -M main
        
        Write-Host "Adding remote..." -ForegroundColor Cyan
        git remote add origin $repo_url
        
        Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
        git push -u origin main
        
        Write-Host ""
        Write-Host "✅ Code pushed successfully!" -ForegroundColor Green
        Write-Host "Repository: $repo_url" -ForegroundColor Yellow
    }
    
    7 {
        Write-Host ""
        Write-Host "📦 Generating requirements.txt" -ForegroundColor Green
        Write-Host "===============================" -ForegroundColor Green
        Write-Host ""
        
        Write-Host "Activating virtual environment..." -ForegroundColor Cyan
        & ".venv\Scripts\Activate.ps1"
        
        Write-Host "Generating requirements..." -ForegroundColor Cyan
        pip freeze > requirements-generated.txt
        
        Write-Host ""
        Write-Host "✅ Generated requirements-generated.txt" -ForegroundColor Green
    }
    
    8 {
        Write-Host ""
        Write-Host "🧪 Testing Locally" -ForegroundColor Green
        Write-Host "==================" -ForegroundColor Green
        Write-Host ""
        
        Write-Host "Starting Flask API..." -ForegroundColor Cyan
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'skin_disease_api'; python app.py"
        
        Start-Sleep -Seconds 5
        
        Write-Host "Starting Streamlit..." -ForegroundColor Cyan
        streamlit run app.py
        
        Write-Host ""
        Write-Host "✅ App running!" -ForegroundColor Green
        Write-Host "Streamlit: http://localhost:8501" -ForegroundColor Yellow
        Write-Host "Flask API: http://localhost:5001" -ForegroundColor Yellow
    }
    
    9 {
        Write-Host "Goodbye!" -ForegroundColor Cyan
        exit 0
    }
    
    default {
        Write-Host "❌ Invalid choice!" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
