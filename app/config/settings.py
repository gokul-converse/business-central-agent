import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from azure.identity import ClientSecretCredential
from agent_framework.foundry import FoundryChatClient


load_dotenv()


class Settings(BaseSettings):

    # =========================
    # Business Central
    # =========================
    bc_tenant_id: str
    bc_client_id: str
    bc_client_secret: str

    bc_base_url: str
    bc_environment: str
    bc_api_version: str
    bc_company_id: str

    http_base_url: str

    # =========================
    # Azure / Foundry
    # =========================
    foundry_project_endpoint: str
    azure_ai_key: str
    azure_openai_deployment: str
    azure_openai_api_version: str

    azure_client_id: str
    azure_client_secret: str
    azure_tenant_id: str


    postgres_host: str
    postgres_port: int = 5432
    postgres_db: str
    postgres_user: str
    postgres_password: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()


# =========================
# Foundry Client
# =========================

credential = ClientSecretCredential(
    tenant_id=settings.azure_tenant_id,
    client_id=settings.azure_client_id,
    client_secret=settings.azure_client_secret,
)

client = FoundryChatClient(
    project_endpoint=settings.foundry_project_endpoint,
    model=settings.azure_openai_deployment,
    credential=credential,
)