import redis
import json
from typing import List

from fastapi import Request, APIRouter
from fastapi.responses import JSONResponse

from models import Product, Component, User
from services import get_product_by_barcode, cache_product_response


router = APIRouter()


@router.get('/product/{barcode}/', response_model=Product.get_pydantic())
async def get_product(barcode: str):
    cached_product_data = redis.client.get(barcode)
    if cached_product_data:
        return Product(**cached_product_data)
    product: Product = await get_product_by_barcode(barcode)
    await cache_product_response(product)
    return product


@router.get('/blacklist', response_model=List[Component.get_pydantic(include={'id', 'name'})])
async def user_blacklist(request: Request):
    user: User = request.authenticated_user
    blacklist = json.loads(user.blacklist)
    components = []
    for component_id in blacklist:
        component = await Component.objects.get(id=component_id)
        components.append(component)
    return components


@router.post('/blacklist/{component_id}')
async def add_to_blacklist(request: Request, component_id: int):
    user: User = request.authenticated_user
    component = await Component.objects.get(id=component_id)
    await user.add_component_to_blacklist(component)
    return JSONResponse({'ok': True})


@router.delete('/blacklist/{component_id}')
async def remove_from_blacklist(request: Request, component_id: int):
    user: User = request.authenticated_user
    component = await Component.objects.get(id=component_id)
    await user.remove_component_from_blacklist(component)
    return JSONResponse({'ok': True})
