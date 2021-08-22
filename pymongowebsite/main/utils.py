from pymongo import MongoClient 

# create database
def get_db_handle(db_name, host, port, username, password):

    #input host, username, password, etc
    client = MongoClient(host,
            port,
            username=username,
            password=password
            )

    #client= MongoClient("mongodb://QuintonPang:quinton@localhost:27017/")

    #create database
    db_handle = client[db_name]

    #return created database
    return db_handle, client


def get_collection_handle(db_handle, collection_name):

    #create collection named "counters" for incrementing _id
    counters=db_handle["counters"]

    #create collection
    return counters,db_handle[collection_name]


def getNextSequence(name,counters):

    #equivalent to db.counters.findAndModify() in mongo

    sequence= counters.find_one_and_update(

    { "_id": name },

    { "$inc": { "seq": 1 }} ,

    new=True 
    )


    return sequence.get("seq")
