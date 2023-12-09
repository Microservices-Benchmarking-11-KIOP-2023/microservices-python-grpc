# Use python:3.9-slim as the base image
FROM python:3.9-slim

# Set environment variable to ensure Python output is sent straight to terminal without being buffered
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container to /geo
WORKDIR /geo

# Install necessary packages
RUN apt-get update && apt-get install -y unzip

# Copy the requirements.txt file from the project root to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the geo.zip file from the geo service directory into the container
COPY services/geo/data/geo.zip .

# Unzip the geo.zip file into the data directory
RUN unzip geo.zip -d data

# Copy the rest of your geo service source code into the container
COPY services/geo .

# Specify the command to run on container start
CMD ["python", "main.py"]
