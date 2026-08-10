from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from fastapi_wishlist.models.products import Product
from fastapi_wishlist.schemas.products import (
    ProductSchema,
    ProductUpdateSchema,
)
from fastapi_wishlist.service.helpers import (
    delete_object,
    get_object,
    save_object,
    update_object,
)


async def create_product_service(
    db: AsyncSession, product: ProductSchema
) -> Product:
    new_product = Product(
        title=product.title,
        price=product.price,
        description=product.description,
        brand=product.brand,
    )
    db_product = await save_object(db, new_product)

    result = await db.execute(
        select(Product)
        .options(selectinload(Product.reviews))
        .where(Product.id == db_product.id)
    )
    product_with_relation = result.scalar_one()
    return product_with_relation


async def list_product_service(
    db: AsyncSession,
    search: str | None,
    min_price: float | None,
    max_price: float | None,
) -> Sequence[Product]:
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

    return products


async def get_product_service(db: AsyncSession, product_id: int) -> Product:
    result = await db.execute(
        select(Product)
        .options(selectinload(Product.reviews))
        .where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()

    if not product:
        raise ValueError(
            'produto não encontrado',
        )

    return product


async def update_product_service(
    db: AsyncSession, product_id: int, product_update: ProductUpdateSchema
) -> Product:
    product = await get_object(db, Product, product_id, 'Produto')

    update_data = product_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(product, field, value)

    await update_object(db, product)

    result = await db.execute(
        select(Product)
        .options(selectinload(Product.reviews))
        .where(Product.id == product_id)
    )
    product_with_relation = result.scalar_one()

    return product_with_relation


async def delete_product_service(db: AsyncSession, product_id: int):
    product = await get_object(db, Product, product_id, 'Produto')

    await delete_object(db, product)
