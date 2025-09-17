"""
Authentication package.
Integrates SuperTokens with our database models.
"""

from .dependencies import get_current_user, get_current_user_id, get_optional_current_user
from ..services.auth_service import AuthService

__all__ = [
    "get_current_user",
    "get_current_user_id",
    "get_optional_current_user",
    "AuthService",
]
