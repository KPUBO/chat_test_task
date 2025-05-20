from fastapi_users.authentication import AuthenticationBackend

from core.authentication.transport import bearer_transport
from api.dependencies.authentication.strategy import get_JWT_strategy

authentication_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_JWT_strategy,
)
