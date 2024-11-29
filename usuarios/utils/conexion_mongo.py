
from pymongo import MongoClient, errors
from pymongo.errors import OperationFailure


def conectar_mongobb(MONGO_HOST = "localhost", MONGO_PORT = "27017", MONGO_DB = "Ejemplo", MONGO_TIMEOUT = 1000):
    try:
        MONGO_URI = "mongodb://localhost:27017"
        #MONGO_URI = "mongodb+srv://hugorojas:admin1234@itj-desarrollo.yi09p.mongodb.net/?retryWrites=true&w=majority&appName=ITJ-DESARROLLO"
        MONGO_CLIENT = MongoClient(MONGO_URI)
        try:
            return MONGO_CLIENT
        except OperationFailure as error:
            return "Error en la operación "+ str(error)
    except errors.ServerSelectionTimeoutError as err:
        return "Tiempo excedido ->" + str(err)