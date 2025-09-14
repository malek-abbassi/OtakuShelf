"""
Factory classes for creating test data.
"""

import factory
from faker import Faker

from src.models import User, WatchlistItem

fake = Faker()


class UserFactory(factory.Factory):
    """Factory for creating User instances."""
    
    class Meta:
        model = User
    
    supertokens_user_id = factory.LazyFunction(lambda: f"st-user-{fake.uuid4()}")
    username = factory.LazyFunction(lambda: fake.user_name())
    email = factory.LazyFunction(lambda: fake.email())
    full_name = factory.LazyFunction(lambda: fake.name())
    is_active = True


class WatchlistItemFactory(factory.Factory):
    """Factory for creating WatchlistItem instances."""
    
    class Meta:
        model = WatchlistItem
    
    anime_id = factory.LazyFunction(lambda: fake.random_int(min=1, max=999999))
    anime_title = factory.LazyFunction(lambda: fake.catch_phrase())
    anime_picture_url = factory.LazyFunction(lambda: fake.image_url())
    anime_score = factory.LazyFunction(lambda: round(fake.random.uniform(1.0, 10.0), 1))
    status = factory.LazyFunction(lambda: fake.random_element(elements=[
        "plan_to_watch", "watching", "completed", "dropped", "on_hold"
    ]))
    notes = factory.LazyFunction(lambda: fake.text(max_nb_chars=200))
