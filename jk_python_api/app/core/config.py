# Core configuration

from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = 'postgresql+asyncpg://postgres:postgres@localhost:5432/booksdb'
    SECRET_KEY: str = 'supersecretkey'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    LLAMA3_API_URL: str = 'http://localhost:11434/api/generate'  # Example for Ollama

    class Config:
        env_file = '.env'

settings = Settings()
