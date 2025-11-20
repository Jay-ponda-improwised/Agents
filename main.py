import logging
import asyncio
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from controller.v1_models import router as v1_models
from controller.v2_embeddings import router as v2_embeddings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context Manager for managing the lifespan of the FastAPI application.
    Handles startup and shutdown events, including Docker Compose operations.
    """
    logger.info("Application startup event triggered.")

    # Docker Compose Up
    logger.info("Attempting to start Docker Compose services...")
    process = await asyncio.create_subprocess_shell(
        "docker-compose up -d",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=os.getcwd()  # Ensure command runs in the project root
    )
    stdout, stderr = await process.communicate()

    if process.returncode == 0:
        logger.info(f"Docker Compose services started successfully:\n{stdout.decode().strip()}")
    else:
        logger.error(f"Failed to start Docker Compose services. Stdout: {stdout.decode().strip()}, Stderr: {stderr.decode().strip()}")
        # Depending on requirements, you might want to raise an exception here
        # or handle this failure more gracefully without stopping the app startup.

    yield

    # Docker Compose Down
    logger.info("Application shutdown event triggered.")
    logger.info("Attempting to stop Docker Compose services...")
    process = await asyncio.create_subprocess_shell(
        "docker-compose down",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=os.getcwd()  # Ensure command runs in the project root
    )
    stdout, stderr = await process.communicate()

    if process.returncode == 0:
        logger.info(f"Docker Compose services stopped successfully:\n{stdout.decode().strip()}")
    else:
        logger.error(f"Failed to stop Docker Compose services. Stdout: {stdout.decode().strip()}, Stderr: {stderr.decode().strip()}")
    
app = FastAPI(
    title="My FastAPI App",
    description="This is my awesome FastAPI application.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(v1_models)
app.include_router(v2_embeddings)


@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=33001)
