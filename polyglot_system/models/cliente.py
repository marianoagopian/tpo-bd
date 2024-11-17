from pydantic import BaseModel

class Cliente(BaseModel):
    nro_cliente: int
    nombre: str
    apellido: str
    direccion: str
    activo: int