from typing import Sequence

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_wishlist.core.security import get_password_hash
from fastapi_wishlist.models.users import User
from fastapi_wishlist.schemas.users import (
    UserSchema,
    UserUpdateSchema,
)
from fastapi_wishlist.service.helpers import (
    UserConflictError,
    delete_object,
    get_object,
    save_object,
    update_object,
)


async def create_user_service(db: AsyncSession, user_data: UserSchema) -> User:
    username_exists = await db.scalar(
        select(exists().where(User.username == user_data.username))
    )
    if username_exists:
        raise ValueError('Username já está em uso')

    email_exists = await db.scalar(
        select(exists().where(User.email == user_data.email))
    )
    if email_exists:
        raise ValueError('Email já está em uso')

    db_user = User(
        username=user_data.username,
        email=user_data.email,
        password=get_password_hash(user_data.password),
    )

    db_user = await save_object(db, db_user)

    return db_user


async def list_user_service(
    db: AsyncSession, search: str | None, offset: int, limit: int
) -> Sequence[User]:
    query = select(User)

    if search:
        search_filter = f'%{search}%'
        query = query.where(
            (User.username.ilike(search_filter))
            | (User.email.ilike(search_filter))
        )

    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    users = result.scalars().all()

    return users


async def get_user_service(db: AsyncSession, user_id: int) -> User:
    return await get_object(
        db=db, db_model=User, object_id=user_id, resource_name='Usuário'
    )


async def update_user_service(
    db: AsyncSession, user_id: int, user_update: UserUpdateSchema
) -> User:
    user = await get_user_service(db, user_id)

    update_data = user_update.model_dump(exclude_unset=True)

    if 'username' in update_data and update_data['username'] != user.username:
        username_exists = await db.scalar(
            select(
                exists().where(
                    (User.username == update_data['username'])
                    & (User.id != user_id)
                )
            )
        )
        if username_exists:
            raise UserConflictError('Username já está em uso')

    if 'email' in update_data and update_data['email'] != user.email:
        email_exists = await db.scalar(
            select(
                exists().where(
                    (User.email == update_data['email']) & (User.id != user_id)
                )
            )
        )
        if email_exists:
            raise UserConflictError('Email já está em uso')

    if 'password' in update_data:
        update_data['password'] = get_password_hash(update_data['password'])

    for field, value in update_data.items():
        setattr(user, field, value)

    user = await update_object(db, user)

    return user


async def delete_user_service(db: AsyncSession, user_id: int):
    user = await get_user_service(db, user_id)

    await delete_object(db, user)
