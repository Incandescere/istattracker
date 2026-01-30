from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import DESCENDING

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
    # check if update is all_time
    # check if update is outdated
    # check if same agentname

    # TODO: error handling
    lastUpdate = getlastUpdate(collection, user_id)

    
    if update['time_span'] != "all_time":
        raise Exception("Send me the ALL TIME update instead")

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

def getlastUpdate(collection, user_id):
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

# Testing db connections

# dbConn = getDbConnection(mongoUser, mongoPassword)
# jsonUpdate = parseUpdateToJson(mockUpdate)
# result = insertUpdate(dbConn, 1, jsonUpdate)
# print(result)

# getTest = getlastUpdate(dbConn, 1)
# print(getTest)

# result = getlastUpdate(dbConn, 231395341)
# print(result)
