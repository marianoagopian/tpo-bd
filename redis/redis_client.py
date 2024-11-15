import redis
import pandas as pd

# Conexión a Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Cargar datos del CSV usando pandas con encoding latin1
df = pd.read_csv('./data/e01_cliente.csv', encoding='latin1', delimiter=';')

# Iterar sobre cada fila del DataFrame y guardar en Redis
for index, row in df.iterrows():
    nro_cliente = row['nro_cliente']
    nombre = row['nombre']
    apellido = row['apellido']
    direccion = row['direccion']
    activo = row['activo']
    
    # Usar un hash para almacenar los datos del cliente
    cliente_key = f"cliente:{nro_cliente}"
    r.hset(cliente_key, mapping={
        'nombre': nombre,
        'apellido': apellido,
        'direccion': direccion,
        'activo': activo
    })


df = pd.read_csv('./data/e01_detalle_factura.csv', encoding='latin1', delimiter=';')

# Iterar sobre cada fila del DataFrame y guardar en Redis
for index, row in df.iterrows():
    nro_factura = row['nro_factura']
    codigo_producto = row['codigo_producto']
    nro_item = row['nro_item']
    cantidad = row['cantidad']
    
    # Usar un hash para almacenar los datos del cliente
    cliente_key = f"detalle_factura:{nro_factura}"
    r.hset(cliente_key, mapping={
        'nro_factura': nro_factura,
        'codigo_producto': codigo_producto,
        'nro_item': nro_item,
        'cantidad': cantidad
    })

df = pd.read_csv('./data/e01_factura.csv', encoding='latin1', delimiter=';')

# Iterar sobre cada fila del DataFrame y guardar en Redis
for index, row in df.iterrows():
    nro_factura = row['nro_factura']
    fecha = row['fecha']
    total_sin_iva = row['total_sin_iva']
    iva = row['iva']
    total_con_iva = row['total_con_iva']
    nro_cliente = row['nro_cliente']
    
    # Usar un hash para almacenar los datos del cliente
    cliente_key = f"factura:{nro_factura}"
    r.hset(cliente_key, mapping={
        'fecha': fecha,
        'total_sin_iva': total_sin_iva,
        'iva': iva,
        'total_con_iva': total_con_iva,
        'nro_cliente': nro_cliente
    })

df = pd.read_csv('./data/e01_producto.csv', encoding='latin1', delimiter=';')

# Iterar sobre cada fila del DataFrame y guardar en Redis
for index, row in df.iterrows():
    codigo_producto = row['codigo_producto']
    marca = row['marca']
    nombre = row['nombre']
    descripcion = row['descripcion']
    precio = row['precio']
    stock = row['stock']
    
    # Usar un hash para almacenar los datos del cliente
    cliente_key = f"producto:{codigo_producto}"
    r.hset(cliente_key, mapping={
        'marca': marca,
        'nombre': nombre,
        'descripcion': descripcion,
        'precio': precio,
        'stock': stock
    })

df = pd.read_csv('./data/e01_telefono.csv', encoding='latin1', delimiter=';')

# Iterar sobre cada fila del DataFrame y guardar en Redis
for index, row in df.iterrows():
    codigo_area = row['codigo_area']
    nro_telefono = row['nro_telefono']
    tipo = row['tipo']
    nro_cliente = row['nro_cliente']
    
    # Usar un hash para almacenar los datos del cliente
    cliente_key = f"telefono:{codigo_area}"
    r.hset(cliente_key, mapping={
        'nro_telefono': nro_telefono,
        'tipo': tipo,
        'nro_cliente': nro_cliente,
    })

print("Datos cargados en la base de datos")