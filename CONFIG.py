"""
Configuration of 'memos' Flask app.
Edit to fit development or deployment environment.

"""

### Flask settings
PORT=6291        # The port I run Flask on
SERVER_NAME = "ix.cs.uoregon.edu:{}".format(PORT)
DEBUG = False     # Set to False on ix

### MongoDB settings
MONGO_PORT=4570 #  Probably best to use the same port as you use on ix

### The following are for a Mongo user you create for accessing your
### memos database.  It should not be the same as your database administrator
### account.
MONGO_PW = "iremember"
MONGO_USER = "memoproj"
MONGO_URL = "mongodb://{}:{}@ix.cs.uoregon.edu:{}/memos".format(MONGO_USER,MONGO_PW,MONGO_PORT)
