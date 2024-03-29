from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import gridfs
import base64
from io import BytesIO
from PIL import Image


uri = "mongodb+srv://guevarajosue637:v8FzPfzWkj5a7Pnj@tigerocr.z8x5i0u.mongodb.net/?retryWrites=true&w=majority&appName=TigerOCR"

client = MongoClient(uri, server_api=ServerApi("1"))


def get_Connection():
    try:
        client.admin.command("ping")
        
    except Exception as e:
        
        print(e)


def createDataUser(data: dict[str, str]):
    db = client["TigerOCR"]
    collection = db["users"]
    try:
        collection.insert_one(data)
    except Exception as e:
        print(e)


def saveImage(path_img, nis: str):
    db = client["TigerOCR"]
    collection = db["images"]
    filename = nis
    try: 
        with open(path_img, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        fs = gridfs.GridFS(db)
        field_id = fs.put(encoded_string, filename=filename)
        collection.insert_one({"filename": filename, "field_id": field_id, "nis": nis})
        
    except Exception as e:
        print(e)



def getImage(filename):
    db = client["TigerOCR"]
    collection = db["images"]
    fs = gridfs.GridFS(db)
    try:

        image = collection.find_one({"filename": filename})
        image = fs.get(image["field_id"])
        image = Image.open(BytesIO(base64.b64decode(image.read())))
        return image
    except Exception as e:
        print(e)
        return None


def getAllUsers() -> list[dict[str, str]]:
    db = client["TigerOCR"]
    collection = db["users"]
    try:
        res = collection.find({}, {"_id": 0})
        return [user for user in res]
    except Exception as e:
        print(e)
        return None
