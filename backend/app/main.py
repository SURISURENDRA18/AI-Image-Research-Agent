from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="AI Image Research Agent",
    description="Analyze images using AI and extract insights",
    version="1.0.0"
)

# Include routes
app.include_router(router)

# Root endpoint (fixes your 404)
@app.get("/")
def home():
    return {
        "status": "running",
        "message": "AI Image Research Agent API is live",
        "docs": "/docs"
    }

# Health check (useful for debugging / deployment)
@app.get("/health")
def health_check():
    return {"status": "ok"}
