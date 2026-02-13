from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from fastapi_wishlist.core.database import get_session
from fastapi_wishlist.core.security import get_current_user
from fastapi_wishlist.models.users import User
from fastapi_wishlist.models.favorites import Favorite
from fastapi_wishlist.models.products import Product
from fastapi_wishlist.schemas.favorites import (
    FavoritePublicSchema,
    FavoriteSchema
)

router = APIRouter()


@router.post(
    path='/'
)
async def create_favorite(
    product: FavoriteSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(
        select(Product)
        .options(selectinload(Product.reviews))
        .where(Product.id == product.id)
    )
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='produto não encontrado',
        )
    
    favorite_exists = await db.scalar(
        select(exists().where())
    )
