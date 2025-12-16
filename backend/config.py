"""Configuration management for Marlene smart home assistant."""
import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    porcupine_access_key: str
    deepgram_api_key: str
    
    # Audio settings
    audio_rate: int = 16000
    audio_chunk_size: int = 1024
    audio_channels: int = 1
    
    # Porcupine settings
    porcupine_keyword: str = "porcupine"  # Built-in keyword
    porcupine_sensitivity: float = 0.5
    
    # Deepgram settings
    deepgram_model: str = "nova-2"
    deepgram_language: str = "en-US"
    
    # Server settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


# Global settings instance
settings = Settings()
