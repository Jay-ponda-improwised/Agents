
# Use an official Python runtime as a parent image
FROM python:3.9-slim-bullseye

# Set the working directory in the container
WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Install any needed packages specified in requirements.txt using uv
COPY requirements.txt .
RUN uv pip install --system -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Run the FastAPI application
CMD ["python", "main.py"]
