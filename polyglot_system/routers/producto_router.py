from fastapi import APIRouter, HTTPException
from typing import List
from models.producto import Producto, ProductoResponse
from db.database import producto_collection  

router = APIRouter()

# Crear un nuevo producto
@router.post("/", response_model=ProductoResponse)
async def create_producto(producto: Producto):
    # Verificar si el producto ya existe
    existing_producto = producto_collection.find_one({"codigo_producto": producto.codigo_producto})
    if existing_producto:
        raise HTTPException(status_code=400, detail="Producto ya existe")
    
    # Insertar producto en la base de datos
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
    producto = producto_collection.find_one({"codigo_producto": codigo_producto})
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

# Eliminar un producto
@router.delete("/{codigo_producto}")
async def delete_producto(codigo_producto: int):
    result = producto_collection.delete_one({"codigo_producto": codigo_producto})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Producto eliminado correctamente"}

# Actualizar un producto
@router.put("/{codigo_producto}", response_model=Producto)
async def update_producto(codigo_producto: int, producto_update: Producto):
    # Verificar si el producto existe
    existing_producto = producto_collection.find_one({"codigo_producto": codigo_producto})
    if not existing_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Filtrar los campos que tienen valores no nulos
    update_data = {k: v for k, v in producto_update.dict().items() if v is not None}

    # Actualizar solo los campos proporcionados
    producto_collection.update_one(
        {"codigo_producto": codigo_producto},
        {"$set": update_data}
    )
    
    # Obtener el producto actualizado
    updated_producto = producto_collection.find_one({"codigo_producto": codigo_producto})
    return updated_producto
