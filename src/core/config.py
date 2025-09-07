from pydantic_settings import BaseSettings

class Config(BaseSettings):
    CONTRAST_MIN: int = 60
    BLOOD_RATIO_MAX: float = 0.15
    SKIN_RATIO_MAX: float = 0.35

    class Config:
        env_file = ".env"