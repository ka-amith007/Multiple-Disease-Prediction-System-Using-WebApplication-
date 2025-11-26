"""
Flask REST API for Skin Disease Prediction
Handles image upload, CNN prediction, and response generation
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image
import os
import json
import uuid
from datetime import datetime
import traceback

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
SAVED_PREDICTIONS_FOLDER = 'saved_predictions'
MODEL_PATH = 'models/skin_disease_model_final.keras'
DISEASE_INFO_PATH = 'disease_info.json'
CLASS_INDICES_PATH = 'models/class_indices.json'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
IMG_SIZE = 224

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SAVED_PREDICTIONS_FOLDER, exist_ok=True)

# Load model and data
print("Loading AI model...")
try:
    model = keras.models.load_model(MODEL_PATH)
    print("✓ Model loaded successfully!")
except Exception as e:
    print(f"✗ Error loading model: {str(e)}")
    model = None

# Load disease information
print("Loading disease information database...")
try:
    with open(DISEASE_INFO_PATH, 'r', encoding='utf-8') as f:
        disease_info = json.load(f)
    print("✓ Disease info loaded successfully!")
except Exception as e:
    print(f"✗ Error loading disease info: {str(e)}")
    disease_info = {}

# Load class indices
print("Loading class indices...")
try:
    with open(CLASS_INDICES_PATH, 'r') as f:
        class_indices = json.load(f)
    # Convert keys to integers
    class_indices = {int(k): v for k, v in class_indices.items()}
    print(f"✓ Class indices loaded: {class_indices}")
except Exception as e:
    print(f"⚠️  Using default class indices")
    class_indices = {
        0: 'Acne',
        1: 'Eczema',
        2: 'Healthy',
        3: 'Melanoma',
        4: 'Psoriasis',
        5: 'Ringworm'
    }

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image_path):
    """Preprocess image for model prediction"""
    try:
        # Load image with faster resampling
        img = Image.open(image_path)
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize with faster BILINEAR method instead of default LANCZOS
        img = img.resize((IMG_SIZE, IMG_SIZE), Image.BILINEAR)
        
        # Convert to array and normalize in one step
        img_array = np.array(img, dtype=np.float32) / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    
    except Exception as e:
        raise Exception(f"Error preprocessing image: {str(e)}")

def predict_disease(image_path):
    """Make prediction using the CNN model"""
    try:
        if model is None:
            raise Exception("Model not loaded. Please train the model first.")
        
        # Preprocess image
        img_array = preprocess_image(image_path)
        
        # Make prediction with optimized settings
        predictions = model.predict(img_array, verbose=0, batch_size=1)
        
        # Get predicted class and confidence
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx]) * 100
        
        # Get class name
        predicted_class = class_indices.get(predicted_class_idx, 'Unknown')
        
        # Get all probabilities
        all_probabilities = {}
        for idx, prob in enumerate(predictions[0]):
            class_name = class_indices.get(idx, f'Class_{idx}')
            all_probabilities[class_name] = float(prob) * 100
        
        return {
            'predicted_class': predicted_class,
            'confidence': confidence,
            'all_probabilities': all_probabilities
        }
    
    except Exception as e:
        raise Exception(f"Prediction error: {str(e)}")

def get_disease_details(disease_name):
    """Get disease information from database"""
    try:
        if disease_name in disease_info:
            return disease_info[disease_name]
        else:
            return {
                'name': disease_name,
                'symptoms': ['Information not available'],
                'causes': ['Information not available'],
                'precautions': ['Consult a dermatologist'],
                'treatments': ['Seek professional medical advice']
            }
    except Exception as e:
        return {
            'name': disease_name,
            'symptoms': ['Error loading information'],
            'causes': ['Error loading information'],
            'precautions': ['Consult a dermatologist'],
            'treatments': ['Seek professional medical advice']
        }

def save_prediction_history(prediction_data):
    """Save prediction to history"""
    try:
        history_file = os.path.join(SAVED_PREDICTIONS_FOLDER, 'prediction_history.json')
        
        # Load existing history
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                history = json.load(f)
        else:
            history = []
        
        # Add new prediction
        history.append(prediction_data)
        
        # Keep only last 100 predictions
        history = history[-100:]
        
        # Save updated history
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Error saving prediction history: {str(e)}")
        return False

@app.route('/')
def home():
    """API home endpoint"""
    return jsonify({
        'status': 'online',
        'message': 'Skin Disease Prediction API',
        'version': '1.0',
        'model_loaded': model is not None,
        'endpoints': {
            'predict': '/predict (POST)',
            'health': '/health (GET)',
            'history': '/history (GET)',
            'classes': '/classes (GET)'
        }
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/classes')
def get_classes():
    """Get list of disease classes"""
    return jsonify({
        'classes': list(class_indices.values()),
        'num_classes': len(class_indices)
    })

@app.route('/history')
def get_history():
    """Get prediction history"""
    try:
        history_file = os.path.join(SAVED_PREDICTIONS_FOLDER, 'prediction_history.json')
        
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                history = json.load(f)
            return jsonify({
                'success': True,
                'count': len(history),
                'history': history
            })
        else:
            return jsonify({
                'success': True,
                'count': 0,
                'history': []
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/predict', methods=['POST'])
def predict():
    """Main prediction endpoint"""
    try:
        # Check if model is loaded
        if model is None:
            return jsonify({
                'success': False,
                'error': 'Model not loaded. Please train the model first.',
                'message': 'Run train_model.py to create the AI model.'
            }), 500
        
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file uploaded',
                'message': 'Please upload an image file.'
            }), 400
        
        file = request.files['file']
        
        # Check if filename is empty
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected',
                'message': 'Please select an image file.'
            }), 400
        
        # Check file extension
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Invalid file type',
                'message': f'Allowed file types: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Generate unique filename
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save uploaded file
        file.save(filepath)
        
        # Make prediction
        prediction_result = predict_disease(filepath)
        
        # Get disease details
        disease_details = get_disease_details(prediction_result['predicted_class'])
        
        # Prepare response
        response_data = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'prediction': {
                'disease': prediction_result['predicted_class'],
                'confidence': round(prediction_result['confidence'], 2),
                'all_probabilities': {k: round(v, 2) for k, v in prediction_result['all_probabilities'].items()}
            },
            'details': disease_details,
            'image_id': unique_filename,
            'disclaimer': 'This is an AI-based screening tool and not a confirmed medical diagnosis. Please consult a dermatologist for proper diagnosis and treatment.'
        }
        
        # Save to history
        save_prediction_history({
            'timestamp': response_data['timestamp'],
            'disease': prediction_result['predicted_class'],
            'confidence': round(prediction_result['confidence'], 2),
            'image_id': unique_filename
        })
        
        # Optional: Save a copy to saved_predictions
        saved_copy_path = os.path.join(SAVED_PREDICTIONS_FOLDER, unique_filename)
        try:
            Image.open(filepath).save(saved_copy_path)
        except:
            pass
        
        return jsonify(response_data)
    
    except Exception as e:
        # Log error
        print(f"Error in prediction: {str(e)}")
        print(traceback.format_exc())
        
        return jsonify({
            'success': False,
            'error': 'Prediction failed',
            'message': str(e),
            'disclaimer': 'Please try again or consult a dermatologist.'
        }), 500

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({
        'success': False,
        'error': 'File too large',
        'message': f'Maximum file size is {MAX_FILE_SIZE // (1024*1024)}MB'
    }), 413

@app.errorhandler(500)
def internal_error(e):
    """Handle internal server error"""
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'message': str(e)
    }), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('API_PORT', 5001))
    
    print("\n" + "="*70)
    print("SKIN DISEASE PREDICTION API")
    print("="*70)
    print(f"Model Status: {'✓ Loaded' if model else '✗ Not Loaded'}")
    print(f"Disease Classes: {list(class_indices.values())}")
    print(f"Upload Folder: {UPLOAD_FOLDER}")
    print(f"Max File Size: {MAX_FILE_SIZE // (1024*1024)}MB")
    print(f"Port: {port}")
    print("="*70)
    print("\nStarting Flask server...")
    print(f"API will be available at: http://0.0.0.0:{port}")
    print("="*70 + "\n")
    
    # Run without debug mode to avoid reloader issues
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
