from PIL import Image
from typing import Callable
from src.models.approval_status import Status

class ValidationRule:
    """Represents a single validation rule with its logic and metadata."""
    
    def __init__(
        self, name: str, check_func: Callable[[Image.Image], bool], 
        failure_message: str, failure_action: Status = Status.REQUIRES_REVIEW
    ):
        self.name = name
        self.check_func = check_func
        self.failure_message = failure_message
        self.failure_action = failure_action