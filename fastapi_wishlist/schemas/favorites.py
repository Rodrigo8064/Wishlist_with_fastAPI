from pydantic import BaseModel, ConfigDict

from fastapi_wishlist.schemas.products import ProductPublicSchema


class FavoriteSchema(BaseModel):
    product_id: int


class FavoritePublicSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product: ProductPublicSchema
