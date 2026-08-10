from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from fastapi_wishlist.models.products import Review
from fastapi_wishlist.schemas.reviews import (
    ReviewSchema,
    ReviewUpdateSchema,
)
from fastapi_wishlist.service.helpers import (
    delete_object,
    get_object,
    save_object,
    update_object,
)


async def create_review_service(db: AsyncSession, review: ReviewSchema):
    new_review = Review(
        stars=review.stars,
        comment=review.comment,
        product_id=review.product_id,
    )
    new_review = await save_object(db, new_review)

    result = await db.execute(
        select(Review)
        .options(selectinload(Review.product))
        .where(Review.id == new_review.id)
    )
    review_with_relation = result.scalar_one()

    return review_with_relation


async def update_review_service(
    db: AsyncSession, review_id: int, review_update: ReviewUpdateSchema
):
    review = await get_object(db, Review, review_id, 'Review')

    update_data = review_update.model_dump(exclude_unset=True)

    for attr, value in update_data.items():
        setattr(review, attr, value)

    await update_object(db, review)

    result = await db.execute(
        select(Review)
        .options(selectinload(Review.product))
        .where(Review.id == review_id)
    )
    review_with_relation = result.scalar_one()

    return review_with_relation


async def delete_review_service(db: AsyncSession, review_id: int):
    review = await get_object(db, Review, review_id, 'Review')

    await delete_object(db, review)
