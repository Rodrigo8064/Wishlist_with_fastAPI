from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from fastapi_wishlist.core.database import get_session
from fastapi_wishlist.core.security import get_current_user
from fastapi_wishlist.models.products import Review
from fastapi_wishlist.models.users import User
from fastapi_wishlist.schemas.reviews import (
    ReviewPublicSchema,
    ReviewSchema,
    ReviewUpdateSchema,
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
    new_review = Review(
        stars=review.stars,
        comment=review.comment,
        product_id=review.product_id,
    )

    db.add(new_review)
    await db.commit()
    await db.refresh(new_review)

    result = await db.execute(
        select(Review)
        .options(selectinload(Review.product))
        .where(Review.id == new_review.id)
    )
    review_with_relation = result.scalar_one()

    return review_with_relation


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
    review = await db.get(Review, review_id)

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Review não encontrado',
        )

    update_data = review_update.model_dump(exclude_unset=True)

    for attr, value in update_data.items():
        setattr(review, attr, value)

    await db.commit()
    await db.refresh(review)

    result = await db.execute(
        select(Review)
        .options(selectinload(Review.product))
        .where(Review.id == review_id)
    )
    review_with_relation = result.scalar_one()

    return review_with_relation


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
    review = await db.get(Review, review_id)

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Review não encontrado',
        )

    await db.delete(review)
    await db.commit()
