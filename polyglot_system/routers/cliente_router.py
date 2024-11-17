from fastapi import APIRouter, HTTPException
from typing import List
from models.cliente import Cliente
from models.queries import ClienteResponse
from db.database import cliente_collection, redis_db
import json

router = APIRouter()

# Crear un nuevo cliente
@router.post("/", response_model=Cliente)
async def create_cliente(cliente: Cliente):
    cached_cliente = redis_db.hgetall(f"Cliente:{cliente.nro_cliente}")
    
    if cached_cliente:
        # Si el cliente existe en Redis, lanzar un error
        raise HTTPException(status_code=400, detail="Cliente ya existe")
    
    redis_db.hset(f"Cliente:{cliente.nro_cliente}", mapping={
        'nombre': cliente.nombre,
        'apellido': cliente.apellido,
        'direccion': cliente.direccion,
        'activo': cliente.activo
    })

    new_cliente = cliente.dict()
    cliente_collection.insert_one(new_cliente)
    return new_cliente

# Obtener todos los clientes
@router.get("/", response_model=List[Cliente])
async def get_all_clientes():
    clientes = list(cliente_collection.find())
    return clientes

# Obtener un cliente por nro_cliente
@router.get("/{nro_cliente}", response_model=Cliente)
async def get_cliente(nro_cliente: int):
    # Primero verificar si el cliente está en caché (Redis)
    cached_cliente = redis_db.hgetall(f"Cliente:{nro_cliente}")
    
    if not cached_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    cliente = cliente_collection.find_one({"nro_cliente": nro_cliente})
    return cliente

# Eliminar un cliente
@router.delete("/{nro_cliente}")
async def delete_cliente(nro_cliente: int):
    # Verificar si el cliente está en Redis
    cached_cliente = redis_db.hgetall(f"Cliente:{nro_cliente}")
    
    if not cached_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    redis_db.delete(f"Cliente:{nro_cliente}")

    # Luego buscar el cliente en MongoDB para eliminarlo
    cliente_collection.delete_one({"nro_cliente": nro_cliente})
    
    return HTTPException(status_code=204, detail="Cliente eliminado")

# Actualizar un cliente
@router.put("/{nro_cliente}", response_model=Cliente)
async def update_cliente(nro_cliente: int, cliente_update: Cliente):
    # Verificar si el cliente existe
    existing_cliente = cliente_collection.find_one({"nro_cliente": nro_cliente})
    if not existing_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    # Filtrar los campos que tienen valores no nulos
    update_data = {k: v for k, v in cliente_update.dict().items() if v is not None}

    # Actualizar solo los campos proporcionados
    cliente_collection.update_one(
        {"nro_cliente": nro_cliente},
        {"$set": update_data}
    )
    
    # Obtener el cliente actualizado
    updated_cliente = cliente_collection.find_one({"nro_cliente": nro_cliente})
    return updated_cliente
