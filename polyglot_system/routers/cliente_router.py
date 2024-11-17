from fastapi import APIRouter, HTTPException
from typing import List
from models.cliente import Cliente
from models.queries import ClienteResponse
from db.database import cliente_collection

router = APIRouter()

# Crear un nuevo cliente
@router.post("/", response_model=Cliente)
async def create_cliente(cliente: Cliente):
    existing_cliente = cliente_collection.find_one({"nro_cliente": cliente.nro_cliente})
    if existing_cliente:
        raise HTTPException(status_code=400, detail="Cliente ya existe")
    
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
    cliente = cliente_collection.find_one({"nro_cliente": nro_cliente})
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

# Eliminar un cliente
@router.delete("/{nro_cliente}")
async def delete_cliente(nro_cliente: int):
    result = cliente_collection.delete_one({"nro_cliente": nro_cliente})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {"message": "Cliente eliminado correctamente"}

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
