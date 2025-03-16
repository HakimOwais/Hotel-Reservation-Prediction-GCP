# Use a lightweight Python image as the base image
FROM python:slim

# Set environment variables:
# - PYTHONDONTWRITEBYTECODE=1 prevents Python from writing .pyc files (cached bytecode files)
# - PYTHONUNBUFFERED=1 ensures that Python output is displayed immediately (useful for logging)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app  # Corrected from "WORDIR" to "WORKDIR"

# Update package lists and install required system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Dependency required for LightGBM or similar libraries
    libgomp1 \  
    # Remove unnecessary package data to reduce image size
    && apt-get clean \  
    # Free up space by deleting cached package lists
    && rm -rf /var/lib/apt/lists/* 
     
# Copy all project files into the container
COPY . .

# Install Python dependencies from the project's setup file (editable mode)
RUN pip install --no-cache-dir -e .

# Run the training pipeline before starting the application
RUN python pipeline/training_pipeline.py

# Expose port 8000 to allow external access to the application
EXPOSE 8000

# Set the default command to run the application API
CMD ["python", "application/api.py"]
