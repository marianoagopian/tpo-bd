from pydantic import BaseModel
from typing import List
from models.telefono import Telefono

class ClienteResponse(BaseModel):
    nro_cliente: int
    nombre: str
    apellido: str
    direccion: str
    activo: int
    telefono: List[Telefono]

class TelefonoResponse(BaseModel):
    codigo_area: int
    nro_telefono: int
    tipo: str  # "F" para fijo, "C" para celular, etc.
    nro_cliente: int  # Relación con el cliente
    nombre: str
    apellido: str
    direccion: str
    activo: int

class ClienteResponseCount(BaseModel):
    nro_cliente: int
    nombre: str
    apellido: str
    cantidad_facturas: int

class ClienteResponseTotal(BaseModel):
    nombre: str
    apellido: str
    total_gastado: float

class FacturaResponseProd(BaseModel):
    nro_factura: int
    fecha: str
    total_sin_iva: float
    iva: int
    total_con_iva: float
    codigo_producto: int
    marca: str
    nombre: str
    descripcion: str
    cantidad: int