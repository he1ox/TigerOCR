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
        print("Connected to MongoDB")
    except Exception as e:
        print("Not connected to MongoDB")
        print(e)


def createDataUser(data: dict[str, str]):
    db = client["TigerOCR"]
    collection = db["users"]
    collection.insert_one(data)


def saveImage(path_img, nis: str):
    print(f"path_img: {path_img}")
    db = client["TigerOCR"]
    collection = db["images"]
    filename = nis
    with open(path_img, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    fs = gridfs.GridFS(db)
    field_id = fs.put(encoded_string, filename=filename)
    collection.insert_one({"filename": filename, "field_id": field_id, "nis": nis})
    return field_id


def getImage(filename):
    db = client["TigerOCR"]
    collection = db["images"]
    fs = gridfs.GridFS(db)
    image = collection.find_one({"filename": filename})
    image = fs.get(image["field_id"])
    image = Image.open(BytesIO(base64.b64decode(image.read())))
    return image


def getAllUsers():
    db = client["TigerOCR"]
    collection = db["users"]
    return collection.find({}, {"_id": 0})
