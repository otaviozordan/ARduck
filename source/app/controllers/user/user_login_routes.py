from flask import render_template, request, redirect, url_for, Response
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.models.user_table import Usuario
import json

@app.route('/login', methods=['POST'])
def login_acao():
    body = request.get_json()
    email = body['email']
    pwd = body['password']
    response = {}

    user = Usuario.query.filter_by(email=email).first()
    if not user or user.verify_password(pwd):
        response['login'] = False
        response["Mensagem"] = "Usuario ou senha incorreta"
        return Response(json.dumps(response), status=200, mimetype="application/json")
    else:
        response["login"] = True
        return Response(json.dumps(response), status=200, mimetype="application/json")
    
@app.route('/logout')
def logout():
    logout_user()