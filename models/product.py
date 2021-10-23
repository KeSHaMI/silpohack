import ormar
from decimal import Decimal
from typing import List

from db import BaseMeta
from .component import Component


class Product(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'product'

    DECIMAL_PARAMS = {'nullable': True, 'default': True, 'max_digits': 10, 'decimal_places': 5}

    barcode: str = ormar.String(max_length=15, primary_key=True)
    name: str = ormar.Text()

    proteins: float = ormar.Decimal(**DECIMAL_PARAMS)
    fats: float = ormar.Decimal(**DECIMAL_PARAMS)
    carbohydrates: float = ormar.Decimal(**DECIMAL_PARAMS)
    calories: float = ormar.Decimal(**DECIMAL_PARAMS)

    mass: float = ormar.Decimal(**DECIMAL_PARAMS)

    package: str = ormar.Text()

    is_gmo: bool = ormar.Boolean()
    is_organic: bool = ormar.Boolean()

    is_vegetarian: bool = ormar.Boolean()
    is_vegan: bool = ormar.Boolean()

    components: List[Component.get_pydantic()] = ormar.ManyToMany(Component)

    @property
    def image_path(self) -> str:
        return f'product_{self.barcode}'

    def save_image(self):
        return


Product.update_forward_refs()
