import ormar
from typing import List
import random
from pydantic import validator
from decimal import Decimal

from db import BaseMeta
from .component import Component


def get_rand_price() -> float:
    return round(random.uniform(1.0, 100.0), 2)


DEFAULT_PHOTO_URL = 'https://e7.pngegg.com/pngimages/140/347/png-clipart-grocery-store-shopping-list-food-icon-a-bag-of-food-text-hand.png'


class Product(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'product'

    barcode: str = ormar.String(max_length=15, primary_key=True)
    name: str = ormar.Text()

    proteins: float = ormar.Float()
    fats: float = ormar.Float()
    carbohydrates: float = ormar.Float()
    calories: float = ormar.Float()

    mass: float = ormar.Float()
    price: float = ormar.Float(default=get_rand_price)

    package: str = ormar.Text()
    utilize: str = ormar.Text()

    is_gmo: bool = ormar.Boolean()
    is_organic: bool = ormar.Boolean()

    is_vegetarian: bool = ormar.Boolean()
    is_vegan: bool = ormar.Boolean()
    image_url: str = ormar.Text(default=DEFAULT_PHOTO_URL)

    components: List[Component.get_pydantic()] = ormar.ManyToMany(Component)

    healthy_components_percentage: float = ormar.Float(pydantic_only=True, default=0.0)


Product.update_forward_refs()
