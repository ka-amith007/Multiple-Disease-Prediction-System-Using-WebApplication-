"""
Create a Simple Pre-trained CNN Model for Immediate Use
This creates a basic model structure - users should train with real data
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV2
import json
import os

# Configuration
IMG_SIZE = 224
NUM_CLASSES = 6
CLASSES = ['Acne', 'Eczema', 'Healthy', 'Melanoma', 'Psoriasis', 'Ringworm']

def create_model():
    """Create the CNN model architecture"""
    print("Creating model architecture...")
    
    # Load pre-trained MobileNetV2
    base_model = MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights='imagenet'
    )
    
    base_model.trainable = False
    
    # Build model
    model = keras.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.5),
        layers.Dense(512, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.4),
        layers.Dense(256, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        layers.Dense(NUM_CLASSES, activation='softmax')
    ])
    
    # Compile
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def main():
    """Create and save the initial model"""
    print("\n" + "="*70)
    print("CREATING INITIAL MODEL")
    print("="*70)
    print("\n⚠️  This creates an UNTRAINED model for testing.")
    print("For production use, train the model with real data using train_model.py")
    print("="*70 + "\n")
    
    # Create models directory
    os.makedirs('models', exist_ok=True)
    
    # Create model
    model = create_model()
    
    # Display summary
    print("\nModel Architecture:")
    model.summary()
    
    # Save model
    print("\nSaving model...")
    model.save('models/skin_disease_model_final.h5')
    model.save('models/skin_disease_model_final.keras')
    print("✓ Model saved!")
    
    # Save class indices
    class_indices = {i: cls for i, cls in enumerate(CLASSES)}
    with open('models/class_indices.json', 'w') as f:
        json.dump(class_indices, f, indent=2)
    print("✓ Class indices saved!")
    
    print("\n" + "="*70)
    print("MODEL CREATION COMPLETED")
    print("="*70)
    print("\nFiles created:")
    print("  - models/skin_disease_model_final.h5")
    print("  - models/skin_disease_model_final.keras")
    print("  - models/class_indices.json")
    print("\n⚠️  IMPORTANT: This model is UNTRAINED!")
    print("It will give random predictions until trained with real data.")
    print("\nTo train the model:")
    print("  1. Prepare dataset using: python prepare_dataset.py")
    print("  2. Train model using: python train_model.py")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
