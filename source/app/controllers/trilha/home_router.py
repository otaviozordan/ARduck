from flask import render_template, request, redirect, url_for, Response
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.models.user_table import Usuario
import json

@app.route('/home', method='GET')
def carregar():
    response = {}
    response["nome"] = current_user().nome
    return Response(json.dumps(response), status=200, mimetype="application/json")