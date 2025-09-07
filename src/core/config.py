from pydantic_settings import BaseSettings

class Config(BaseSettings):
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

    class Config:
        env_file = ".env"