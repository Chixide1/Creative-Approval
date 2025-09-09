from pydantic import BaseModel, Field
from typing import TypedDict

class MetricsDict(TypedDict):
    total_requests: int
    APPROVED: int
    REJECTED: int
    REQUIRES_REVIEW: int

class Metrics(BaseModel):
    total_requests: int = Field(
        default=0,
        description="Total number of requests processed",
        ge=0
    )
    total_approved_decisions: int = Field(
        default=0,
        description="Total number of items that were approved",
        ge=0
    )
    total_rejected_decisions: int = Field(
        default=0,
        description="Total number of items that were rejected",
        ge=0
    )
    total_requires_review_decisions: int = Field(
        default=0,
        description="Total number of items that require manual review",
        ge=0
    )