# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY app/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files into the container
COPY app /app

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to start the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
