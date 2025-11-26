# Skin Disease Prediction System - Setup Guide

## 🎯 Overview
Full-stack AI-powered skin disease detection system using Deep Learning (CNN) integrated with your Multiple Disease Prediction webapp.

## 🏗️ Architecture
- **Frontend**: Streamlit (Dark Theme UI)
- **Backend**: Flask REST API
- **AI Model**: TensorFlow/Keras CNN (MobileNetV2)
- **Dataset**: ISIC/Kaggle Skin Disease Images

## 📋 Features
✅ 6 Disease Classes: Acne, Eczema, Psoriasis, Ringworm, Melanoma, Healthy Skin
✅ Real-time image upload and prediction
✅ Detailed disease information (symptoms, causes, precautions, treatments)
✅ Confidence scores and probability distribution
✅ Medical disclaimer and warnings
✅ Prediction history tracking
✅ Responsive dark theme UI

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
# Install API dependencies
cd skin_disease_api
pip install -r requirements.txt
```

### Step 2: Create Initial Model (For Testing)

```bash
# This creates an untrained model structure for testing
cd skin_disease_api
python create_initial_model.py
```

### Step 3: Start Flask API Server

```bash
# Start the backend API (keep this terminal open)
cd skin_disease_api
python app.py
```

The API will start at: http://localhost:5000

### Step 4: Start Streamlit App

```bash
# Open a NEW terminal and run:
cd ..
streamlit run app.py
```

The web app will open at: http://localhost:8501

### Step 5: Test the System
1. Go to http://localhost:8501
2. Navigate to "Skin Disease Prediction" from sidebar
3. Upload a test image (JPG or PNG)
4. Click "Analyze Image"
5. View results with detailed information

## 🎓 Training Your Own Model (Recommended for Production)

### Step 1: Prepare Dataset

```bash
cd skin_disease_api
python prepare_dataset.py
```

This will:
- Create directory structure
- Guide you to download datasets from Kaggle
- Help organize images into class folders

### Step 2: Organize Images Manually

Create this structure:
```
skin_disease_api/dataset/raw/
├── Acne/           (put acne images here)
├── Eczema/         (put eczema images here)
├── Healthy/        (put healthy skin images here)
├── Melanoma/       (put melanoma images here)
├── Psoriasis/      (put psoriasis images here)
└── Ringworm/       (put ringworm images here)
```

Minimum 100-200 images per class recommended.

### Step 3: Split Dataset

```bash
python prepare_dataset.py
# Choose 'y' when asked to split dataset
```

### Step 4: Train the Model

```bash
python train_model.py
```

Training will:
- Use transfer learning (MobileNetV2)
- Take 1-3 hours depending on dataset size
- Save best model automatically
- Achieve 90%+ accuracy with good dataset

## 📊 Dataset Sources

### Recommended Sources:
1. **ISIC Archive** (Melanoma): https://www.isic-archive.com/
2. **Kaggle HAM10000**: https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000
3. **DermNet NZ**: https://www.kaggle.com/datasets/shubhamgoel27/dermnet
4. **Google Images**: Search for "[disease name] skin" (ensure you have rights to use)

### Using Kaggle API:

```bash
# Install Kaggle
pip install kaggle

# Setup API key
# 1. Go to https://www.kaggle.com/account
# 2. Click "Create New API Token"
# 3. Place kaggle.json in ~/.kaggle/ (Linux/Mac) or C:\Users\<username>\.kaggle\ (Windows)

