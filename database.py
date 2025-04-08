from pymongo import MongoClient
import os

CONN_STRING = ("mongodb://sendgridemail:aEAYXxZVrhILrAwhxmMkGav8AgaomAJGKQDQIvhtFVv5A3kwQwD0vyswn933L6ZV5wld17kcbcWCACDbBLB7TA==@sendgridemail.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@sendgridemail@")
client = MongoClient(CONN_STRING)
db = client["carworkshop"]
collection = db["appointments"]
