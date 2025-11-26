# 🚀 Quick Deployment Guide

## Choose Your Deployment Method

### 🎯 Easiest: Streamlit Cloud (FREE)
**Best for:** Simple demo, no Flask API needed
```bash
# Run the Windows deployment script
.\deploy.ps1
# Choose option 1
```

### 💪 Recommended: Railway (FREE tier available)
**Best for:** Full app with Flask API
1. Push to GitHub: `.\deploy.ps1` → Option 6
2. Visit: https://railway.app/
3. Connect GitHub repo
4. Deploy automatically!

### 🐳 Docker (Run anywhere)
```bash
# Build and run
docker-compose up -d

# Access at http://localhost:8501
```

### 📦 Heroku (Classic PaaS)
```bash
# Windows
.\deploy.ps1
# Choose option 2

# Or manually:
heroku create your-app-name
git push heroku main
```

---

## 📋 Pre-Deployment Checklist

- [ ] All dependencies in `requirements-deploy.txt`
- [ ] Flask API working on port 5001
- [ ] Streamlit app working on port 8501
- [ ] Models saved in correct folders
- [ ] `.gitignore` configured
- [ ] Git repository initialized

---

## ⚡ Quick Deploy Command

### Windows:
```powershell
.\deploy.ps1
```

### Linux/Mac:
```bash
chmod +x deploy.sh
./deploy.sh
```

---

## 🌐 Deployment URLs

After deploying, your app will be available at:

- **Streamlit Cloud**: `https://your-username-disease-prediction.streamlit.app`
- **Heroku**: `https://your-app-name.herokuapp.com`
- **Render**: `https://your-app-name.onrender.com`
- **Railway**: `https://your-app-name.up.railway.app`

---

## 🔧 Environment Variables

Set these on your hosting platform:

```env
PYTHONUNBUFFERED=1
FLASK_APP=skin_disease_api/app.py
API_URL=http://localhost:5001/predict
```

---

## 🎬 Video Tutorial Links

- Streamlit Cloud: https://docs.streamlit.io/streamlit-community-cloud
- Heroku: https://devcenter.heroku.com/categories/deployment
- Railway: https://docs.railway.app/
- Render: https://render.com/docs

---

## 💡 Pro Tips

1. **Model Size**: The ML models are large. Use Git LFS or host separately
2. **Free Tiers**: Most platforms have usage limits on free plans
3. **Flask API**: Consider serverless functions for production
4. **Performance**: Use GPU instances for faster predictions
5. **Monitoring**: Add logging and error tracking

---

## 🆘 Common Issues

### Issue: "Model file not found"
**Solution**: Ensure models are in correct directory or use Git LFS

### Issue: "Port already in use"
**Solution**: Change port in `skin_disease_api/app.py`

### Issue: "Memory limit exceeded"
**Solution**: Upgrade to paid tier or optimize model size

### Issue: "Flask API timeout"
**Solution**: Increase timeout in `app.py` or deploy Flask separately

---

## 📞 Need Help?

1. Check `DEPLOYMENT_GUIDE.md` for detailed instructions
2. Read platform-specific documentation
3. Check GitHub Issues
4. Contact support

---

**Ready to deploy? Run `.\deploy.ps1` and choose your platform!** 🚀
