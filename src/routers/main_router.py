from fastapi import APIRouter, Depends, HTTPException, UploadFile
from src.core.dependencies import get_content_validator
import tempfile
import os
from pathlib import Path
from src.services.content_validator import ContentValidator


router = APIRouter(tags=["Approval"])

@router.post("/creative-approval")
def submit_creative_for_approval(
    file: UploadFile,
    validator: ContentValidator = Depends(get_content_validator)
):
    approved_formats = (".png", ".jpeg", ".jpg", ".gif")

    if not file.filename or not file.filename.endswith(approved_formats):
        raise HTTPException(
            status_code=422,
            detail=f"{file.filename} has an invalid file format. Allowed formats are {', '.join(approved_formats)}"
        )

    filename = Path(file.filename)
    with tempfile.NamedTemporaryFile(delete=False, suffix=filename.suffix) as temp_file:
        temp_file.write(file.file.read())
        temp_file_path = temp_file.name
    
    try:
        result = validator.validate_image(temp_file_path)
        
    finally:
        os.unlink(temp_file_path)   

    return result

@router.get("/health")
def get_health_status():
    return