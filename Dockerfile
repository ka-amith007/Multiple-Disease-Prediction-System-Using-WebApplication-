FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements-deploy.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-deploy.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p skin_disease_api/uploads skin_disease_api/saved_predictions

# Expose ports
EXPOSE 8501 5001

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run both Streamlit and Flask API
CMD streamlit run app.py --server.port=8501 --server.address=0.0.0.0 & \
    cd skin_disease_api && python app.py
