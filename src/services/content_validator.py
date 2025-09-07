from src.core.config import Config
from src.core.logging import logger
from PIL import Image
from src.models.approval_status import ApprovalStatus, Status
from src.models.validation_rule import ValidationRule
from src.utils.image_analysis import calculate_red_pixel_ratio, calculate_contrast_std, calculate_skin_tone_ratio


class ContentValidator:
    """
    Validates image content against defined rules.
    
    This class coordinates the validation process but delegates
    the actual analysis to utility functions.
    """
    
    def __init__(self, config: Config):
        self.config = config
        self.rules = self._build_validation_rules()
    
    def _build_validation_rules(self) -> list[ValidationRule]:
        """Build the list of validation rules to apply."""
        return [
            ValidationRule(
                name="contrast_check",
                check_func=lambda img: calculate_contrast_std(img) >= self.config.CONTRAST_MIN,
                failure_message="Image has insufficient contrast for quality standards",
                failure_action=Status.REJECTED
            ),
            ValidationRule(
                name="skin_content_check", 
                check_func=lambda img: calculate_skin_tone_ratio(img) <= self.config.SKIN_RATIO_MAX,
                failure_message="High skin tone content detected - manual review required",
                failure_action=Status.REQUIRES_REVIEW
            ),
            ValidationRule(
                name="blood_content_check",
                check_func=lambda img: calculate_red_pixel_ratio(img) <= self.config.BLOOD_RATIO_MAX,
                failure_message="High red content detected - manual review required",
                failure_action=Status.REQUIRES_REVIEW
            ),
            # ValidationRule(
            #     name="size_check",
            #     check_func=lambda img: is_image_size_valid(img, self.config.MIN_WIDTH, self.config.MIN_HEIGHT),
            #     failure_message=f"Image must be at least {self.config.MIN_WIDTH}x{self.config.MIN_HEIGHT} pixels",
            #     failure_action=Status.REJECTED
            # )
        ]
    
    def validate_image(self, img_path: str) -> ApprovalStatus:
        """
        Validate an image against all content policy rules.
        
        Args:
            img_path: Path to the image file
            
        Returns:
            ApprovalStatus with status and reasons
        """
        outcome = ApprovalStatus(status=Status.APPROVED)
        
        try:
            img = Image.open(img_path)
        except (IOError, OSError) as e:
            logger.error(f"Failed to open image {img_path}: {e}")
            return ApprovalStatus(
                status=Status.REJECTED,
                reasons=[f"Could not process image file: {str(e)}"]
            )

        for rule in self.rules:
            if not rule.check_func(img):
                logger.info(f"Validation failed: {rule.name}")
                
                if rule.failure_action == Status.REJECTED:
                    outcome.status = Status.REJECTED
                elif outcome.status != Status.REJECTED:
                    outcome.status = Status.REQUIRES_REVIEW
                    
                outcome.reasons.append(rule.failure_message)
        
        self._log_validation_results(img_path, outcome)
        return outcome
    
    def _log_validation_results(self, img_path: str, outcome: ApprovalStatus) -> None:
        """Log the final validation results."""
        logger.info(f"Validation complete for {img_path}: {outcome.status.value}")
        if outcome.reasons:
            for reason in outcome.reasons:
                logger.info(f"  - {reason}")