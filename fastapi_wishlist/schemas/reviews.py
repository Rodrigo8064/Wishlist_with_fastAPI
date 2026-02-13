from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class ReviewSchema(BaseModel):
    product_id: int
    stars: int
    comment: Optional[str] = None

    @field_validator('stars')
    def stars_validation(cls, v):
        if v < 0 or v > 5:
            raise ValueError('Estrelas devem estar entre 0 e 5')
        return v


class ReviewUpdateSchema(BaseModel):
    stars: Optional[int] = None
    comment: Optional[str] = None

    @field_validator('stars')
    def stars_validation(cls, v):
        if v < 0 or v > 5:
            raise ValueError('Estrelas devem estar entre 0 e 5')
        return v


class ProductSimpleSchema(BaseModel):
    id: int
    title: str


class ReviewPublicSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product: ProductSimpleSchema
    stars: int
    comment: Optional[str] = None
    created_at: datetime


class ReviewProductSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    stars: int
    comment: Optional[str] = None
    created_at: datetime
