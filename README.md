# proj5-mongo
Simple list of dated memos kept in MongoDB database

## What is here

A simple Flask app that displays all the dated memos it finds in a MongoDB database in date order.
The user can add dated memos on a separate page by clicking the Create button. The user
can also delete memos from their list.

## Author

Megan McMillan

## Location on ix

http://ix.cs.uoregon.edu/~mcmillan/htbin/cis399/proj5-mongo/

## Setting up

Clone the repository, modify environment variables to the environment you're working in, and run
```
make install
```
Then start the environment
```
. env/bin/activate
```

Use mongoctl on ix to create your database.  On your own computer, 'mongod' is the program that starts the database process.  

You will need to create an administrative user for your database, and a non-administrative user with readWrite access to a
'memos' database.  Note that MongoDB on ix is version 2.4, while your computer probably has version 3.x.  The procedures for
adding a user are somewhat different between versions. In Python, the pymongo API works with both versions of MongoDB, so it's only the initial setup where you have to be careful to use the right version-specific commands.

After the database is set up and running, type the following to run the application
```
python3 flask_main.py
```
You can then navigate to localhost:5000 if on your own computer or ix.cs.uoregon.edu:PORTNUM if you're on ix.
