import pymongo

"""
Request a database connection. If the connection is successful a reference to
the database 'db' will be returned.
Optionally a host and a port can be specified. The default parameters of these are
'localhost' and 27017 respectively.
"""
def getDbConn(db, host = 'localhost', port = 27017):
    # Initialize a connection to the MongoDB.
    try:
        conn = pymongo.MongoClient(host, port)
    except pymongo.errors.ConnectionFailure as e:
        return None
    dbc = conn.db
    return dbc
