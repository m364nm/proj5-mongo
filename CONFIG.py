"""
Configuration of 'memos' Flask app.
Edit to fit development or deployment environment.

"""

### Flask settings for ix
PORT=6291        # The port I run Flask on
SERVER_NAME = "ix.cs.uoregon.edu:{}".format(PORT)
DEBUG = False

### Flask settings for local machine
PORT=5000      # The port I run Flask on
DEBUG = True

### MongoDB settings
MONGO_PORT=27017 #  modify to where your mongodb is listening, ex: 27017 or 4570

### The following are for a Mongo user you create for accessing your
### memos database.  It should not be the same as your database administrator
### account.
MONGO_PW = "iremember"
MONGO_USER = "memoproj"
MONGO_URL = "mongodb://{}:{}@localhost:{}/memos".format(MONGO_USER,MONGO_PW,MONGO_PORT)
#MONGO_URL for ix
#MONGO_URL = "mongodb://{}:{}@ix.cs.uoregon.edu:{}/memos".format(MONGO_USER,MONGO_PW,MONGO_PORT)
