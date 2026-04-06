from fastapi import APIRouter, UploadFile, File
from app.agent import run_agent

router = APIRouter()

@router.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = run_agent(image_bytes)
    return result
