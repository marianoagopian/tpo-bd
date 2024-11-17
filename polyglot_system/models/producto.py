from pydantic import BaseModel

class Producto(BaseModel):
    codigo_producto: int
    marca: str
    nombre: str
    descripcion: str
    precio: float
    stock: int

class ProductoResponse(Producto):
    class Config:
        from_attributes = True