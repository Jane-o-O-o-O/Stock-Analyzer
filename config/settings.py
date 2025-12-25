"""Application settings loader using environment variables."""
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    tushare_token: str = os.getenv("TUSHARE_TOKEN", "")
    siliconflow_api_key: str = os.getenv("SILICONFLOW_API_KEY", "")
    siliconflow_model: str = os.getenv("SILICONFLOW_MODEL", "")
    mongodb_uri: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    mongodb_db: str = os.getenv("MONGODB_DB", "stock_analyzer")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()


def validate_settings() -> None:
    missing = []
    if not settings.tushare_token:
        missing.append("TUSHARE_TOKEN")
    if not settings.siliconflow_api_key:
        missing.append("SILICONFLOW_API_KEY")
    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")
