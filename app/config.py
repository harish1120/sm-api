from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_TYPE: str
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    SECURITY_KEY: str
    ALGORITHM: str
    EXPIRE_IN: int

    class Config: 
        env_file = ".env"


settings = Settings()