@echo off
echo ====================================================================
echo    SKIN DISEASE PREDICTION SYSTEM - STARTUP
echo ====================================================================
echo.

REM Check if we're in the right directory
if not exist "skin_disease_api" (
    echo Error: skin_disease_api folder not found!
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

echo Step 1: Checking dependencies...
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo Virtual environment not found. Please run the main app first.
    pause
    exit /b 1
)

echo Step 2: Setting up Flask API...
echo.

REM Navigate to API directory
cd skin_disease_api

REM Check if model exists
if not exist "models\skin_disease_model_final.h5" (
    echo [WARNING] AI Model not found!
    echo.
    echo Creating initial model structure...
    echo.
    "..\\.venv\Scripts\python.exe" create_initial_model.py
    echo.
    echo [INFO] Initial model created. This is an UNTRAINED model for testing.
    echo [INFO] For production use, train the model with real data.
    echo.
    pause
)

echo.
echo ====================================================================
echo    STARTING FLASK API SERVER
echo ====================================================================
echo.
echo API will start at: http://localhost:5000
echo.
echo IMPORTANT: Keep this window open while using the app!
echo.
echo To stop the server: Press Ctrl+C
echo.
echo ====================================================================
echo.

REM Start Flask API
"..\\.venv\Scripts\python.exe" app.py

REM If Flask exits
echo.
echo API server stopped.
pause
