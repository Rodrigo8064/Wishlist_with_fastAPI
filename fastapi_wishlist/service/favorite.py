from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from fastapi_wishlist.core.security import verify_favorite_ownership
from fastapi_wishlist.models.favorites import Favorite
from fastapi_wishlist.models.products import Product
from fastapi_wishlist.schemas.favorites import (
    FavoriteSchema,
)
from fastapi_wishlist.service.helpers import (
    delete_object,
    get_object,
    save_object,
)


async def create_favorite_service(
    db: AsyncSession, favorite: FavoriteSchema, current_user
) -> Favorite:
    await get_object(
        db=db,
        db_model=Product,
        object_id=favorite.product_id,
        resource_name='Produto',
    )

    query_check = select(Favorite).where(
        Favorite.owner_id == current_user.id,
        Favorite.product_id == favorite.product_id,
    )
    result_check = await db.execute(query_check)
    if result_check.scalar_one_or_none():
        raise ValueError('Produto já está na sua lista de favoritos')

    new_favorite = Favorite(
        product_id=favorite.product_id,
        owner_id=current_user.id,
    )

    new_favorite = await save_object(db, new_favorite)
    result = await db.execute(
        select(Favorite)
        .options(
            selectinload(Favorite.product).selectinload(Product.reviews),
            selectinload(Favorite.owner),
        )
        .where(Favorite.id == new_favorite.id)
    )
    favorite_with_relations = result.scalar_one()

    return favorite_with_relations


async def list_favorites_service(
    db: AsyncSession, current_user
) -> Sequence[Favorite]:
    result = await db.execute(
        select(Favorite)
        .options(
            selectinload(Favorite.product).selectinload(Product.reviews),
            selectinload(Favorite.owner),
        )
        .where(Favorite.owner_id == current_user.id)
    )

    favorites = result.scalars().all()
    return favorites


async def delete_favorite_service(
    db: AsyncSession, product_id: int, current_user
):
    product = await get_object(
        db=db,
        db_model=Favorite,
        object_id=product_id,
        resource_name='Produto',
    )
    verify_favorite_ownership(current_user, product.owner_id)

    await delete_object(db, product)
