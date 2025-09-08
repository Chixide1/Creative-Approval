import os
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.params import Form
from src.core.dependencies import get_content_validator
import tempfile
from pathlib import Path
from src.models.approval_status import ApprovalStatus
from src.models.health_status import HealthStatus
from src.services.content_validator import ContentValidator
from src.core.logging import logger

router = APIRouter(tags=["Approval"])

@router.post("/creative-approval")
def submit_creative_for_approval(
    file: UploadFile,
    metadata: Annotated[str | None, Form()] = None,
    validator: ContentValidator = Depends(get_content_validator)
) -> ApprovalStatus:
    approved_formats = (".png", ".jpeg", ".jpg", ".gif")

    if not file.filename or not file.filename.lower().endswith(approved_formats):
        raise HTTPException(
            status_code=422,
            detail=f"{file.filename} has an invalid file format. Allowed formats are {', '.join(approved_formats)}"
        )

    temp_file_path = None
    try:
        filename = Path(file.filename)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=filename.suffix) as temp_file:
            temp_file.write(file.file.read())
            temp_file_path = temp_file.name
        
        result = validator.validate_content(temp_file_path, metadata)
        return result
        
    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process uploaded file: {str(e)}"
        )
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except:
                pass

@router.get("/health")
def get_health_status() -> HealthStatus:
    return HealthStatus()