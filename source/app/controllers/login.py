from flask import render_template, request, redirect, url_for, Response
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.models.login_table import Usuario
import json

@app.route('/registrar', methods=['GET'])
def registrar_pagina():
    return render_template('registrar.html')

@app.route('/registrar', methods=['POST'])
def registrar_acao():
    body = request.get_json()

    pwd = body['password']
    nome = body['nome']
    email = body['email']
    response = {}

    try:
        if nome and email and pwd:
            usuario = Usuario(password=pwd, nome=nome, email=email, turma=None)
            db.session.add(usuario)
            db.session.commit()
            print("Usuário Cadastrado.")
            response['success'] = True
            return Response(json.dumps(response), status=200, mimetype="application/json")
        if not nome:
            response['Mensagem'] = 'Nome nulo.'
        if not email:
            response['Mensagem'] = response['Mensagem'] + 'Email nulo.'
        if not pwd:
            response['Mensagem'] = response['Mensagem'] + 'Password nulo.'
        return Response(json.dumps(response), status=200, mimetype="application/json")
    
    except Exception as e:
        print('Erro', e, " ao cadastrar usuário.")
        response['success'] = False
        response['erro'] = str(e)
        return Response(json.dumps(response), status=400, mimetype="application/json")

@app.route('/login', methods=['GET'])
def login_pagina():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_acao():
    body = request.get_json()
    email = body['email']
    pwd = body['password']
    response = {}

    user = Usuario.query.filter_by(email=email).first()
    if not user or user.verify_password(pwd):
        response["Mensagem"] = "Usuario ou senha incorreta"
        return Response(json.dumps(response), status=200, mimetype="application/json")




@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login.html'))
