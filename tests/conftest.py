import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from fastapi_wishlist.app import app
from fastapi_wishlist.core.database import get_session
from fastapi_wishlist.core.security import (
    create_access_token,
    get_password_hash,
)
from fastapi_wishlist.models import Base
from fastapi_wishlist.models.favorites import Favorite
from fastapi_wishlist.models.products import Product, Review
from fastapi_wishlist.models.users import User


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        url='sqlite+aiosqlite:///:memory:',
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def user_data():
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'secret123',
    }


@pytest_asyncio.fixture
async def second_user(session):
    hashed_password = get_password_hash('password123')
    db_user = User(
        username='seconduser',
        email='second@example.com',
        password=hashed_password,
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


@pytest_asyncio.fixture
async def user(session, user_data):
    hashed_password = get_password_hash(user_data['password'])
    db_user = User(
        username=user_data['username'],
        email=user_data['email'],
        password=hashed_password,
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


@pytest.fixture
def access_token(user):
    return create_access_token(data={'sub': str(user.id)})


@pytest.fixture
def auth_headers(access_token):
    return {'Authorization': f'Bearer {access_token}'}


@pytest_asyncio.fixture
async def product_data():
    return {
        'title': 'testando',
        'price': 2000,
        'description': 'testando',
        'brand': 'de teste',
    }


@pytest_asyncio.fixture
async def product(session, product_data):
    db_product = Product(
        title=product_data['title'],
        price=product_data['price'],
        description=product_data['description'],
        brand=product_data['brand'],
    )
    session.add(db_product)
    await session.commit()
    await session.refresh(db_product)
    return db_product


@pytest_asyncio.fixture
async def second_product(session):
    db_product = Product(
        title='teclado de teste',
        price=1000,
        description='teclado bem bom',
        brand='Logitech',
    )
    session.add(db_product)
    await session.commit()
    await session.refresh(db_product)
    return db_product


@pytest_asyncio.fixture
async def review(session, product):
    db_review = Review(
        stars='5',
        comment='muito bom',
        product_id=product.id,
    )

    session.add(db_review)
    await session.commit()
    await session.refresh(db_review)
    return db_review


@pytest_asyncio.fixture
async def favorite(session, product, user):
    db_favorite = Favorite(
        product_id=product.id,
        owner_id=user.id,
    )

    session.add(db_favorite)
    await session.commit()
    await session.refresh(db_favorite)
    return db_favorite
