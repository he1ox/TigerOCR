from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://guevarajosue637:v8FzPfzWkj5a7Pnj@tigerocr.z8x5i0u.mongodb.net/?retryWrites=true&w=majority&appName=TigerOCR"

client = MongoClient(uri, server_api=ServerApi("1"))


def get_Connection():
    try:
        client.admin.command("ping")
        print("Connected to MongoDB")
    except Exception as e:
        print("Not connected to MongoDB")
        print(e)

def createDataUser(data: dict[str, str]):
    db = client["TigerOCR"]
    collection = db["users"]
    collection.insert_one(data)
    print("Data inserted")
