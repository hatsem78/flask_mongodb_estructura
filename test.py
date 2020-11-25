import pymongo
client = pymongo.MongoClient(
    "mongodb://compensar2:compensar2@18.220.38.225:27017/compensar")
db = client.compensar
posts = db.usuarios

# imprime el número de elementos en la colección.
print(posts.count())
