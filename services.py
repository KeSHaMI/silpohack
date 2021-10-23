import ormar

import redis
from models import Product, Component


async def _find_product_info_by_barcode(barcode: str) -> Product:
    # contains all product's fields and component's names as list of strings
    general_info: dict = _get_product_info(barcode)
    components = general_info.pop('components')
    product = Product(**general_info)
    for component_name in components:
        component_data = await redis.client.get(component_name)
        if component_data:
            component = Component(**component_data)
        else:
            try:
                component = Component.objects.get(name=component_name)
            except ormar.NoMatch:
                # contains all component's fields
                component_data: dict = _get_component_info_by_name(component_name)
                await redis.client.set(component_name, component_data, ex=3600)
                component = Component(**component_data)
        product.components.append(component)
    return product


async def get_product_by_barcode(barcode: str) -> Product:
    try:
        product: Product = await Product.objects.select_related('components').get(barcode=barcode)
    except ormar.NoMatch:
        # DS part
        product = await _find_product_info_by_barcode(barcode)
        await product.upsert()

    return product
