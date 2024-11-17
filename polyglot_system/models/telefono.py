from pydantic import BaseModel

class Telefono(BaseModel):
    codigo_area: int
    nro_telefono: int
    tipo: str  # "F" para fijo, "C" para celular, etc.
    nro_cliente: int  # Relación con el cliente
