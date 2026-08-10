from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_wishlist.core.database import get_session
from fastapi_wishlist.core.security import get_current_user
from fastapi_wishlist.models.users import User
from fastapi_wishlist.schemas.reviews import (
    ReviewPublicSchema,
    ReviewSchema,
    ReviewUpdateSchema,
)
from fastapi_wishlist.service.review import (
    create_review_service,
    delete_review_service,
    update_review_service,
)

router = APIRouter()


@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=ReviewPublicSchema,
    summary='Criar review',
)
async def create_review(
    review: ReviewSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    new_review = await create_review_service(db, review)

    return new_review


@router.put(
    path='/{review_id}',
    status_code=status.HTTP_200_OK,
    response_model=ReviewPublicSchema,
    summary='Atualizar review',
)
async def update_review(
    review_id: int,
    review_update: ReviewUpdateSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    review = await update_review_service(db, review_id, review_update)

    return review


@router.delete(
    path='/{review_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Deletar review',
)
async def delete_review(
    review_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    await delete_review_service(db, review_id)