# Download datasets
kaggle datasets download -d kmader/skin-cancer-mnist-ham10000
kaggle datasets download -d shubhamgoel27/dermnet
```

## 🗂️ Project Structure

```
Multiple-Disease-Prediction-Webapp-main/
├── app.py                          # Main Streamlit app (UPDATED with Skin Disease page)
├── skin_disease_api/               # Backend API
│   ├── app.py                      # Flask REST API
│   ├── train_model.py              # Model training script
│   ├── create_initial_model.py     # Creates untrained model for testing
│   ├── prepare_dataset.py          # Dataset preparation script
│   ├── disease_info.json           # Disease information database
│   ├── requirements.txt            # API dependencies
│   ├── models/                     # Trained models
│   │   ├── skin_disease_model_final.h5
│   │   └── class_indices.json
│   ├── uploads/                    # Temporary uploaded images
│   ├── saved_predictions/          # Prediction history
│   └── dataset/                    # Training dataset
│       ├── train/
│       │   ├── Acne/
│       │   ├── Eczema/
│       │   └── ...
│       └── validation/
│           ├── Acne/
│           └── ...
└── skin_disease_assets/            # Icons, logos, etc.
```

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API status |
| `/health` | GET | Health check |
| `/predict` | POST | Image prediction |
| `/history` | GET | Prediction history |
| `/classes` | GET | List disease classes |

## 🎨 Customization

### Change Disease Classes
Edit `train_model.py`:
```python
CLASSES = ['Your', 'Custom', 'Classes']
```

### Modify Disease Information
Edit `disease_info.json` to add/update disease details.

### Adjust Model Architecture
Edit `train_model.py` to modify CNN layers, hyperparameters, etc.

## ⚠️ Important Notes

1. **Initial Model**: The `create_initial_model.py` creates an UNTRAINED model for testing. It will give random predictions until trained with real data.

2. **Model Training**: Training requires a GPU for reasonable speed. Use Google Colab if you don't have a GPU.

3. **API Server**: Keep the Flask API running in a separate terminal while using the web app.

4. **Image Quality**: Use clear, well-lit images for best results.

5. **Medical Disclaimer**: This is a screening tool, NOT a medical diagnosis. Always consult healthcare professionals.

## 🐛 Troubleshooting

### API Connection Error
- Make sure Flask API is running: `python skin_disease_api/app.py`
- Check if port 5000 is available
- Try: http://localhost:5000/health

### Model Not Found Error
- Run: `python skin_disease_api/create_initial_model.py`
- Check if `models/skin_disease_model_final.h5` exists

### Import Errors
- Install dependencies: `pip install -r skin_disease_api/requirements.txt`
- Use Python 3.8 or higher

### Low Accuracy
- Collect more training data (500+ images per class)
- Use data augmentation (already implemented)
- Train for more epochs
- Use higher quality images

## 📈 Model Performance Tips

1. **Dataset Quality**: 
   - Use diverse, high-quality images
   - Balance classes (similar number of images per class)
   - Include various lighting, angles, skin tones

2. **Training Tips**:
   - Start with transfer learning (faster, better results)
   - Use data augmentation (already implemented)
   - Monitor validation accuracy
   - Use early stopping to prevent overfitting

3. **Expected Accuracy**:
   - With 100 images/class: 70-80%
   - With 500 images/class: 85-90%
   - With 1000+ images/class: 90-95%

## 🔐 Security Considerations

- Implement file size limits (already set to 10MB)
- Validate file types (already implemented)
- Use secure file handling (already implemented)
- Don't store sensitive user data
- Add authentication for production use

## 📝 License & Disclaimer

This is an educational/research tool. NOT for clinical diagnosis.

⚕️ **Medical Disclaimer**: 
This AI system is for informational and educational purposes only. It is not intended to be a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

## 🤝 Support

For issues or questions:
1. Check this README
2. Review code comments
3. Check API logs: Look at Flask terminal output
4. Verify file paths and dependencies

## 🎉 Next Steps

1. ✅ Set up and test with initial model
2. 📊 Collect and prepare dataset
3. 🎓 Train model with real data
4. 🧪 Test with various images
5. 📈 Monitor and improve accuracy
6. 🚀 Deploy to production (optional)

---

**Created for Multiple Disease Prediction System**
Version 1.0 | November 2025
