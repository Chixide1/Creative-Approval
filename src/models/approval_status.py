from enum import Enum
from pydantic import BaseModel

class Status(str, Enum):
    APPROVED = "APPROVED",
    REJECTED = "REJECTED"
    REQUIRES_REVIEW = "REQUIRES_REVIEW"


class ApprovalStatus(BaseModel):
    status: Status
    reasons: list[str] = []