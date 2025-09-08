from src.core.config import Config
from src.core.logging import logger
from PIL import Image
from src.models.approval_status import ApprovalStatus, Status
from src.models.validation_rule import ValidationRule
from src.utils.image_analysis import calculate_blood_pixel_ratio, calculate_contrast_std, calculate_skin_tone_ratio


class ContentValidator:
    """
    Validates image content against defined rules.
    
    This class coordinates the validation process but delegates
    the actual analysis to utility functions.
    """
    
    def __init__(self, config: Config):
        self.config = config
        self.rules = self._build_validation_rules()

    def validate_content(self, img_path: str, metadata: str | None) -> ApprovalStatus:
        """
        Validate both image and metadata content.
        """

        combined_result = ApprovalStatus(status=Status.APPROVED)
        all_reasons: list[str] = []
        
        if metadata:
            metadata_result = self.validate_metadata(metadata)
            all_reasons.extend(metadata_result.reasons)
            
            if metadata_result.status == Status.REJECTED:
                combined_result.status = Status.REJECTED
            elif metadata_result.status == Status.REQUIRES_REVIEW:
                combined_result.status = Status.REQUIRES_REVIEW
        
        image_result = self.validate_image(img_path)
        all_reasons.extend(image_result.reasons)
        
        if image_result.status == Status.REJECTED:
            combined_result.status = Status.REJECTED
        elif image_result.status == Status.REQUIRES_REVIEW and combined_result.status != Status.REJECTED:
            combined_result.status = Status.REQUIRES_REVIEW
        
        combined_result.reasons = all_reasons
        
        self._log_combined_validation_results(img_path, combined_result, metadata is not None)
        return combined_result

    def validate_metadata(self, metadata: str) -> ApprovalStatus:
        """Validate metadata against prohibited keywords."""

        metadata_words = [word.strip() for word in metadata.split(',') if word.strip()]
        
        flagged_words: list[str] = []
        logger.info(f"metadata: {metadata_words}")

        for word in metadata_words:
            if word.lower() in self.config.PROHIBITED_KEYWORDS:
                flagged_words.append(word)
        
        if flagged_words:
            logger.info(f"Metadata Validation Failed. Words flagged were: {flagged_words}")
            status = ApprovalStatus(status=Status.REJECTED)
            status.reasons.append(f"The following list of words are prohibited: {", ".join(flagged_words)}")
            return status
        
        logger.info(f"Metadata Validation Passed.")
        return ApprovalStatus(status=Status.APPROVED)

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
                check_func=lambda img: calculate_blood_pixel_ratio(img) <= self.config.BLOOD_RATIO_MAX,
                failure_message="High red content detected - manual review required",
                failure_action=Status.REQUIRES_REVIEW
            ),
        ]
    
    def validate_image(self, img_path: str) -> ApprovalStatus:
        """
        Validate an image against all content policy rules.
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
        
        return outcome
    
    def _log_validation_results(self, img_path: str, outcome: ApprovalStatus) -> None:
        """Log the final validation results."""
        logger.info(f"Validation complete for {img_path}: {outcome.status.value}")
        if outcome.reasons:
            for reason in outcome.reasons:
                logger.info(f"  - {reason}")

    def _log_combined_validation_results(self, img_path: str, outcome: ApprovalStatus, had_metadata: bool) -> None:
        """Log the combined validation results."""
        validation_types = "image and metadata" if had_metadata else "image"
        logger.info(f"Combined {validation_types} validation complete for {img_path}: {outcome.status.value}")
        if outcome.reasons:
            for reason in outcome.reasons:
                logger.info(f"  - {reason}")