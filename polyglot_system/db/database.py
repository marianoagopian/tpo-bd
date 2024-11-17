from pymongo import MongoClient

# Conexión a MongoDB
mongo_client = MongoClient("mongodb://localhost:27017")
mongo_db = mongo_client["mymongo"]

# Colecciones
cliente_collection = mongo_db["Cliente"]
factura_collection = mongo_db["Factura"]
detalle_factura_collection = mongo_db["DetalleFactura"]
producto_collection = mongo_db["Producto"]
telefono_collection = mongo_db["Telefono"]