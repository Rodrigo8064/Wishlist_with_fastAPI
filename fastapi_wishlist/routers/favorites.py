from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_wishlist.core.database import get_session
from fastapi_wishlist.core.security import (
    get_current_user,
)
from fastapi_wishlist.models.users import User
from fastapi_wishlist.schemas.favorites import (
    FavoriteListSchema,
    FavoritePublicSchema,
    FavoriteSchema,
)
from fastapi_wishlist.service.favorite import (
    create_favorite_service,
    delete_favorite_service,
    list_favorites_service,
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
    try:
        new_favorite = await create_favorite_service(
            db, favorite, current_user
        )
        return new_favorite
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err),
        )


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
    favorites = await list_favorites_service(db, current_user)

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
    await delete_favorite_service(db, product_id, current_user)
