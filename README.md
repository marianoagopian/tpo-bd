# TPO-BasesDeDatos2
## Trabajo Práctico Obligatorio Base de Datos II ITBA 2C2024

## Integrantes

| Legajo | Nombre y Apellido       | Github         |
|--------|-------------------------|----------------|
| 62317  | Mariano Agopian         | marianoagopian |
| 62358  | Axel Castro Benza       | AxelCastroo    |
| 60505  | Lautaro Farias          | LautiFarias    |


## Data

La data fuente del trabajo se encuentra dentro de la carpeta "data".

## Documentos

La consigna del trabajo se encuentra dentro de la carpeta "doc"

# Respuestas al Enunciado

## MongoDB
Para cargar la data de los csv dentro de nuestra base de datos Mongo lo que se hizo fue subir los archivos csv a docker con el comando <i>cp</i> de la siguiente manera:

```
  docker cp ./data/e01_cliente.csv Mymongo:/files/e01_cliente.csv
  docker cp ./data/e01_detalle_factura.csv Mymongo:/files/e01_detalle_factura.csv
  docker cp ./data/e01_factura.csv Mymongo:/files/e01_factura.csv
  docker cp ./data/e01_telefono.csv Mymongo:/files/e01_telefono.csv
  docker cp ./data/e01_producto.csv Mymongo:/files/e01_producto.csv
```

Luego dentro de docker se utilizó el comando <i>sed</i> para cambiar los separadores del csv de ; a , ya que sino surgían problemas al momento de importarlos dentro de la base de datos.
Esto se realizó de la siguiente manera:
```
  sed 's/;/,/g' /files/e01_cliente.csv > /files/e01_cliente_comas.csv
  sed 's/;/,/g' /files/e01_detalle_factura.csv > /files/e01_detalle_factura_comas.csv
  sed 's/;/,/g' /files/e01_factura.csv > /files/e01_factura_comas.csv
  sed 's/;/,/g' /files/e01_telefono.csv > /files/e01_telefono_comas.csv
  sed 's/;/,/g' /files/e01_producto.csv > /files/e01_producto_comas.csv
```

Una vez parseado los archivos se importaron los datos de los csv a colecciones dentro de la base de datos con el comando <i>mongoimport</i>. Esto se realizó de la siguiente manera:
```
  mongoimport --host localhost --db mymongo --collection Cliente --type csv --file /files/e01_cliente_comas.csv --headerline
  mongoimport --host localhost --db mymongo --collection DetalleFactura --type csv --file /files/e01_detalle_factura_comas.csv --headerline
  mongoimport --host localhost --db mymongo --collection Factura --type csv --file /files/e01_factura_comas.csv --headerline
  mongoimport --host localhost --db mymongo --collection Telefono --type csv --file /files/e01_telefono_comas.csv --headerline
  mongoimport --host localhost --db mymongo --collection Producto --type csv --file /files/e01_producto_comas.csv --headerline
```

Una vez ya cargada la base de datos, se siguió conectandose a la misma y ejecutando las queries que se encuentran en <i>./mongo/consultas.md</i>.

## Redis
Para cargar la data de los csv dentro de nuestra base de datos Redis se utilizó python. Lo que se hizo fue crear el archivo redis_client.py en el cual con la ayuda de la librería pandas, se abren los archivos csv, se itera por las filas y se cargan dentro de la base de datos.

Una vez ya cargada la base de datos, se siguió conectandose a la misma y ejecutando las queries que se encuentran en <i>./redis/consultas.md</i>.
