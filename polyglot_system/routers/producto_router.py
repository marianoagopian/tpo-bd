from fastapi import APIRouter, HTTPException
from typing import List
from models.producto import Producto, ProductoResponse
from db.database import producto_collection, redis_db

router = APIRouter()

# Crear un nuevo producto
@router.post("/", response_model=ProductoResponse)
async def create_producto(producto: Producto):
    # Verificar si el producto ya existe
    cached_producto = redis_db.hgetall(f"Producto:{producto.codigo_producto}")

    if cached_producto:
        raise HTTPException(status_code=400, detail="Producto ya existe")
    
    redis_db.hset(f"Producto:{producto.codigo_producto}", mapping= {
        'marca': producto.marca,
        'nombre': producto.nombre,
        'descripcion': producto.descripcion,
        'precio': producto.precio,
        'stock': producto.stock
    })

    new_producto = producto.dict()
    producto_collection.insert_one(new_producto)
    return new_producto

# Obtener todos los productos
@router.get("/", response_model=List[ProductoResponse])
async def get_all_productos():
    productos = list(producto_collection.find())
    return productos

# Obtener un producto por código
@router.get("/{codigo_producto}", response_model=ProductoResponse)
async def get_producto(codigo_producto: int):
    cached_producto = redis_db.hgetall(f"Producto:{codigo_producto}")

    if not cached_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    producto = producto_collection.find_one({"codigo_producto":codigo_producto})
    return producto

# Eliminar un producto
@router.delete("/{codigo_producto}")
async def delete_producto(codigo_producto: int):
    cached_producto = redis_db.hgetall(f"Producto:{codigo_producto}")

    if not cached_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    redis_db.delete(f"Producto:{codigo_producto}")

    producto_collection.delete_one({"codigo_producto": codigo_producto})

    return HTTPException(status_code=204, detail="Producto eliminado")

# Actualizar un producto
@router.put("/{codigo_producto}", response_model=Producto)
async def update_producto(producto_update: Producto):
    # Verificar si el producto existe
    existing_producto = redis_db.hgetall(f"Producto:{producto_update.codigo_producto}")
    
    if not existing_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Filtrar los campos que tienen valores no nulos
    update_data = producto_update.dict()
    redis_db.hset(f"Producto:{producto_update.codigo_producto}", mapping=update_data)

    # Actualizar solo los campos proporcionados
    producto_collection.update_one(
        {"codigo_producto": producto_update.codigo_producto},
        {"$set": update_data}
    )
    
    # Obtener el producto actualizado
    updated_producto = producto_collection.find_one({"codigo_producto": producto_update.codigo_producto})
    return updated_producto
