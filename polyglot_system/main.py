from fastapi import FastAPI
from routers import cliente_router, producto_router, queries_router

app = FastAPI()

# Incluir los routers para cada colección
app.include_router(cliente_router.router, prefix="/clientes", tags=["Clientes"])
app.include_router(producto_router.router, prefix="/productos", tags=["Productos"])
app.include_router(queries_router.router, prefix="/queries", tags=["Queries"])