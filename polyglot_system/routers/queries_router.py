from fastapi import APIRouter, HTTPException
from typing import List
from models.queries import ClienteResponse, TelefonoResponse, ClienteResponseCount, FacturaResponseProd, ClienteResponseTotal
from models.cliente import Cliente
from models.factura import FacturaResponse
from models.producto import ProductoResponse
from db.database import cliente_collection, detalle_factura_collection, producto_collection, mongo_db

router = APIRouter()

@router.get("/clientes_con_telefonos", response_model=List[ClienteResponse])
async def get_clientes_con_telefonos():
    aggregation_pipeline = [
        {
            "$lookup": {
                "from": "Telefono",
                "localField": "nro_cliente",
                "foreignField": "nro_cliente",
                "as": "telefono"
            }
        },
        {
            "$project": {
                "_id": 0,
                "nro_cliente": 1,
                "nombre": 1,
                "apellido": 1,
                "direccion": 1,
                "activo": 1,
                "telefono": {
                    "$map": {
                        "input": "$telefono",
                        "as": "telefono",
                        "in": {
                            "nro_cliente": "$$telefono.nro_cliente",  
                            "codigo_area": "$$telefono.codigo_area",
                            "nro_telefono": "$$telefono.nro_telefono",
                            "tipo": "$$telefono.tipo"
                        }
                    }
                }
            }
        }
    ]

    result = list(cliente_collection.aggregate(aggregation_pipeline))
    return result

@router.get("/info_de_Jacob_Cooper", response_model=List[ClienteResponse])
async def get_info_de_Jacob_Cooper():
    aggregation_pipeline = [
        {
            "$match": {
                "nombre": "Jacob",
                "apellido": "Cooper"
            }
        },
        {
            "$lookup": {
                "from": "Telefono",
                "localField": "nro_cliente",
                "foreignField": "nro_cliente",
                "as": "telefonos"
            }
        },
        {
            "$project": {
                "_id": 0,
                "nombre": 1,
                "apellido": 1,
                "nro_cliente": 1,
                "telefonos": {
                    "codigo_area": 1,
                    "nro_telefono": 1,
                    "tipo": 1
                },
                "direccion": {"$ifNull": ["$direccion", ""]},  # Asigna una cadena vacía si no existe 'direccion'
                "activo": {"$ifNull": ["$activo", True]},     # Asigna True si no existe 'activo'
                "telefono": {"$ifNull": ["$telefonos", []]}   # Devuelve una lista vacía si no hay teléfonos
            }
        }
    ]
    
    result = list(cliente_collection.aggregate(aggregation_pipeline))
    return result


@router.get("/telefono_con_cliente", response_model=List[TelefonoResponse])
async def get_telefono_con_cliente():
    aggregation_pipeline = [
    {
        '$lookup': {
            'from': 'Telefono',
            'localField': 'nro_cliente',
            'foreignField': 'nro_cliente',
            'as': 'telefonos'
        }
    },
    {
        '$project': {
            '_id': 0,
            'nro_cliente': 1,
            'nombre': 1,
            'apellido': 1,
            'direccion': 1,
            'activo': 1,
            'telefonos': 1
        }
    },
    {
        '$unwind': '$telefonos'
    },
    {
        '$project': {
            '_id': 0,
            'nro_cliente': 1,
            'nombre': 1,
            'apellido': 1,
            'direccion': 1,
            'activo': 1,
            'codigo_area': '$telefonos.codigo_area',
            'nro_telefono': '$telefonos.nro_telefono',
            'tipo': '$telefonos.tipo'
        }
    }
]

    result = list(cliente_collection.aggregate(aggregation_pipeline))
    return result


@router.get("/clientes_con_al_menos_una_factura", response_model=List[Cliente])
async def get_clientes_con_al_menos_una_factura():
    aggregation_pipeline = [
    {
        "$lookup": {
            "from": "Factura",
            "localField": "nro_cliente",
            "foreignField": "nro_cliente",
            "as": "has_factura"
        }
    },
    {
        "$match": {
            "has_factura": {"$exists": True, "$ne": []}
        }
    },
    {
        "$project": {
            "_id": 0,
            "nro_cliente": 1,
            "nombre": 1,
            "apellido": 1,
            "direccion": 1,  
            "activo": 1,     
        }
    }
    ]

    result = list(cliente_collection.aggregate(aggregation_pipeline))
    return result

@router.get("/clientes_que_no_tengan_una_factura", response_model=List[Cliente])
async def get_clientes_que_no_tengan_una_factura():
    aggregation_pipeline = [
    {
        "$lookup": {
            "from": "Factura",
            "localField": "nro_cliente",
            "foreignField": "nro_cliente",
            "as": "has_factura"
        }
    },
    {
        "$match": {
            "has_factura": {"$exists": True, "$eq": []}
        }
    },
    {
        "$project": {
            "_id": 0,
            "nro_cliente": 1,
            "nombre": 1,
            "apellido": 1,
            "direccion": 1,  
            "activo": 1,     
        }
    }
    ]

    result = list(cliente_collection.aggregate(aggregation_pipeline))
    return result

@router.get("/clientes_con_cantidad_de_facturas", response_model=List[ClienteResponseCount])
async def get_clientes_con_cantidad_de_facturas():
    aggregation_pipeline = [
    {
        '$lookup': {
            'from': 'Factura',
            'localField': 'nro_cliente',
            'foreignField': 'nro_cliente',
            'as': 'facturas'
        }
    },
    {
        '$addFields': {
            'cantidad_facturas': {'$size': {'$ifNull': ['$facturas', []]}}
        }
    },
    {
        '$project': {
            '_id': 0,
            'nro_cliente': 1,
            'nombre': 1,
            'apellido': 1,
            'cantidad_facturas': 1
        }
    }
    ]

    result = list(cliente_collection.aggregate(aggregation_pipeline))
    return result

