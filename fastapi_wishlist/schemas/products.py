from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, field_validator

from fastapi_wishlist.schemas.reviews import ReviewProductSchema


class ProductSchema(BaseModel):
    title: str
    price: Decimal
    description: Optional[str] = None
    brand: str

    @field_validator('title')
    def title_min_length(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Título deve ter pelo menos 2 caracteres')
        return v.strip()

    @field_validator('brand')
    def brand_min_length(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Marca deve ter pelo menos 2 caracteres')
        return v.strip()

    @field_validator('price')
    def price_validation(cls, v):
        if v <= 0:
            raise ValueError('Preço deve ser maior que zero')
        return v
    

class ProductUpdateSchema(BaseModel):
    title: Optional[str] = None
    price: Optional[Decimal] = None
    description: Optional[str] = None
    brand: Optional[str] = None

    @field_validator('title')
    def title_min_length(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Título deve ter pelo menos 2 caracteres')
        return v.strip()

    @field_validator('brand')
    def brand_min_length(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Marca deve ter pelo menos 2 caracteres')
        return v.strip()

    @field_validator('price')
    def price_validation(cls, v):
        if v <= 0:
            raise ValueError('Preço deve ser maior que zero')
        return v


class ProductPublicSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    price: Decimal
    description: Optional[str] = None
    image: Optional[str] = None
    brand: str
    reviews: List[ReviewProductSchema]
    created_at: datetime
    update_at: Optional[datetime]


class ProductListSchema(BaseModel):
    products: List[ProductPublicSchema]
