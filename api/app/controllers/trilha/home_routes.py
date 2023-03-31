from flask import render_template, request, redirect, url_for, Response
from flask_login import current_user
from app import app, db, colectionTrilhas
import json

@app.route('/home', methods=['GET'])
def carregarhome():
    response = {}
    usuario = current_user
    response["Usuario"] = usuario.to_json()
    return Response(json.dumps(response), status=200, mimetype="application/json")