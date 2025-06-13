# Use an official lightweight Python image
FROM python:3.10-slim

# Install system dependencies (Tesseract + libraries)
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        tesseract-ocr \
        tesseract-ocr-eng \
        libtesseract-dev \
        libleptonica-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variable for Tesseract language data
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata

# Set work directory
WORKDIR /app

# Copy requirement files first for caching
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Command to run the Streamlit app. Render will inject the PORT env variable.
CMD ["sh", "-c", "streamlit run app.py --server.port $PORT --server.address 0.0.0.0"] 