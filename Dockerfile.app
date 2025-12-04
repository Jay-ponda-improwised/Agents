# Application Dockerfile that uses the base image
# Build with: docker build -t langchain-base -f Dockerfile.base .
# Then: docker build -t langchain-api .

# Use the base image (you'll need to build it first)
FROM langchain-base

# Set working directory
WORKDIR /app

# Update PATH to include the conda environment
ENV PATH=/opt/conda/envs/langchain_env/bin:$PATH

# Copy application code
COPY . .

# Expose the port FastAPI will run on
EXPOSE 33001

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "33001"]