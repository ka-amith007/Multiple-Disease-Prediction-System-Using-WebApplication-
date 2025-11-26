#!/bin/bash
echo "Building model if not exists..."
bash build_model.sh

echo "Starting Skin Disease API in background..."
export API_PORT=5001
(cd skin_disease_api && python app.py > /tmp/api.log 2>&1) &
API_PID=$!
echo "API started with PID: $API_PID"

echo "Waiting for API to initialize..."
sleep 5

echo "Starting Streamlit App on port $PORT..."
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
