from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from fastapi_wishlist.core.database import get_session
from fastapi_wishlist.core.security import (
    get_current_user,
    verify_favorite_ownership,
)
from fastapi_wishlist.models.favorites import Favorite
from fastapi_wishlist.models.products import Product
from fastapi_wishlist.models.users import User
from fastapi_wishlist.schemas.favorites import (
    FavoriteListSchema,
    FavoritePublicSchema,
    FavoriteSchema,
)

router = APIRouter()


@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=FavoritePublicSchema,
    summary='Favoritar produto',
)
async def create_favorite(
    favorite: FavoriteSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    product_exists = await db.get(Product, favorite.product_id)
    if not product_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Produto não encontrado',
        )

    query_check = select(Favorite).where(
        Favorite.owner_id == current_user.id,
        Favorite.product_id == favorite.product_id,
    )
    result_check = await db.execute(query_check)
    if result_check.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Produto já está na sua lista de favoritos',
        )

    new_favorite = Favorite(
        product_id=favorite.product_id,
        owner_id=current_user.id,
    )

    db.add(new_favorite)
    await db.commit()
    await db.refresh(new_favorite)

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


@router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=FavoriteListSchema,
    summary='Lista de favoritos',
)
async def list_favorites(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    result = await db.execute(
        select(Favorite)
        .options(
            selectinload(Favorite.product).selectinload(Product.reviews),
            selectinload(Favorite.owner),
        )
        .where(Favorite.owner_id == current_user.id)
    )

    favorites = result.scalars().all()

    return {'favorites': favorites}


@router.delete(
    '/{product_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Deletar produto favoritado',
)
async def delete_favorite_product(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    product = await db.get(Favorite, product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Produto não encontrado',
        )

    verify_favorite_ownership(current_user, product.owner_id)

    await db.delete(product)
    await db.commit()
