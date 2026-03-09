from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    APP_NAME: str = "MicroQuant API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # CORS
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    # Image Processing
    TARGET_RESOLUTION: tuple[int, int] = (550, 672)
    CANNY_SIGMA: float = 0.1
    PLATE_WIDTH_OFFSET: int = 40
    GAUSSIAN_SIGMA: int = 2
    MIN_PEAK_DISTANCE: int = 2
    MAX_PEAKS_PER_LABEL: int = 10

    class Config:
        env_file = ".env"


settings = Settings()
