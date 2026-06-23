import pytest
from sqlalchemy import select

from fastapi_wishlist.models import User


@pytest.mark.asyncio
async def test_create_user(session):
    new_user = User(
        username='teste', email='testedb@testedb.com', password='secret'
    )
    session.add(new_user)
    await session.commit()

    user = await session.scalar(
        select(User).where(User.email == 'testedb@testedb.com')
    )

    new_user_data = {
        'id': user.id,
        'username': user.username,
        'password': user.password,
        'email': user.email,
    }

    assert new_user_data == {
        'id': 1,
        'username': 'teste',
        'email': 'testedb@testedb.com',
        'password': 'secret',
    }
