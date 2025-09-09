from enum import Enum
from pydantic import BaseModel, Field

class ImageInfo(BaseModel):
    width: int
    height: int
    format: str = Field(examples=["JPEG", "PNG", "GIF", "JPG"])
    size: str 

class Status(str, Enum):
    APPROVED = "APPROVED",
    REJECTED = "REJECTED"
    REQUIRES_REVIEW = "REQUIRES_REVIEW"


class ApprovalStatus(BaseModel):
    status: Status
    reasons: list[str] = Field(
        default=[],
        examples=[
            "Image has insufficient contrast for quality standards",
            "High skin tone content detected - manual review required",
            "High red content detected - manual review required",
            "The following list of words are prohibited: guns, weapons, nudity",
        ]
    )
    image_info: ImageInfo | None = None