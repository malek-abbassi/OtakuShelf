"""
Watchlist service for handling watchlist-related business logic.
"""

from typing import List, Optional, Dict, Any
import logging

from sqlmodel import Session, select, func

from ..models import User, WatchlistItem, WatchlistItemCreate, WatchlistItemUpdate
from ..exceptions import WatchlistItemNotFoundError, DuplicateWatchlistItemError, DatabaseError

logger = logging.getLogger(__name__)


class WatchlistService:
    """Service for watchlist-related operations."""

    def __init__(self, db: Session):
        self.db = db

    def add_to_watchlist(self, user: User, item_data: WatchlistItemCreate) -> WatchlistItem:
        """Add an anime to user's watchlist."""
        # Check if anime already exists in watchlist
        existing = self.get_watchlist_item_by_anime_id(user.id, item_data.anime_id)
        if existing:
            raise DuplicateWatchlistItemError(anime_id=item_data.anime_id)

        try:
            watchlist_item = WatchlistItem(
                **item_data.model_dump(),
                user_id=user.id
            )

            self.db.add(watchlist_item)
            self.db.commit()
            self.db.refresh(watchlist_item)
            logger.info(f"Added anime {item_data.anime_id} to {user.username}'s watchlist")
            return watchlist_item
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to add anime {item_data.anime_id} to watchlist: {str(e)}")
            raise DatabaseError(f"Failed to add anime to watchlist: {str(e)}", "add_to_watchlist")

    def get_watchlist(
        self,
        user_id: int,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 20
    ) -> Dict[str, Any]:
        """Get user's watchlist with pagination and filtering."""
        try:
            query = select(WatchlistItem).where(WatchlistItem.user_id == user_id)

            if status:
                query = query.where(WatchlistItem.status == status)

            # Get total count
            count_query = query.with_only_columns(func.count(WatchlistItem.id))
            total_count = self.db.exec(count_query).first() or 0

            # Apply pagination
            query = query.offset(skip).limit(limit)
            items = self.db.exec(query).all()

            # Get status counts
            status_counts = self.get_watchlist_status_counts(user_id)

            return {
                "items": items,
                "total_count": total_count,
                "status_counts": status_counts,
            }
        except Exception as e:
            logger.error(f"Failed to get watchlist for user {user_id}: {str(e)}")
            raise DatabaseError(f"Failed to get watchlist: {str(e)}", "get_watchlist")

    def get_watchlist_item(self, user_id: int, item_id: int) -> Optional[WatchlistItem]:
        """Get a specific watchlist item."""
        return self.db.exec(
            select(WatchlistItem).where(
                WatchlistItem.id == item_id,
                WatchlistItem.user_id == user_id
            )
        ).first()

    def get_watchlist_item_by_anime_id(self, user_id: int, anime_id: int) -> Optional[WatchlistItem]:
        """Get watchlist item by anime ID."""
        return self.db.exec(
            select(WatchlistItem).where(
                WatchlistItem.anime_id == anime_id,
                WatchlistItem.user_id == user_id
            )
        ).first()

    def update_watchlist_item(
        self,
        user_id: int,
        item_id: int,
        update_data: WatchlistItemUpdate
    ) -> WatchlistItem:
        """Update a watchlist item."""
        item = self.get_watchlist_item(user_id, item_id)
        if not item:
            raise WatchlistItemNotFoundError(user_id=user_id, item_id=item_id)

        try:
            update_dict = update_data.model_dump(exclude_unset=True, by_alias=True)
            for field, value in update_dict.items():
                setattr(item, field, value)

            self.db.add(item)
            self.db.commit()
            self.db.refresh(item)
            logger.info(f"Updated watchlist item {item_id} for user {user_id}")
            return item
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to update watchlist item {item_id}: {str(e)}")
            raise DatabaseError(f"Failed to update watchlist item: {str(e)}", "update_watchlist_item")

    def remove_from_watchlist(self, user_id: int, item_id: int) -> None:
        """Remove an item from watchlist."""
        item = self.get_watchlist_item(user_id, item_id)
        if not item:
            raise WatchlistItemNotFoundError(user_id=user_id, item_id=item_id)

        try:
            self.db.delete(item)
            self.db.commit()
            logger.info(f"Removed watchlist item {item_id} for user {user_id}")
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to remove watchlist item {item_id}: {str(e)}")
            raise DatabaseError(f"Failed to remove watchlist item: {str(e)}", "remove_from_watchlist")

    def bulk_update_status(self, user_id: int, item_ids: List[int], new_status: str) -> int:
        """Bulk update status for multiple watchlist items."""
        items = self.db.exec(
            select(WatchlistItem).where(
                WatchlistItem.id.in_(item_ids),
                WatchlistItem.user_id == user_id
            )
        ).all()

        if not items:
            raise WatchlistItemNotFoundError(user_id=user_id, item_ids=item_ids)

        try:
            for item in items:
                item.status = new_status
                self.db.add(item)

            self.db.commit()
            logger.info(f"Updated {len(items)} watchlist items to status {new_status}")
            return len(items)
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to bulk update watchlist items: {str(e)}")
            raise DatabaseError(f"Failed to bulk update watchlist items: {str(e)}", "bulk_update_status")

    def get_watchlist_status_counts(self, user_id: int) -> Dict[str, int]:
        """Get status counts for user's watchlist."""
        try:
            items = self.db.exec(
                select(WatchlistItem).where(WatchlistItem.user_id == user_id)
            ).all()

            status_counts = {}
            for item in items:
                status_counts[item.status] = status_counts.get(item.status, 0) + 1

            return status_counts
        except Exception as e:
            logger.error(f"Failed to get watchlist status counts for user {user_id}: {str(e)}")
            raise DatabaseError(f"Failed to get watchlist status counts: {str(e)}", "get_watchlist_status_counts")


def get_watchlist_service(db: Session) -> WatchlistService:
    """Dependency to get WatchlistService instance."""
    return WatchlistService(db)
