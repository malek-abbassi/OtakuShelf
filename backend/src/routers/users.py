"""
User management API router.
Handles user authentication, profile management, and user operations.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from ..auth import get_current_user
from ..dependencies import AuthServiceDep, UserServiceDep
from ..models import User, UserUpdate, UserRead
from ..schemas import (
    UserSignupRequest,
    UserLoginRequest,
    UserProfileResponse,
    SuccessResponse,
)
from ..services.auth_service import (
    UsernameTakenError,
    EmailAlreadyRegisteredError,
    UserCreationError,
    AuthException,
    InvalidCredentialsError,
    UserProfileNotFoundError,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/signup", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED
)
async def signup(
    signup_data: UserSignupRequest,
    auth_service: AuthServiceDep,
):
    """
    Register a new user account.

    Creates a new user with SuperTokens authentication and database profile.
    """
    try:
        user = await auth_service.signup_user(
            email=signup_data.email,
            password=signup_data.password,
            username=signup_data.username,
            full_name=signup_data.full_name,
        )
        return SuccessResponse(
            message="User created successfully",
            data={"user_id": user.id, "username": user.username},
        )
    except UsernameTakenError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except EmailAlreadyRegisteredError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except UserCreationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except AuthException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.post("/signin", response_model=SuccessResponse)
async def signin(
    signin_data: UserLoginRequest,
    auth_service: AuthServiceDep,
):
    """
    Sign in an existing user.

    Authenticates user with SuperTokens and returns user information.
    """
    try:
        user = await auth_service.signin_user(
            email=signin_data.email,
            password=signin_data.password,
        )
        return SuccessResponse(
            message="Sign in successful",
            data={"user_id": user.id, "username": user.username},
        )
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except UserProfileNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.get("/me", response_model=UserProfileResponse)
async def get_current_user_profile(
    current_user: Annotated[User, Depends(get_current_user)],
    user_service: UserServiceDep,
):
    """
    Get current user's profile information.

    Returns detailed profile including watchlist count.
    """
    return UserProfileResponse(**user_service.get_user_profile_data(current_user))


@router.put("/me", response_model=UserRead)
async def update_current_user_profile(
    user_update: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    auth_service: AuthServiceDep,
    user_service: UserServiceDep,
):
    """
    Update current user's profile information.

    Allows updating username and full_name.
    """
    # Check if username is being updated and if it's available
    if user_update.username and user_update.username != current_user.username:
        if not auth_service.is_username_available(user_update.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
            )

    # Update user
    updated_user = user_service.update_user(current_user, user_update)
    return UserRead.model_validate(updated_user)


@router.get("/check-username/{username}", response_model=dict)
async def check_username_availability(
    username: str,
    auth_service: AuthServiceDep,
):
    """
    Check if a username is available.

    Returns availability status for the given username.
    """
    is_available = auth_service.is_username_available(username)

    return {
        "username": username,
        "available": is_available,
        "message": "Username is available"
        if is_available
        else "Username already taken",
    }


@router.delete("/me", response_model=SuccessResponse)
async def deactivate_current_user(
    current_user: Annotated[User, Depends(get_current_user)],
    user_service: UserServiceDep,
):
    """
    Deactivate current user account.

    Sets user as inactive instead of deleting to preserve data integrity.
    """
    user_service.deactivate_user(current_user)
    return SuccessResponse(message="Account deactivated successfully")
