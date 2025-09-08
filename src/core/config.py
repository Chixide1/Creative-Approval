from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    
    CONTRAST_MIN: int = 60
    BLOOD_RATIO_MAX: float = 0.15
    SKIN_RATIO_MAX: float = 0.35
    PROHIBITED_KEYWORDS: list[str] = [
        "tobacco", "cigarettes", "weapons", "guns", "political extremist",
        "prostitution", "sexual massage", "pyramid scheme", "escort", "lap-dancing",
        "gentlemen's club", "nudity", "sexual imagery", "violence", "drugs",
        "blood", "swear", "prescription medicine", "infant formula", "controversy",
        "pr stunt", "hate", "discrimination", "incite violence", "harassment",
        "bullying", "extremist", "illegal activity",
    ]