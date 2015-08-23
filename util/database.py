import pymongo

def getDbConn():
    # Initialize a connection to the MongoDB.
    try:
        conn = pymongo.MongoClient('localhost', 27017)
        print("Connection to MongoDB was successful.")
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s" % e)
        return # Well fuck.
    db = conn.blog
    return db
