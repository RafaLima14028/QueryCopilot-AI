from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENROUTER_API_KEY: str

    DATABASE_URL: str

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str

    ENCRYPT_SECRET_KEY: str

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }


settings = Settings()


def get_settings() -> Settings:
    return settings
