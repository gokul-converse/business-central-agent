from app.config.settings import settings


print("Configuration loaded successfully!")
print(f"Tenant ID: {settings.bc_tenant_id}")
print(f"Client ID: {settings.bc_client_id}")
print(f"Environment: {settings.bc_environment}")
print(f"API Version: {settings.bc_api_version}")
print(f"Company ID: {settings.bc_company_id}")
print(f"Client Secret: {'Loaded' if settings.bc_client_secret else 'Missing'}")