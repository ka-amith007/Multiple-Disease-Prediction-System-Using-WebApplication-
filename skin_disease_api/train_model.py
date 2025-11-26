"""
Skin Disease Classification Model - Training Script
Uses CNN architecture with Transfer Learning (MobileNetV2)
Classes: Acne, Eczema, Psoriasis, Ringworm, Melanoma, Healthy
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import numpy as np
import os

# Configuration
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 50
CLASSES = ['Acne', 'Eczema', 'Healthy', 'Melanoma', 'Psoriasis', 'Ringworm']
NUM_CLASSES = len(CLASSES)
DATASET_PATH = 'dataset'  # Should contain train/ and validation/ folders

# Data Augmentation for better generalization
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    vertical_flip=True,
    fill_mode='nearest'
)

validation_datagen = ImageDataGenerator(rescale=1./255)

print("Loading training data...")
train_generator = train_datagen.flow_from_directory(
    os.path.join(DATASET_PATH, 'train'),
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=True
)

print("Loading validation data...")
validation_generator = validation_datagen.flow_from_directory(
    os.path.join(DATASET_PATH, 'validation'),
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False
)

# Build CNN Model with Transfer Learning
def create_model():
    # Load pre-trained MobileNetV2 model
    base_model = MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze the base model initially
    base_model.trainable = False
    
    # Build the model
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
    
    return model, base_model

print("Creating model...")
model, base_model = create_model()

# Compile the model
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy', keras.metrics.AUC(), keras.metrics.Precision(), keras.metrics.Recall()]
)

model.summary()

# Callbacks
checkpoint = ModelCheckpoint(
    'models/skin_disease_model_best.h5',
    monitor='val_accuracy',
    save_best_only=True,
    mode='max',
    verbose=1
)

early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True,
    verbose=1
)

reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.2,
    patience=5,
    min_lr=0.00001,
    verbose=1
)

callbacks = [checkpoint, early_stopping, reduce_lr]

# First training phase with frozen base
print("\n" + "="*70)
print("PHASE 1: Training with frozen base model")
print("="*70 + "\n")

history1 = model.fit(
    train_generator,
    epochs=20,
    validation_data=validation_generator,
    callbacks=callbacks,
    verbose=1
)

# Second training phase - Fine-tuning
print("\n" + "="*70)
print("PHASE 2: Fine-tuning - Unfreezing top layers")
print("="*70 + "\n")

# Unfreeze the top layers of the base model
base_model.trainable = True

# Fine-tune from this layer onwards
fine_tune_at = 100

# Freeze all layers before the `fine_tune_at` layer
for layer in base_model.layers[:fine_tune_at]:
    layer.trainable = False

# Recompile with lower learning rate
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy', keras.metrics.AUC(), keras.metrics.Precision(), keras.metrics.Recall()]
)

# Continue training
history2 = model.fit(
    train_generator,
    epochs=EPOCHS,
    initial_epoch=history1.epoch[-1],
    validation_data=validation_generator,
    callbacks=callbacks,
    verbose=1
)

# Save final model
print("\nSaving final model...")
model.save('models/skin_disease_model_final.h5')
model.save('models/skin_disease_model_final.keras')

# Convert to TFLite for mobile deployment (optional)
print("\nConverting to TFLite...")
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open('models/skin_disease_model.tflite', 'wb') as f:
    f.write(tflite_model)

# Evaluate the model
print("\n" + "="*70)
print("FINAL EVALUATION")
print("="*70 + "\n")

results = model.evaluate(validation_generator)
print(f"\nFinal Validation Loss: {results[0]:.4f}")
print(f"Final Validation Accuracy: {results[1]:.4f}")
print(f"Final Validation AUC: {results[2]:.4f}")
print(f"Final Validation Precision: {results[3]:.4f}")
print(f"Final Validation Recall: {results[4]:.4f}")

# Save class indices for later use
import json
class_indices = train_generator.class_indices
# Invert the dictionary
index_to_class = {v: k for k, v in class_indices.items()}

with open('models/class_indices.json', 'w') as f:
    json.dump(index_to_class, f)

print("\nClass indices saved!")
print(f"Classes: {index_to_class}")

print("\n" + "="*70)
print("Training completed successfully!")
print("Models saved:")
print("  - models/skin_disease_model_best.h5")
print("  - models/skin_disease_model_final.h5")
print("  - models/skin_disease_model_final.keras")
print("  - models/skin_disease_model.tflite")
print("  - models/class_indices.json")
print("="*70)
