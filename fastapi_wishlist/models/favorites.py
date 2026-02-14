from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_wishlist.models import Base

if TYPE_CHECKING:
    from fastapi_wishlist.models import Product, User


class Favorite(Base):
    __tablename__ = 'favorites'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    product: Mapped['Product'] = relationship(
        'Product',
        back_populates='favorites',
    )
    owner_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
    )
    owner: Mapped['User'] = relationship(
        'User',
        back_populates='favorites',
    )

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        onupdate=func.now(), server_default=func.now()
    )
