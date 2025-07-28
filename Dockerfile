# Use Python 3.9 slim base image with amd64 platform
FROM --platform=linux/amd64 python:3.9-slim

# Set working directory in container
WORKDIR /app

# Copy current directory contents into container
COPY . /app

# Install system dependencies for PyMuPDF and others 
RUN apt-get update && apt-get install -y \
    build-essential \
    libmupdf-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download sentence-transformers model to avoid internet at runtime
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Default command to run main.py
ENTRYPOINT ["python", "main.py"]
