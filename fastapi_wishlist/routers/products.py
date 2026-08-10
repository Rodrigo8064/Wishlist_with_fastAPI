from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_wishlist.core.database import get_session
from fastapi_wishlist.core.security import get_current_user
from fastapi_wishlist.models.users import User
from fastapi_wishlist.schemas.products import (
    ProductListSchema,
    ProductPublicSchema,
    ProductSchema,
    ProductUpdateSchema,
)
from fastapi_wishlist.service.product import (
    create_product_service,
    delete_product_service,
    get_product_service,
    list_product_service,
    update_product_service,
)

router = APIRouter()


@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=ProductPublicSchema,
    summary='Criar Produto',
)
async def create_product(
    product: ProductSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    new_product = await create_product_service(db, product)
    return new_product


@router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=ProductListSchema,
    summary='Listar produtos',
)
async def list_products(
    search: Optional[str] = Query(
        None, description='Buscar por título ou marca'
    ),
    min_price: Optional[float] = Query(None, ge=0, description='Preço mínimo'),
    max_price: Optional[float] = Query(None, ge=0, description='Preço máximo'),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    products = await list_product_service(db, search, min_price, max_price)

    return {'products': products}


@router.get(
    path='/{product_id}',
    status_code=status.HTTP_200_OK,
    response_model=ProductPublicSchema,
    summary='Buscar Produto por ID',
)
async def get_product(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    try:
        product = await get_product_service(db, product_id)
        return product
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err),
        )


@router.put(
    path='/{product_id}',
    status_code=status.HTTP_200_OK,
    response_model=ProductPublicSchema,
    summary='Atualizar produto',
)
async def update_product(
    product_id: int,
    product_update: ProductUpdateSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    product = await update_product_service(db, product_id, product_update)

    return product


@router.delete(
    path='/{product_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Deletar produto',
)
async def delete_product(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    await delete_product_service(db, product_id)
