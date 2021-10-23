import ormar
import pydantic

from db import BaseMeta


class Component(ormar.Model):

    class Meta(BaseMeta):
        tablename = 'component'

    POSITIVITY_GREEN = 'green'
    POSITIVITY_YELLOW = 'yellow'
    POSITIVITY_RED = 'red'

    POSITIVITY_CHOICES = [
        POSITIVITY_GREEN,
        POSITIVITY_YELLOW,
        POSITIVITY_RED,
    ]

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    is_healthy = ormar.Boolean()
    name: str = ormar.Text(index=True)
    description: str = ormar.Text()
    is_blacklisted: bool = ormar.Boolean(pydantic_only=True, default=False)
    # products: List['Product']


Component.update_forward_refs()


