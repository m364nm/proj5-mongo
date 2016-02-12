"""
Flask web app connects to Mongo database.
Keep a simple list of dated memoranda.

Representation conventions for dates:
   - We use Arrow objects when we want to manipulate dates, but for all
     storage in database, in session or g objects, or anything else that
     needs a text representation, we use ISO date strings.  These sort in the
     order as arrow date objects, and they are easy to convert to and from
     arrow date objects.  (For display on screen, we use the 'humanize' filter
     below.) A time zone offset will
   - User input/output is in local (to the server) time.
"""

import flask
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify

import json
import bson
import logging
import sys

# Date handling
import arrow # Replacement for datetime, based on moment.js
import datetime # But we may still need time
from dateutil import tz  # For interpreting local times

# Mongo database
from pymongo import MongoClient
from bson import ObjectId

###
# Globals
###
import CONFIG

app = flask.Flask(__name__)

try:
    dbclient = MongoClient(CONFIG.MONGO_URL)
    db = dbclient.memos
    collection = db.dated
    print(" * Database is connected")

except:
    print("Failure opening database.  Is Mongo running? Correct password?")
    sys.exit(1)

import uuid
app.secret_key = str(uuid.uuid4())

###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
  app.logger.debug("Main page entry")
  flask.session['memos'] = get_memos()
  for memo in flask.session['memos']:
      app.logger.debug("Memo: " + str(memo))
  return flask.render_template('index.html')


@app.route("/create")
def create():
    app.logger.debug("Create")
    return flask.render_template('create.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('page_not_found.html',
                                 badurl=request.base_url,
                                 linkback=url_for("index")), 404

#################
#
# Functions used within the templates
#
#################

# NOT TESTED with this application; may need revision
#@app.template_filter( 'fmtdate' )
# def format_arrow_date( date ):
#     try:
#         normal = arrow.get( date )
#         return normal.to('local').format("ddd MM/DD/YYYY")
#     except:
#         return "(bad date)"

@app.template_filter( 'humanize' )
def humanize_arrow_date( date ):
    """
    Date is internal UTC ISO format string.
    Output should be "today", "yesterday", "in 5 days", etc.
    Arrow will try to humanize down to the minute, so we
    need to catch 'today' as a special case.
    """
    try:
        then = arrow.get(date)
        now = arrow.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        if then.date() == now.date():
            human = "Today"
        else:
            human = then.humanize(now)
            if human == "in a day":
                human = "Tomorrow"
            elif human == "a day ago":
                human = "Yesterday"
    except:
        human = date
    return human

@app.route('/_create')
def save_memo():
  '''
  submits the time and text into the memo database
  '''
  app.logger.debug("Got a JSON request");
  try:
      date = request.args.get('mdate')
      print(date)
      text = request.args.get('mtext')
      print(text)
      new_record = new_memo(date, text)
      new_record['_id'] = str(new_record['_id'])
      print("inserted new memo into db")
  except:
      app.logger.debug("Failed at create");

  return jsonify(result=new_record)

@app.route('/_delete')
def delete_memo():
  '''
  gives the object ids to delete from the database
  '''
  app.logger.debug("Got a JSON request");
  try:
      request_ids = request.args
      memos = request_ids.getlist("todelete[]")
      results = remove_memos(memos)
  except:
      app.logger.debug("Failed at delete");

  return jsonify(result=results)

#############
#
# Functions available to the page code above
#
##############

def new_memo(date, text):
    """
    Inputs: date - simple date, text - string of text
    Output: record that was created in the mongodb
    """
    try:
        record = { "type": "dated_memo",
                   "date": arrow.get(date).naive,
                   "text": text
                  }
        collection.insert_one(record)
    except:
        print("Unexpected error in new_memo:", sys.exc_info()[0])
        raise

    return record

def remove_memos(idlist):
    """
    Input: idlist - list of objectIds in the form of a string
    Output: a list of the return values from removing mongodb reccords
    """
    try:
        results = []
        for obj in idlist:
            res = collection.delete_one( { "_id": ObjectId(obj) })
            results.append(res)
    except:
        print("Unexpected error in remove_memos:", sys.exc_info()[0])
        raise
    return results

def get_memos():
    """
    Returns all memos in the database, in a form that
    can be inserted directly in the 'session' object.
    """
    try:
        records = [ ]
        for record in collection.find( { "type": "dated_memo" } ):
            record['date'] = arrow.get(record['date']).isoformat()
            record['_id'] = str(record['_id'])
            records.append(record)
    except:
        print("Unexpected error in get_memos:", sys.exc_info()[0])
        raise

    return sorted(records, key=lambda k: k['date'])


if __name__ == "__main__":
    # App is created above so that it will
    # exist whether this is 'main' or not
    # (e.g., if we are running in a CGI script)
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    # We run on localhost only if debugging,
    # otherwise accessible to world
    if CONFIG.DEBUG:
        # Reachable only from the same computer
        app.run(port=CONFIG.PORT)
    else:
        # Reachable from anywhere
        app.run(port=CONFIG.PORT,host="0.0.0.0")
