# Queries

## 1. Obtener los datos de los clientes junto con sus teléfonos.

```
db.Cliente.aggregate([
  {
    $lookup: {
      from: "Telefono",
      localField: "nro_cliente",
      foreignField: "nro_cliente",
      as: "telefonos",
    },
  },
  {
    $project: {
      _id: 0,
      nombre: 1,
      apellido: 1,
      direccion: 1,
      activo: 1,
      nro_cliente: 1,
      telefonos: {
        codigo_area: 1,
        nro_telefono: 1,
        tipo: 1,
      },
    },
  },
  {
    $unwind: "$telefonos",
  },
  {
    $group: {
      _id: "$nro_cliente",
      nombre: { $first: "$nombre" },
      apellido: { $first: "$apellido" },
      direccion: { $first: "$direccion" },
      activo: { $first: "$activo" },
      telefonos: { $push: "$telefonos" },
    },
  },
  {
    $project: {
      _id: 0,
      nombre: 1,
      apellido: 1,
      direccion: 1,
      activo: 1,
      nro_cliente: "$_id",
      telefonos: 1,
    },
  },
  {
    $sort: { nro_cliente: 1},
  },
])
```

# 2. Obtener el/los teléfono/s y el número de cliente del cliente con nombre “Jacob” y apellido “Cooper”.

```
db.Cliente.aggregate([
  {
    $match: {
      nombre: "Jacob",
      apellido: "Cooper"
    }
  },
  {
    $lookup: {
      from: "Telefono",
      localField: "nro_cliente",
      foreignField: "nro_cliente",
      as: "telefonos"
    }
  },
  {
    $project: {
      _id: 0,
      nombre: 1,
      apellido: 1,
      nro_cliente: 1,
      telefonos: {
        codigo_area: 1,
        nro_telefono: 1,
        tipo: 1
      }
    }
  }
]);
```

# 3. Mostrar cada teléfono junto con los datos del cliente.

```
db.Cliente.aggregate([
  {
    $lookup: {
      from: "Telefono",
      localField: "nro_cliente",
      foreignField: "nro_cliente",
      as: "telefonos"
    }
  },
  {
    $project: {
      _id: 0,
      nro_cliente: 1,
      nombre: 1,
      apellido: 1,
      direccion: 1,
      activo: 1,
      telefonos: 1
    }
  },
  {
    $unwind: "$telefonos"
  },
  {
    $project: {
      _id: 0,
      nro_cliente: 1,
      nombre: 1,
      apellido: 1,
      direccion: 1,
      activo: 1,
      codigo_area: "$telefonos.codigo_area",
      nro_telefono: "$telefonos.nro_telefono",
      tipo: "$telefonos.tipo"
    }
  }
]);
```

# 4. Obtener todos los clientes que tengan registrada al menos una factura.

```
db.Cliente.aggregate([
  {
    $lookup: {
      from: "Factura",
      localField: "nro_cliente",
      foreignField: "nro_cliente",
      as: "has_factura",
    },
  },
  {
    $match: {
      has_factura: { $exists: true, $ne: [] },
    },
  },
  {
    $project: {
      _id: 0,
      nro_cliente: 1,
      nombre: 1,
      apellido: 1,
    },
  },
]);
```

# 5. Identificar todos los clientes que no tengan registrada ninguna factura.

```
db.Cliente.aggregate([
  {
    $lookup: {
      from: "Factura",
      localField: "nro_cliente",
      foreignField: "nro_cliente",
      as: "has_factura",
    },
  },
  {
    $match: {
      has_factura: { $exists: true, $eq: [] },
    },
  },
  {
    $project: {
      _id: 0,
      nro_cliente: 1,
      nombre: 1,
      apellido: 1,
    },
  },
]);
```

# 6. Devolver todos los clientes, con la cantidad de facturas que tienen registradas (si no tienen, considerar cantidad en 0).

