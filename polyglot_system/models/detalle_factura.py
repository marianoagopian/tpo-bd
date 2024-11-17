from pydantic import BaseModel

class DetalleFactura(BaseModel):
    nro_factura: int
    codigo_producto: int
    nro_item: int
    cantidad: int

class DetalleFacturaResponse(DetalleFactura):
    class Config:
        from_attributes = True
