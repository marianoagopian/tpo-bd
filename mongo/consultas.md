# 1. Obtener los datos de los clientes junto con sus teléfonos

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