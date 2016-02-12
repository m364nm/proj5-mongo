"""
Just to test database functions,
outside of Flask.

We want to open our MongoDB database,
insert some memos, and read them back
"""
import arrow
import bson
# Mongo database
from pymongo import MongoClient

from bson import ObjectId

import CONFIG
try:
    dbclient = MongoClient(CONFIG.MONGO_URL)
    db = dbclient.memos
    collection = db.dated
    print("successfuly opened mongodb")

except:
    print("Failure opening database.  Is Mongo running? Correct password?")
    sys.exit(1)



def new_memo(date, text):
    record = { "type": "dated_memo",
               "date":  date,
               "text": text
              }
    collection.insert(record)

def remove_memo(objId):
    return collection.remove( { "_id": objId })


def remove_memos(objId_list):
    results = []
    for obj in objId_list:
        test = ObjectId(obj)
        res = collection.remove( { "_id": test})
        results.append(res)
    return results


def get_memos():
    """
    Returns all memos in the database, in a form that
    can be inserted directly in the 'session' object.
    """
    records = [ ]
    for record in collection.find( { "type": "dated_memo" } ):
        record['date'] = arrow.get(record['date']).isoformat()
        #del record['_id']
        records.append(record)
    return records

#
# Insertions:  I commented these out after the first
# run successfuly inserted them
#
#print("before new memos")
#records = get_memos()
#print(records)

#new_memo(arrow.utcnow().naive, "Random Test Woot!")
#new_memo(arrow.utcnow().replace(days=+1).naive, "Sample test")

#
# Read database --- May be useful to see what is in there,
# even after you have a working 'insert' operation in the flask app,
# but they aren't very readable.  If you have more than a couple records,
# you'll want a loop for printing them in a nicer format.
#
print("after new memos")
#records = get_memos()
#print(records)
#print("\n")

for record in collection.find({"text":"Random Test Woot!"}):
    result = remove_memo(record["_id"])
    print(result)

print("after first delete")
records = get_memos()
#print(records)

arr = ['56bd52298d1fa7627b6f3274', '56bc396e8d1fa75dc3c5f4c6']
result = remove_memos(arr)
print(result)

print("after second delete")
records = get_memos()
#print(records)
