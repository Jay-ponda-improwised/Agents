
# Use an official Python runtime as a parent image
FROM continuumio/miniconda3:latest

RUN conda install -n base -c conda-forge mamba -y

RUN apt-get update && apt-get install -y curl postgresql-client && rm -rf /var/lib/apt/lists/*



# Set the working directory in the container
WORKDIR /app

# Copy and install environment
COPY environment.yml .
RUN mamba env create -f environment.yml

# Activate the environment and install remaining packages with uv
SHELL ["conda", "run", "-n", "langchain_env", "/bin/bash", "-c"]
ENV PATH="/opt/conda/envs/langchain_env/bin:$PATH"

# Copy the current directory contents into the container at /app
COPY . .

# Run the FastAPI application
CMD ["conda", "run", "-n", "langchain_env", "python", "main.py"]
