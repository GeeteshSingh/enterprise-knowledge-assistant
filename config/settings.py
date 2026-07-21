from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables and .env file.

    All fields can be overridden by setting the corresponding environment
    variable or adding the key to a .env file in the project root.

    Fields:
        GEMINI_API_KEY:  API key for Gemini LLM. Required only for the /ask
                         endpoint and RAG pipeline. Optional for all other features.
        DATA_DIR:        Path to the directory containing .txt document files.
        TOP_K:           Number of top results to return from semantic search.
        LOG_LEVEL:       Logging level for the application logger.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    GEMINI_API_KEY: str = ""
    DATA_DIR: str = "data"
    TOP_K: int = 5
    LOG_LEVEL: str = "INFO"

    @property
    def data_path(self) -> Path:
        """Returns DATA_DIR as a Path object."""
        return Path(self.DATA_DIR)

    @property
    def llm_available(self) -> bool:
        """Returns True if a Gemini API key has been configured."""
        return bool(self.GEMINI_API_KEY.strip())


settings = Settings()
