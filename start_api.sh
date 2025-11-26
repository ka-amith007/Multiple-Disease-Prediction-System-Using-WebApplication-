#!/bin/bash

echo "===================================================================="
echo "   SKIN DISEASE PREDICTION SYSTEM - STARTUP"
echo "===================================================================="
echo ""

# Check if we're in the right directory
if [ ! -d "skin_disease_api" ]; then
    echo "Error: skin_disease_api folder not found!"
    echo "Please run this script from the project root directory."
    exit 1
fi

echo "Step 1: Checking dependencies..."
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Please run the main app first."
    exit 1
fi

echo "Step 2: Setting up Flask API..."
echo ""

# Navigate to API directory
cd skin_disease_api

# Check if model exists
if [ ! -f "models/skin_disease_model_final.h5" ]; then
    echo "[WARNING] AI Model not found!"
    echo ""
    echo "Creating initial model structure..."
    echo ""
    ../.venv/bin/python create_initial_model.py
    echo ""
    echo "[INFO] Initial model created. This is an UNTRAINED model for testing."
    echo "[INFO] For production use, train the model with real data."
    echo ""
    read -p "Press Enter to continue..."
fi

echo ""
echo "===================================================================="
echo "   STARTING FLASK API SERVER"
echo "===================================================================="
echo ""
echo "API will start at: http://localhost:5000"
echo ""
echo "IMPORTANT: Keep this terminal open while using the app!"
echo ""
echo "To stop the server: Press Ctrl+C"
echo ""
echo "===================================================================="
echo ""

# Start Flask API
../.venv/bin/python app.py

# If Flask exits
echo ""
echo "API server stopped."
