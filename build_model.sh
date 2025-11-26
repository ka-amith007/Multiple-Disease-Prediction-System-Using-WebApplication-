#!/bin/bash
echo "Building TensorFlow model..."
cd skin_disease_api
python -c "
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV2
import json
import os

os.makedirs('models', exist_ok=True)

print('Creating MobileNetV2 model...')
base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
base_model.trainable = False

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
    layers.Dense(6, activation='softmax')
])

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.save('models/skin_disease_model_final.keras')
print('✓ Model saved successfully!')

class_indices = {i: cls for i, cls in enumerate(['Acne', 'Eczema', 'Healthy', 'Melanoma', 'Psoriasis', 'Ringworm'])}
json.dump(class_indices, open('models/class_indices.json', 'w'), indent=2)
print('✓ Class indices saved!')
"
cd ..
echo "Model build complete!"
