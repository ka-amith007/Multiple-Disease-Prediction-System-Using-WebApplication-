# 🎨 Add Your Logo - Quick Guide

## Step 1: Prepare Your Logo

1. **Find your logo file** (PNG format recommended)
2. **Make sure it's square** (same width and height)
3. **Good quality** - at least 512x512 pixels

---

## Step 2: Auto-Resize Your Logo

### Method 1: Using the Script (EASY!)

```powershell
# Navigate to project folder
cd "c:\Users\Anusha\Desktop\Multiple-Disease-Prediction-Webapp-main  zip file\Multiple-Disease-Prediction-Webapp-main"

# Run the resize script
python resize_logo.py

# When prompted, enter your logo path, example:
C:\Users\Anusha\Desktop\my-logo.png
```

The script will automatically create 3 sizes in the `assets` folder!

### Method 2: Manual Resize (If script doesn't work)

Use online tool: https://www.iloveimg.com/resize-image

Create these 3 files:
- `logo.png` - Resize to 180x180
- `icon-192x192.png` - Resize to 192x192  
- `icon-512x512.png` - Resize to 512x512

Save all 3 files in the `assets` folder.

---

## Step 3: Verify Files

Your folder should look like this:

```
Multiple-Disease-Prediction-Webapp-main/
├── assets/
│   ├── logo.png ✅
│   ├── icon-192x192.png ✅
│   └── icon-512x512.png ✅
```

---

## Step 4: Test Locally

```powershell
# Start the app
streamlit run app.py

# Open in browser: http://localhost:8501
# You should see your logo in the browser tab!
```

---

## Step 5: Deploy to Railway

Once your logo is added:

```powershell
# Push to GitHub
git add .
git commit -m "Added PWA support with brand logo"
git push

# Deploy to Railway (it will auto-deploy from GitHub)
```

---

## Step 6: Install on Mobile 📱

### Android:
1. Open your deployed app URL in **Chrome**
2. Tap **menu (⋮)** → **"Install app"**
3. Your logo will appear on home screen! 🎉

### iPhone:
1. Open your deployed app URL in **Safari**
2. Tap **Share (□↑)** → **"Add to Home Screen"**
3. Your logo will appear on home screen! 🎉

---

## 🎯 What You Get

✅ Custom app icon on home screen  
✅ Professional splash screen  
✅ Standalone app (no browser UI)  
✅ Works offline  
✅ Push notifications ready  
✅ Full-screen experience  

---

## 🆘 Troubleshooting

**Q: I don't have a logo yet**  
A: Use a free logo maker:
- https://www.canva.com/create/logos/
- https://logo.com/
- https://www.freelogodesign.org/

**Q: Script doesn't work**  
A: Use the online tool (Method 2)

**Q: Logo doesn't show**  
A: Make sure files are exactly named:
- `logo.png`
- `icon-192x192.png`
- `icon-512x512.png`

**Q: Can I change logo later?**  
A: Yes! Just replace the files and redeploy

---

## 📞 Need Help?

Check `MOBILE_APP_SETUP.md` for detailed instructions!

---

**Ready? Run `python resize_logo.py` to add your logo!** 🚀
