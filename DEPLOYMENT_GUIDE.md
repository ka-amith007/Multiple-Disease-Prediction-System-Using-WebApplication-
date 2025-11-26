# Multiple Disease Prediction Web Application - Deployment Guide

## 🚀 Deployment Options

### Option 1: Streamlit Cloud (Recommended - FREE)

**Steps:**

1. **Create GitHub Repository**
   ```bash
   cd "c:\Users\Anusha\Desktop\Multiple-Disease-Prediction-Webapp-main  zip file\Multiple-Disease-Prediction-Webapp-main"
   git init
   git add .
   git commit -m "Initial commit - Multiple Disease Prediction App"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/disease-prediction-app.git
   git push -u origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Go to https://share.streamlit.io/
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file: `app.py`
   - Click "Deploy"

**Note:** Streamlit Cloud has limitations with Flask API. You'll need to modify the app to work without the separate Flask server.

---

### Option 2: Heroku (Supports Both Streamlit + Flask API)

**Prerequisites:**
- Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
- Create Heroku account: https://signup.heroku.com/

**Steps:**

1. **Login to Heroku**
   ```bash
   heroku login
   ```

2. **Create Heroku App**
   ```bash
   cd "c:\Users\Anusha\Desktop\Multiple-Disease-Prediction-Webapp-main  zip file\Multiple-Disease-Prediction-Webapp-main"
   heroku create your-disease-prediction-app
   ```

3. **Add Buildpacks**
   ```bash
   heroku buildpacks:add heroku/python
   ```

4. **Deploy**
   ```bash
   git init
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

5. **Open App**
   ```bash
   heroku open
   ```

**Important:** Heroku free tier is limited. The app might be slow due to model size.

---

### Option 3: Render (FREE with limitations)

**Steps:**

1. **Push to GitHub** (same as Option 1)

2. **Deploy on Render**
   - Go to https://render.com/
   - Sign up/Login
   - Click "New +"
   - Select "Web Service"
   - Connect your GitHub repo
   - Configure:
     - Name: disease-prediction-app
     - Environment: Python 3
     - Build Command: `pip install -r requirements-deploy.txt`
     - Start Command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
   - Click "Create Web Service"

---

### Option 4: Railway (Good for API + Streamlit)

**Steps:**

1. **Push to GitHub** (same as Option 1)

2. **Deploy on Railway**
   - Go to https://railway.app/
   - Sign in with GitHub
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will auto-detect and deploy

---

### Option 5: AWS / Azure / Google Cloud (Production)

For production deployment with full control:

**AWS Elastic Beanstalk:**
```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.10 disease-prediction-app

# Create environment
eb create disease-prediction-env

# Deploy
eb deploy

# Open app
eb open
```

**Azure App Service:**
```bash
# Install Azure CLI
# https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

# Login
az login

# Create resource group
az group create --name disease-prediction-rg --location eastus

# Create app service plan
az appservice plan create --name disease-prediction-plan --resource-group disease-prediction-rg --sku B1 --is-linux

# Create web app
az webapp create --resource-group disease-prediction-rg --plan disease-prediction-plan --name your-disease-app --runtime "PYTHON:3.10"

# Deploy
az webapp deployment source config-local-git --name your-disease-app --resource-group disease-prediction-rg
git remote add azure <GIT_URL_FROM_ABOVE>
git push azure main
```

---

## 📝 Important Notes

### Model Size Issues
The TensorFlow model (`skin_disease_model_final.keras`) is large. For free hosting:
1. Use Git LFS for large files
2. Consider model compression
3. Host model separately (AWS S3, Google Cloud Storage)

### Environment Variables
Set these on your hosting platform:
```
FLASK_APP=skin_disease_api/app.py
PYTHONUNBUFFERED=1
```

### Flask API Configuration
Update `app.py` line 855 to use environment variable:
```python
API_URL = os.getenv('API_URL', 'http://localhost:5001/predict')
```

---

## 🔧 Troubleshooting

**Issue:** App crashes due to memory limits
**Solution:** Use a paid tier or optimize model size

**Issue:** Flask API not responding
**Solution:** Deploy Flask as separate service or merge into single process

**Issue:** Slow predictions
**Solution:** Use GPU-enabled hosting (AWS EC2 with GPU, Google Cloud ML)

---

## 📊 Recommended Setup for Production

1. **Frontend**: Streamlit Cloud (FREE)
2. **Backend API**: Railway or Render (FREE tier)
3. **Model Storage**: AWS S3 or Google Cloud Storage
4. **Database** (if needed): MongoDB Atlas (FREE tier)

---

## 🎯 Quick Deploy Commands

### For Heroku:
```bash
heroku create
git push heroku main
heroku ps:scale web=1
heroku open
```

### For Streamlit Cloud:
Just push to GitHub and connect via Streamlit Cloud dashboard

### For Render:
Connect GitHub repo in Render dashboard

---

## 📞 Support

For deployment issues:
- Streamlit: https://docs.streamlit.io/
- Heroku: https://devcenter.heroku.com/
- Render: https://render.com/docs
- Railway: https://docs.railway.app/

---

**Choose the deployment option that best fits your needs!** 🚀
