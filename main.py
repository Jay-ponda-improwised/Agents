import logging
from logging.config import dictConfig
from logging_config import LOGGING_CONFIG

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Import CORSMiddleware
from controller.v1_models import router as v1_models
from controller.v2_embeddings import router as v2_embeddings
from controller.v3_prompts import router as v3_prompts
from controller.users import router as users_router
from middleware.timing_middleware import TimingMiddleware

dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("") # Get the root logger

app = FastAPI(
    title="My FastAPI App",
    description="This is my awesome FastAPI application.",
    version="1.0.0",
)

# Configure CORS
origins = [
    "http://localhost:5173",  # Allow requests from your frontend development server
    "http://127.0.0.1:5173",  # Also common for local development
    "http://[::1]:5173", # Add IPv6 loopback address
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Use specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TimingMiddleware)

app.include_router(v1_models)
app.include_router(v2_embeddings)
app.include_router(v3_prompts)
app.include_router(users_router)


@app.get("/")
async def read_root():
    logger.info("Root endpoint accessed!") # Add log statement
    return {"message": "Hello, FastAPI!"}

@app.get("/healthz")
async def health_check():
    return {"status": "ok"}
