# TPO-BasesDeDatos2
## Trabajo Práctico Obligatorio Base de Datos II ITBA 2C2024

## Integrantes

| Legajo | Nombre y Apellido       | Github         |
|--------|-------------------------|----------------|
| 62317  | Mariano Agopian         | marianoagopian |
| 62358  | Axel Castro Benza       | AxelCastroo    |
| 60505  | Lautaro Farias          | LautiFarias    |


## Consultas

Las queries, vistas y funcionalidades pedidas se encuentran dentro de la carpeta "consultas"

## Data

La data fuente del trabajo se encuentra dentro de la carpeta "data".

## Documentos

La consigna del trabajo se encuentra dentro de la carpeta "doc"

## API

La API se encuentra dentro de la carpeta "polyglot_system"

# Respuestas al Enunciado

## MongoDB
Se utiliza el contenedor de docker que se instala en la práctica de la materia.

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

## Redis
Se utiliza el contenedor de docker que se instala en la práctica de la materia.

Los datos se cargan automáticamente una vez inicializada la API

## API
Tras tener los archvivos csv en MongoDB, se deben ejecutar los siguientes comandos para generar las dependencias necesarias para el funcionamiento de la API:

```
# Navegar al directorio del proyecto
cd polyglot_system
# Crear un entorno virtual en Python
python3 -m venv venv
# Activar el entorno virtual:
# En Mac/Linux:
source venv/bin/activate
# En Windows:
venv\Scripts\activate
# Instalar las dependencias necesarias
pip install fastapi uvicorn pymongo redis pandas
```

Para inicializar la API:
```
uvicorn main:app --reload
```
Tras esto, se puede acceder a la misma en: <u>http://127.0.0.1:8000/docs#/</u>