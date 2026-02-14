from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from fastapi_wishlist.core.database import get_session
from fastapi_wishlist.core.security import get_current_user
from fastapi_wishlist.models.products import Product
from fastapi_wishlist.models.users import User
from fastapi_wishlist.schemas.products import (
    ProductListSchema,
    ProductPublicSchema,
    ProductSchema,
    ProductUpdateSchema,
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
    new_product = Product(
        title=product.title,
        price=product.price,
        description=product.description,
        brand=product.brand,
    )
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)

    result = await db.execute(
        select(Product)
        .options(selectinload(Product.reviews))
        .where(Product.id == new_product.id)
    )
    product_with_relation = result.scalar_one()
    return product_with_relation


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
    query = select(Product).options(selectinload(Product.reviews))

    if search:
        search_filter = f'%{search}%'
        query = query.where(
            (Product.title.ilike(search_filter))
            | (Product.brand.ilike(search_filter))
        )

    if min_price is not None:
        query = query.where(Product.price >= min_price)

    if max_price is not None:
        query = query.where(Product.price <= max_price)

    result = await db.execute(query)
    products = result.scalars().all()

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
    result = await db.execute(
        select(Product)
        .options(selectinload(Product.reviews))
        .where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='produto não encontrado',
        )

    return product


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
    product = await db.get(Product, product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Carro não encontrado',
        )

    update_data = product_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(product, field, value)

    await db.commit()
    await db.refresh(product)

    result = await db.execute(
        select(Product)
        .options(selectinload(Product.reviews))
        .where(Product.id == product_id)
    )
    product_with_relation = result.scalar_one()

    return product_with_relation


@router.delete(
    path='/(product_id)',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Deletar produto',
)
async def delete_product(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    product = await db.get(Product, product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Carro não encontrado',
        )

    await db.delete(product)
    await db.commit()
