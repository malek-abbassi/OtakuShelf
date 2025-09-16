"""
User management API router.
Handles user authentication, profile management, and user operations.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from ..auth import get_current_user
from ..db.core import get_session
from ..dependencies import AuthServiceDep
from ..models import User, UserUpdate, UserRead
from ..schemas import (
    UserSignupRequest,
    UserLoginRequest,
    UserProfileResponse,
    SuccessResponse,
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
    success, message, user = await auth_service.signup_user(
        email=signup_data.email,
        password=signup_data.password,
        username=signup_data.username,
        full_name=signup_data.full_name,
    )

    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

    return SuccessResponse(
        message="User created successfully",
        data={"user_id": user.id, "username": user.username},
    )


@router.post("/signin", response_model=SuccessResponse)
async def signin(
    signin_data: UserLoginRequest,
    auth_service: AuthServiceDep,
):
    """
    Sign in an existing user.

    Authenticates user with SuperTokens and returns user information.
    """
    success, message, user = await auth_service.signin_user(
        email=signin_data.email,
        password=signin_data.password,
    )

    if not success:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)

    return SuccessResponse(
        message="Sign in successful",
        data={"user_id": user.id, "username": user.username},
    )


@router.get("/me", response_model=UserProfileResponse)
async def get_current_user_profile(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_session)],
):
    """
    Get current user's profile information.

    Returns detailed profile including watchlist count.
    """
    # Count watchlist items
    watchlist_count = (
        len(current_user.watchlist_items) if current_user.watchlist_items else 0
    )

    return UserProfileResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
        watchlist_count=watchlist_count,
    )


@router.put("/me", response_model=UserRead)
async def update_current_user_profile(
    user_update: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    auth_service: AuthServiceDep,
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

    # Update user fields
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)

    auth_service.db.add(current_user)
    auth_service.db.commit()
    auth_service.db.refresh(current_user)

    return UserRead.model_validate(current_user)


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
    db: Annotated[Session, Depends(get_session)],
):
    """
    Deactivate current user account.

    Sets user as inactive instead of deleting to preserve data integrity.
    """
    current_user.is_active = False
    db.add(current_user)
    db.commit()

    return SuccessResponse(message="Account deactivated successfully")
