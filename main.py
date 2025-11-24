import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Import CORSMiddleware
from controller.v1_models import router as v1_models
from controller.v2_embeddings import router as v2_embeddings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
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

app.include_router(v1_models)
app.include_router(v2_embeddings)


@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/healthz")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=33001, reload=True)
