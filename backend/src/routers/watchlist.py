"""
Watchlist management API router.
Handles anime watchlist operations for authenticated users.
"""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query

from ..auth import get_current_user
from ..dependencies import WatchlistServiceDep
from ..models import User, WatchlistItemCreate
from ..schemas import (
    WatchlistAddRequest,
    WatchlistUpdateRequest,
    WatchlistItemResponse,
    WatchlistResponse,
    SuccessResponse,
)

router = APIRouter(prefix="/watchlist", tags=["watchlist"])


@router.post(
    "", response_model=WatchlistItemResponse, status_code=status.HTTP_201_CREATED
)
async def add_to_watchlist(
    watchlist_data: WatchlistAddRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    watchlist_service: WatchlistServiceDep,
):
    """
    Add an anime to the user's watchlist.

    Creates a new watchlist item for the authenticated user.
    """
    try:
        watchlist_item_data = WatchlistItemCreate(**watchlist_data.model_dump(by_alias=True))
        watchlist_item = watchlist_service.add_to_watchlist(current_user, watchlist_item_data)
        return WatchlistItemResponse.model_validate(watchlist_item, from_attributes=True)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=WatchlistResponse)
async def get_watchlist(
    current_user: Annotated[User, Depends(get_current_user)],
    watchlist_service: WatchlistServiceDep,
    status: Optional[str] = Query(None, description="Filter by watch status"),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of items to return"),
):
    """
    Get the user's watchlist with optional filtering and pagination.

    Returns paginated list of watchlist items with status counts.
    """
    result = watchlist_service.get_watchlist(
        current_user.id, status, skip, limit
    )

    # Convert to response format
    items = [WatchlistItemResponse.model_validate(item, from_attributes=True) for item in result["items"]]

    return WatchlistResponse(
        items=items,
        totalCount=result["total_count"],
        statusCounts=result["status_counts"],
    )


@router.get("/{item_id}", response_model=WatchlistItemResponse)
async def get_watchlist_item(
    item_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    watchlist_service: WatchlistServiceDep,
):
    """
    Get a specific watchlist item by ID.

    Returns the watchlist item if it belongs to the authenticated user.
    """
    watchlist_item = watchlist_service.get_watchlist_item(current_user.id, item_id)

    if not watchlist_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Watchlist item not found"
        )

    return WatchlistItemResponse.model_validate(watchlist_item, from_attributes=True)


@router.put("/{item_id}", response_model=WatchlistItemResponse)
async def update_watchlist_item(
    item_id: int,
    update_data: WatchlistUpdateRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    watchlist_service: WatchlistServiceDep,
):
    """
    Update a watchlist item.

    Allows updating status, notes, and user rating.
    """
    try:
        watchlist_item = watchlist_service.update_watchlist_item(
            current_user.id, item_id, update_data
        )
        return WatchlistItemResponse.model_validate(watchlist_item, from_attributes=True)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{item_id}", response_model=SuccessResponse)
async def remove_from_watchlist(
    item_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    watchlist_service: WatchlistServiceDep,
):
    """
    Remove an anime from the user's watchlist.

    Permanently deletes the watchlist item.
    """
    try:
        watchlist_service.remove_from_watchlist(current_user.id, item_id)
        return SuccessResponse(message="Anime removed from watchlist")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/anime/{anime_id}", response_model=Optional[WatchlistItemResponse])
async def get_watchlist_item_by_anime_id(
    anime_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    watchlist_service: WatchlistServiceDep,
):
    """
    Check if a specific anime is in the user's watchlist.

    Returns the watchlist item if found, None otherwise.
    """
    watchlist_item = watchlist_service.get_watchlist_item_by_anime_id(current_user.id, anime_id)

    if not watchlist_item:
        return None

    return WatchlistItemResponse.model_validate(watchlist_item.model_dump())


@router.post("/bulk", response_model=SuccessResponse)
async def bulk_update_status(
    item_ids: list[int],
    new_status: str,
    current_user: Annotated[User, Depends(get_current_user)],
    watchlist_service: WatchlistServiceDep,
):
    """
    Bulk update status for multiple watchlist items.

    Updates the status of all specified watchlist items.
    """
    try:
        updated_count = watchlist_service.bulk_update_status(current_user.id, item_ids, new_status)
        return SuccessResponse(
            message=f"Updated {updated_count} items to status: {new_status}"
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
