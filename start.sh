#!/bin/bash
echo "Starting Skin Disease API..."
(cd skin_disease_api && python app.py) &

echo "Starting Streamlit App..."
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
