from fastapi_users.authentication import JWTStrategy

from core.config import settings


def get_JWT_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.access_token.verification_token_secret, lifetime_seconds=3600)