@router.get("/facturas_compradas_por_Kai_Bullock", response_model=List[FacturaResponse])
async def get_facturas_compradas_por_Kai_Bullock():
    aggregation_pipeline = [
    {
        '$match': {
            'nombre': 'Kai',
            'apellido': 'Bullock'
        }
    },
    {
        '$lookup': {
            'from': 'Factura',
            'localField': 'nro_cliente',
            'foreignField': 'nro_cliente',
            'as': 'facturas'
        }
    },
    {
        '$unwind': '$facturas'
    },
    {
        '$replaceRoot': {'newRoot': '$facturas'}
    }
    ]

    result = list(cliente_collection.aggregate(aggregation_pipeline))
    return result

@router.get("/productos_facturados_al_menos_una_vez", response_model=List[ProductoResponse])
async def get_productos_facturados_al_menos_una_vez():
    aggregation_pipeline = [
    {
        "$lookup": {
            "from": "DetalleFactura",
            "localField": "codigo_producto",
            "foreignField": "codigo_producto",
            "as": "has_factura",
        }
    },
    {
        "$match": {
            "has_factura": {"$exists": True, "$ne": []}
        }
    },
    {
        "$project": {
            "_id": 0,
            "codigo_producto": 1,
            "marca": 1,
            "nombre": 1,
            "descripcion": 1,
            "precio": 1,
            "stock": 1,
        }
    }
]

    result = list(producto_collection.aggregate(aggregation_pipeline))
    return result

@router.get("/facturas_con_productos_Ipsum", response_model=List[FacturaResponseProd])
async def get_facturas_con_productos_Ipsum():
    aggregation_pipeline = [
    {
        "$lookup": {
            "from": "Factura",
            "localField": "nro_factura",
            "foreignField": "nro_factura",
            "as": "factura_info"
        }
    },
    {
        "$unwind": "$factura_info"
    },
    {
        "$lookup": {
            "from": "Producto",
            "localField": "codigo_producto",
            "foreignField": "codigo_producto",
            "as": "producto_info"
        }
    },
    {
        "$unwind": "$producto_info"
    },
    {
        "$match": {
            "producto_info.marca": {"$regex": "Ipsum", "$options": "i"}
        }
    },
    {
        "$project": {
            "_id": 0,
            "nro_factura": "$factura_info.nro_factura",
            "fecha": "$factura_info.fecha",
            "total_sin_iva": "$factura_info.total_sin_iva",
            "iva": "$factura_info.iva",
            "total_con_iva": "$factura_info.total_con_iva",
            "codigo_producto": "$producto_info.codigo_producto",
            "marca": "$producto_info.marca",
            "nombre": "$producto_info.nombre",
            "descripcion": "$producto_info.descripcion",
            "cantidad": "$cantidad"
        }
    }
    ]

    result = list(detalle_factura_collection.aggregate(aggregation_pipeline))
    return result

@router.get("/cliente_con_total_gastado", response_model=List[ClienteResponseTotal])
async def get_cliente_con_total_gastado():
    aggregation_pipeline = [
    {
        "$lookup": {
            "from": "Factura",
            "localField": "nro_cliente",
            "foreignField": "nro_cliente",
            "as": "facturas"
        }
    },
    {
        "$unwind": "$facturas"
    },
    {
        "$group": {
            "_id": {
                "nro_cliente": "$nro_cliente",
                "nombre": "$nombre",
                "apellido": "$apellido"
            },
            "total_gastado": {"$sum": "$facturas.total_con_iva"}
        }
    },
    {
        "$project": {
            "_id": 0,
            "nombre": "$_id.nombre",
            "apellido": "$_id.apellido",
            "total_gastado": 1
        }
    }
    ]

    result = list(cliente_collection.aggregate(aggregation_pipeline))
    return result

if "FacturasOrdenadas" not in mongo_db.list_collection_names():
    mongo_db.create_collection(
        "FacturasOrdenadas",
        viewOn="Factura",
        pipeline=[
            {"$sort": {"fecha": 1}}
        ]
    )

@router.get("/vista_facturas_ordenadas", response_model=List[FacturaResponse])
async def get_vista_facturas_ordenadas():
    
    result = list(mongo_db.FacturasOrdenadas.find({}, {"_id": 0}))    
    return result

if "ProductosNoFacturados" not in mongo_db.list_collection_names():
    pipeline = [
        {
            "$lookup": {
                "from": "DetalleFactura",
                "localField": "codigo_producto",
                "foreignField": "DetalleFactura.codigo_producto",
                "as": "facturas"
            }
        },
        {
            "$match": {
                "facturas": []
            }
        },
        {
            "$project": {
                "_id": 1,
                "codigo_producto": 1,
                "marca": 1,
                "nombre": 1,
                "descripcion": 1,
                "precio": 1,
                "stock": 1
            }
        }
    ]

    mongo_db.create_collection(
        "ProductosNoFacturados", 
        viewOn="Producto", 
        pipeline=pipeline
    )

@router.get("/vista_productos_no_facturados", response_model=List[ProductoResponse])
async def get_vista_productos_no_facturados():
    
    result = list(mongo_db.ProductosNoFacturados.find({}, {"_id": 0}))    
    return result
