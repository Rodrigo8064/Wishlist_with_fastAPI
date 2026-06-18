from fastapi import FastAPI, status

from fastapi_wishlist.routers import auth, favorites, products, reviews, users

app = FastAPI(
    title='Wishlist API',
    description="""
API de lista de desejos para e-commerce.

## Como testar

Use as credenciais abaixo para autenticar:

| campo | valor |
|-------|-------|
| email | recrutador@teste.com |
| senha | teste123 |

**Passo a passo:**
1. Faça POST /api/auth/token com as credenciais acima
2. Copie o access_token retornado
3. Clique em **Authorize** 🔒 no topo da página
4. Cole o token no campo **Value** e clique em Authorize
5. Explore os endpoints à vontade!
    """,
    version='1.0.0',
)


@app.get('/health_check', status_code=status.HTTP_200_OK)
def health_check():
    return {'status': 'ok'}


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
