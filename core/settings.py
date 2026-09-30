from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class DBSettings(BaseSettings):
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: str
    DB_ECHO: bool


    @property
    def postgres_url(self):
       return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file='lichenid/.env', extra='ignore')

class RedisSettings(BaseSettings):
    redis_host: str
    redis_port: int
    redis_db: int

    model_config = SettingsConfigDict(env_file="lichenid/.env", env_file_encoding="utf8", extra="ignore")

    @property
    def redis_url(self):
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

class EmailSettings(BaseSettings):
    email_host: str
    email_port: int
    email_username: str
    email_password: SecretStr

    model_config = SettingsConfigDict(env_file="lichenid/.env", env_file_encoding="utf8", extra="ignore")


class S3Settings(BaseSettings):
    S3_access_key: str
    S3_url: str
    S3_secret_key: SecretStr
    S3_bucket: str
    base_url: str

    model_config = SettingsConfigDict(env_file="lichenid/.env", env_file_encoding="utf8", extra="ignore")

class Settings(BaseSettings):
    db_settings: DBSettings = DBSettings()
    email_settings: EmailSettings = EmailSettings()
    S3_settings: S3Settings = S3Settings()
    redis_settings: RedisSettings = RedisSettings()
    secret_key: SecretStr
    access_token_expire: int
    templates_dir: str = "lichenid/templates"
    frontend_url: str

    model_config = SettingsConfigDict(env_file="lichenid/.env", env_file_encoding="utf8", extra="ignore")


settings = Settings()