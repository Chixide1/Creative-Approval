from functools import lru_cache
from fastapi import Depends
from src.core.config import Config
from src.services.content_validator import ContentValidator

@lru_cache
def get_settings() -> Config:
    return Config()

def get_content_validator(config: Config = Depends(get_settings)) -> ContentValidator:
    return ContentValidator(config)