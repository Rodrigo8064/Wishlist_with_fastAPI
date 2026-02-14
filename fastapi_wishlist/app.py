from fastapi import FastAPI, status

from fastapi_wishlist.routers import auth, favorites, products, reviews, users

app = FastAPI()

app.include_router(
    router=auth.router,
    prefix='/api/auth',
    tags=['authentication'],
)

app.include_router(
    router=users.router,
    prefix='/api/users',
    tags=['users'],
)

app.include_router(
    router=products.router,
    prefix='/api/products',
    tags=['products'],
)

app.include_router(
    router=reviews.router,
    prefix='/api/reviews',
    tags=['reviews'],
)

app.include_router(
    router=favorites.router,
    prefix='/api/favorites',
    tags=['favorites'],
)


@app.get('/health_check', status_code=status.HTTP_200_OK)
def health_check():
    return {'status': 'ok'}
