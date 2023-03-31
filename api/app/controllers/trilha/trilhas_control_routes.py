from app import app, db, colectionTrilhas
from flask import Response
import json

@app.route("/criartrilha", methods=["POST"])
def criartrilha():
    mydict = { "name": "Peter", "address": "Lowstreet 27" }
    x = colectionTrilhas.insert_one(mydict)
    print(x.inserted_id)
    return Response(json.dumps({"teste":"cacas"}), status=200, mimetype="application/json")