```
db.Cliente.aggregate([
{
  $lookup: {
    from: "Factura",
    localField: "nro_cliente",
    foreignField: "nro_cliente",
    as: "facturas"
  }
},
{
  $addFields: {
    cantidad_facturas: { $size: { $ifNull: ["$facturas", []] } }
  }
},
{
  $project: {
    _id: 0,
    nro_cliente: 1,
    nombre: 1,
    apellido: 1,
    cantidad_facturas: 1
  }
}
]);
```

# 7. Listar los datos de todas las facturas que hayan sido compradas por el cliente de nombre "Kai" y apellido "Bullock".

```
db.Cliente.aggregate([
  {
    $match: {
      nombre: "Kai",
      apellido: "Bullock"
    }
  },
  {
    $lookup: {
      from: "Factura",
      localField: "nro_cliente",
      foreignField: "nro_cliente",
      as: "facturas"
    }
  },
  {
    $unwind: "$facturas",
  },
  {
    $replaceRoot: { newRoot: "$facturas" },
  }
]);
```

# 8. Seleccionar los productos que han sido facturados al menos 1 vez.

```
db.Producto.aggregate([
  {
    $lookup: {
      from: "DetalleFactura",
      localField: "codigo_producto",
      foreignField: "codigo_producto",
      as: "has_factura",
    },
  },
  {
    $match: {
      has_factura: { $exists: true, $ne: [] },
    },
  },
  {
    $project: {
      _id: 0,
      codigo_producto: 1,
      marca: 1,
      nombre: 1,
      descripcion: 1,
      precio: 1,
      stock: 1,
    },
  },
]);
```

# 9. Listar los datos de todas las facturas que contengan productos de las marcas “Ipsum”.

```
db.DetalleFactura.aggregate([
  {
    $lookup: {
      from: "Factura",
      localField: "nro_factura",
      foreignField: "nro_factura",
      as: "factura_info"
    }
  },
  {
    $unwind: "$factura_info"
  },
  {
    $lookup: {
      from: "Producto",
      localField: "codigo_producto",
      foreignField: "codigo_producto",
      as: "producto_info"
    }
  },
  {
    $unwind: "$producto_info"
  },
  {
    $match: {
      "producto_info.marca": { $regex: "Ipsum", $options: "i" }
    }
  },
  {
    $project: {
      _id: 0,
      nro_factura: "$factura_info.nro_factura",
      fecha: "$factura_info.fecha",
      total_sin_iva: "$factura_info.total_sin_iva",
      iva: "$factura_info.iva",
      total_con_iva: "$factura_info.total_con_iva",
      codigo_producto: "$producto_info.codigo_producto",
      marca: "$producto_info.marca",
      nombre: "$producto_info.nombre",
      descripcion: "$producto_info.descripcion",
      cantidad: "$cantidad"
    }
  }
]);
```

# 10. Mostrar nombre y apellido de cada cliente junto con lo que gastó en total, con IVA incluido.

```
db.Cliente.aggregate([
  {
    $lookup: {
      from: "Factura",
      localField: "nro_cliente",
      foreignField: "nro_cliente",
      as: "facturas"
    }
  },
  {
    $unwind: "$facturas"
  },
  {
    $group: {
      _id: { nro_cliente: "$nro_cliente", nombre: "$nombre", apellido: "$apellido" },
      total_gastado: { $sum: "$facturas.total_con_iva" }
    }
  },
  {
    $project: {
      _id: 0,
      nombre: "$_id.nombre",
      apellido: "$_id.apellido",
      total_gastado: 1
    }
  }
]);
```

# 11. Se necesita una vista que devuelva los datos de las facturas ordenadas por fecha.

```
db.createCollection("FacturasOrdenadas", {
  viewOn: "Factura",
  pipeline: [
    { $sort: { fecha: 1 } }
  ]
});
```

# 12. Se necesita una vista que devuelva todos los productos que aún no han sido facturados.
```
```

# 13. Implementar la funcionalidad que permita crear nuevos clientes, eliminar y modificar los ya existentes.
```
```

# 14. Implementar la funcionalidad que permita crear nuevos productos y modificar los ya existentes. Tener en cuenta que el precio de un producto es sin IVA.
