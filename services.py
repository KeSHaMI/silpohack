import json

import ormar
from typing import Optional

import redis
from models import Product, Component
from ds_services import get_product_info, get_component_info_by_name


async def _create_or_update_component(component_name: str, component_id: Optional[int] = None):
    component_data: dict = get_component_info_by_name(component_name.lower())
    if component_id:
        component_data['id'] = component_data
    component = Component(**component_data)
    await redis.client.set(component_name, json.dumps(component_data), ex=3600)
    return component


async def _find_product_info_by_barcode(barcode: str) -> Product:
    # contains all product's fields and component's names as list of strings
    general_info: dict = get_product_info(barcode)
    components = general_info.pop('components')
    product = Product(**general_info)
    product = await product.save()
    for component_name in components:
        component_data = await redis.client.get(component_name)
        if component_data:
            component_data = json.loads(component_data)
            component = Component(**component_data)
            await component.save()
        else:
            try:
                component = await Component.objects.get(name=component_name, is_autocreated=False)
                component = await _create_or_update_component(component.name, component.id)
            except ormar.NoMatch:
                # contains all component's fields
                component = await _create_or_update_component(component_name)
                await component.save()

        await product.components.add(component)
    return product


async def get_product_by_barcode(barcode: str) -> Product:
    try:
        product: Product = await Product.objects.select_related('components').get(barcode=barcode)
    except ormar.NoMatch:
        # DS part
        product = await _find_product_info_by_barcode(barcode)
        await product.upsert()

    return product
