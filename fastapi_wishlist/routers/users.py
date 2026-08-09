from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_wishlist.core.database import get_session
from fastapi_wishlist.core.security import get_current_user
from fastapi_wishlist.models.users import User
from fastapi_wishlist.schemas.users import (
    UserListPublicSchema,
    UserPublicSchema,
    UserSchema,
    UserUpdateSchema,
)
from fastapi_wishlist.service.users import (
    UserConflictError,
    create_user_service,
    delete_user_service,
    get_user_service,
    list_user_service,
    update_user_service,
)

router = APIRouter()


@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=UserPublicSchema,
    summary='Criar novo usuário',
)
async def create_user(
    user: UserSchema,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    try:
        db_user = await create_user_service(db=db, user_data=user)
        return db_user
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err),
        )


@router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=UserListPublicSchema,
    summary='Listar usuários',
)
async def list_users(
    offset: int = Query(0, ge=0, description='Número de registros para pular'),
    limit: int = Query(100, ge=1, le=100, description='Limite de registros'),
    search: Optional[str] = Query(
        None, description='Buscar por username ou email'
    ),
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    users = await list_user_service(
        db=db, search=search, offset=offset, limit=limit
    )

    return {'users': users, 'offset': offset, 'limit': limit}


@router.get(
    path='/{user_id}',
    status_code=status.HTTP_200_OK,
    response_model=UserPublicSchema,
    summary='Buscar usuário por ID',
)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await get_user_service(db=db, user_id=user_id)


@router.put(
    path='/{user_id}',
    status_code=status.HTTP_200_OK,
    response_model=UserPublicSchema,
    summary='Atualizar usuário',
)
async def update_user(
    user_id: int,
    user_update: UserUpdateSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    try:
        updated_user = await update_user_service(
            db=db, user_id=user_id, user_update=user_update
        )
        return updated_user
    except UserConflictError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err),
        )


@router.delete(
    path='/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Deletar usuário',
)
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    await delete_user_service(db=db, user_id=user_id)
