import os
from django.conf import settings

# Keycloak Configuration
KEYCLOAK_CONFIG = {
    'server_url': os.getenv('KEYCLOAK_SERVER_URL', 'http://localhost:8080/'),
    'realm_name': os.getenv('KEYCLOAK_REALM', 'dev-crown-realm'),
    'client_id': os.getenv('KEYCLOAK_CLIENT_ID', 'dev-crown-client'),
    'client_secret': os.getenv('KEYCLOAK_CLIENT_SECRET', ''),
    'redirect_uri': os.getenv('KEYCLOAK_REDIRECT_URI', 'http://localhost:8000/users/keycloak/callback/'),
    'scope': 'openid profile email',
}

# Keycloak URLs
KEYCLOAK_BASE_URL = f"{KEYCLOAK_CONFIG['server_url']}realms/{KEYCLOAK_CONFIG['realm_name']}"
KEYCLOAK_AUTH_URL = f"{KEYCLOAK_BASE_URL}/protocol/openid-connect/auth"
KEYCLOAK_TOKEN_URL = f"{KEYCLOAK_BASE_URL}/protocol/openid-connect/token"
KEYCLOAK_USERINFO_URL = f"{KEYCLOAK_BASE_URL}/protocol/openid-connect/userinfo"
KEYCLOAK_LOGOUT_URL = f"{KEYCLOAK_BASE_URL}/protocol/openid-connect/logout"

# Admin Configuration (for user management)
KEYCLOAK_ADMIN_CONFIG = {
    'username': os.getenv('KEYCLOAK_ADMIN_USERNAME', 'admin'),
    'password': os.getenv('KEYCLOAK_ADMIN_PASSWORD', 'admin'),
    'admin_url': f"{KEYCLOAK_CONFIG['server_url']}admin/realms/{KEYCLOAK_CONFIG['realm_name']}",
}
