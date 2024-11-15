from pymongo import MongoClient
import pandas as pd

file_path = './data/e01_producto.csv'
data = pd.read_csv(file_path, delimiter=';')

client = MongoClient("mongodb://localhost:27017/")
db = client["facturacion"]
collection = db["productos"]
data_dict = data.to_dict("records")
collection.insert_many(data_dict)
print("Datos insertados en MongoDB.")