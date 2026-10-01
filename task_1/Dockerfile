FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Pre-download models to bake them into the image for faster cold starts.
RUN python -c "from transformers import BlipProcessor, BlipForConditionalGeneration; BlipProcessor.from_pretrained('Salesforce/blip-image-captioning-base'); BlipForConditionalGeneration.from_pretrained('Salesforce/blip-image-captioning-base')"
RUN python -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification; AutoTokenizer.from_pretrained('martin-ha/toxic-comment-model'); AutoModelForSequenceClassification.from_pretrained('martin-ha/toxic-comment-model')"

EXPOSE 8501

# Command to run the application, using the port provided by Render
CMD ["sh", "-c", "streamlit run app.py --server.port=$PORT --server.address=0.0.0.0"]