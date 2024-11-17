from pydantic import BaseModel

class Factura(BaseModel):
    nro_factura: int
    fecha: str
    total_sin_iva: float
    iva: int
    total_con_iva: float
    nro_cliente: int

class FacturaResponse(Factura):
    class Config:
        from_attributes = True
