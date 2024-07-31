# Use the official Python 3.8 image
FROM python:3.6-slim

# Set the working directory
WORKDIR /app

# Install system dependencies for building packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libatlas-base-dev \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


# Fix the print statement in the azimuth package
RUN sed -i 's/print "/print("/g; s/")/")/g' /usr/local/lib/python3.6/site-packages/azimuth/model_comparison.py

# Copy the rest of the application code to the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=/app/server/App.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Start the Flask application
ENTRYPOINT ["flask", "run"]
