from pydantic import BaseModel
from typing import TypedDict

class MetricsDict(TypedDict):
    total_requests: int
    APPROVED: int
    REJECTED: int
    REQUIRES_REVIEW: int

class Metrics(BaseModel):
    total_requests: int = 0
    total_approved_decisions: int = 0
    total_rejected_decisions: int = 0
    total_requires_review_decisions: int = 0