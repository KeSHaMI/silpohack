import ormar

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
    positivity: str = ormar.String(max_length=8, choices=POSITIVITY_CHOICES)
    name: str = ormar.Text(index=True)
    description: str = ormar.Text()
    # products: List['Product']


Component.update_forward_refs()


