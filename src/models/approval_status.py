from enum import Enum
from pydantic import BaseModel, Field

class ImageInfo(BaseModel):
    width: int = Field(..., description="Width of the image in pixels", gt=0)
    height: int = Field(..., description="Height of the image in pixels", gt=0)
    format: str = Field(..., description="Image file format", examples=["JPEG", "PNG", "GIF", "JPG"])
    size: str = Field(..., description="File size in bytes")

class Status(str, Enum):
    APPROVED = "APPROVED",
    REJECTED = "REJECTED"
    REQUIRES_REVIEW = "REQUIRES_REVIEW"


class ApprovalStatus(BaseModel):
    status: Status = Field(..., description="The approval decision for the content")
    reasons: list[str] = Field(
        default_factory=list,
        description="List of reasons explaining the approval decision",
        examples=[
            "Image has insufficient contrast for quality standards",
            "High skin tone content detected - manual review required", 
            "High red content detected - manual review required",
            "The following list of words are prohibited: guns, weapons, nudity",
        ]
    )
    image_info: ImageInfo | None = Field(
        default=None, 
        description="Metadata about the image being reviewed"
    )