"""
Watchlist management API router.
Handles anime watchlist operations for authenticated users.
"""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select

from ..auth import get_current_user
from ..db.core import get_session
from ..models import User, WatchlistItem, WatchlistItemCreate
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
    db: Annotated[Session, Depends(get_session)],
):
    """
    Add an anime to the user's watchlist.

    Creates a new watchlist item for the authenticated user.
    """
    # Check if anime is already in user's watchlist
    existing_item = db.exec(
        select(WatchlistItem).where(
            WatchlistItem.user_id == current_user.id,
            WatchlistItem.anime_id == watchlist_data.anime_id,
        )
    ).first()

    if existing_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Anime already in watchlist"
        )

    # Create new watchlist item
    watchlist_item_data = WatchlistItemCreate(**watchlist_data.model_dump())
    watchlist_item = WatchlistItem(
        **watchlist_item_data.model_dump(), user_id=current_user.id
    )

    db.add(watchlist_item)
    db.commit()
    db.refresh(watchlist_item)

    return WatchlistItemResponse.model_validate(watchlist_item, from_attributes=True)


@router.get("", response_model=WatchlistResponse)
async def get_watchlist(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_session)],
    status_filter: Optional[str] = Query(None, description="Filter by watch status"),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of items to return"),
):
    """
    Get the user's watchlist with optional filtering and pagination.

    Returns paginated list of watchlist items with status counts.
    """
    # Build base query
    query = select(WatchlistItem).where(WatchlistItem.user_id == current_user.id)

    # Apply status filter if provided
    if status_filter:
        query = query.where(WatchlistItem.status == status_filter)

    # Apply pagination
    query = query.offset(skip).limit(limit)

    # Execute query
    watchlist_items = db.exec(query).all()

    # Get total count for pagination
    total_query = select(WatchlistItem).where(WatchlistItem.user_id == current_user.id)
    if status_filter:
        total_query = total_query.where(WatchlistItem.status == status_filter)
    total_count = len(db.exec(total_query).all())

    # Get status counts
    all_items = db.exec(
        select(WatchlistItem).where(WatchlistItem.user_id == current_user.id)
    ).all()

    status_counts = {}
    for item in all_items:
        status_counts[item.status] = status_counts.get(item.status, 0) + 1

    # Convert to response format
    items = [WatchlistItemResponse.model_validate(item, from_attributes=True) for item in watchlist_items]

    return WatchlistResponse(
        items=items,
        totalCount=total_count,
        statusCounts=status_counts,
    )


@router.get("/{item_id}", response_model=WatchlistItemResponse)
async def get_watchlist_item(
    item_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_session)],
):
    """
    Get a specific watchlist item by ID.

    Returns the watchlist item if it belongs to the authenticated user.
    """
    watchlist_item = db.exec(
        select(WatchlistItem).where(
            WatchlistItem.id == item_id, WatchlistItem.user_id == current_user.id
        )
    ).first()

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
    db: Annotated[Session, Depends(get_session)],
):
    """
    Update a watchlist item.

    Allows updating status, notes, and user rating.
    """
    watchlist_item = db.exec(
        select(WatchlistItem).where(
            WatchlistItem.id == item_id, WatchlistItem.user_id == current_user.id
        )
    ).first()

    if not watchlist_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Watchlist item not found"
        )

    # Update fields
    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(watchlist_item, field, value)

    db.add(watchlist_item)
    db.commit()
    db.refresh(watchlist_item)

    return WatchlistItemResponse.model_validate(watchlist_item, from_attributes=True)


@router.delete("/{item_id}", response_model=SuccessResponse)
async def remove_from_watchlist(
    item_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_session)],
):
    """
    Remove an anime from the user's watchlist.

    Permanently deletes the watchlist item.
    """
    watchlist_item = db.exec(
        select(WatchlistItem).where(
            WatchlistItem.id == item_id, WatchlistItem.user_id == current_user.id
        )
    ).first()

    if not watchlist_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Watchlist item not found"
        )

    db.delete(watchlist_item)
    db.commit()

    return SuccessResponse(message="Anime removed from watchlist")


@router.get("/anime/{anime_id}", response_model=Optional[WatchlistItemResponse])
async def get_watchlist_item_by_anime_id(
    anime_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_session)],
):
    """
    Check if a specific anime is in the user's watchlist.

    Returns the watchlist item if found, None otherwise.
    """
    watchlist_item = db.exec(
        select(WatchlistItem).where(
            WatchlistItem.anime_id == anime_id, WatchlistItem.user_id == current_user.id
        )
    ).first()

    if not watchlist_item:
        return None

    return WatchlistItemResponse.model_validate(watchlist_item.model_dump())


@router.post("/bulk", response_model=SuccessResponse)
async def bulk_update_status(
    item_ids: list[int],
    new_status: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_session)],
):
    """
    Bulk update status for multiple watchlist items.

    Updates the status of all specified watchlist items.
    """
    watchlist_items = db.exec(
        select(WatchlistItem).where(
            WatchlistItem.id.in_(item_ids), WatchlistItem.user_id == current_user.id
        )
    ).all()

    if not watchlist_items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No watchlist items found"
        )

    # Update status for all items
    for item in watchlist_items:
        item.status = new_status
        db.add(item)

    db.commit()

    return SuccessResponse(
        message=f"Updated {len(watchlist_items)} items to status: {new_status}"
    )
