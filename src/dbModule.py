from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import DESCENDING, ASCENDING

from datetime import datetime

from parseUpdateToJson import *

# "Schema"
# _id: id of the update
# user_id: telegram chat id of the one making the update
# update: update in json format

# ============================================================================================================================

def getDbConnection(mongoUser, mongoPassword):
    # TODO: error handling

    uri = "mongodb+srv://{}:{}@istattracker.caqxjvw.mongodb.net/?appName=istattracker".format(mongoUser, mongoPassword)

    client = MongoClient(uri, server_api=ServerApi('1'))

    # Select database and collection
    db = client["istattracker-db"]
    collection = db["istattracker-collection-updates"]

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("DB Connection Check Success")
    except Exception as e:
        print(e)

    return collection

# ============================================================================================================================

def insertUpdate(collection, user_id, update):
    # check if same agentname

    # TODO: error handling
    lastUpdate = getLastUpdate(collection, user_id)

    if lastUpdate is not None:
        if lastUpdate['agent_name'] == update['agent_name'] and firstDTIsBeforeEqualsSecondDT(update, lastUpdate):
            raise Exception("Current update must be after the last update ({})".format(getIsoDtFromJsonUpdate(lastUpdate)))

    wrappedUpdate = {
        "user_id": user_id,
        "update": update,
    }
    result = collection.insert_one(wrappedUpdate)

    return result.inserted_id

# ============================================================================================================================

def getLastUpdate(collection, user_id):
    # TODO: error handling
    result = collection.find_one(
        {"user_id": user_id},
        sort=[
            ("update.date_(yyyy-mm-dd)", DESCENDING),
            ("update.time_(hh:mm:ss)", DESCENDING)
        ]        
    )
    return None if result is None else result['update']

# ============================================================================================================================

def delete4thNewest(collection, user_id):
    # TODO: error handling
    #Better to sort by lifetime ap, as it will only ever increase
    toDelete = collection.find_one(
        {"user_id": user_id},
        sort=[("update.lifetime_ap", DESCENDING)],
        skip=3
    )

    if toDelete:
        collection.find_one_and_delete({"_id": toDelete["_id"]})

# ============================================================================================================================

# Testing db connections
# dbConn = getDbConnection(mongoUser, mongoPassword)
# delete4thNewest(dbConn, 231395341)

# jsonUpdate = parseUpdateToJson(mockUpdate)
# result = insertUpdate(dbConn, 1, jsonUpdate)
# print(result)

# getTest = getLastUpdate(dbConn, 1)
# print(getTest)

# result = getLastUpdate(dbConn, 231395341)
# print(result)
