from flask import render_template, request, redirect, url_for, Response
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.models.user_table import Usuario
import json

@app.route('/login', methods=['POST', 'GET'])
def login_acao():
    try:
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
            try:
                login_user(user)
                response["usuario"] = current_user.to_json()
            except Exception as e:
                response = {'Retorno': "impossivel fazer login", 'erro': str(e)}
            return Response(json.dumps(response), status=200, mimetype="application/json")
        
    except Exception as e:
        response = {'Retorno': "Parametros invalidos ou ausentes", 'erro': str(e)}

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    response = {"usuario": False, "Mensagem:":"Usuário desconectado"}
    return Response(json.dumps(response), status=200, mimetype="application/json")

@app.route('/login_page', methods=['POST', 'GET'])
def paginadelogin():
    if request.method == 'POST':
        try:
            email = request.form['usuario']
            pwd = request.form['senha']
            response = {}

            user = Usuario.query.filter_by(email=email).first()
            if not user or user.verify_password(pwd):
                response['login'] = False
                response["Mensagem"] = "Usuario ou senha incorreta"
                return Response(json.dumps(response), status=200, mimetype="application/json")
            else:
                response["login"] = True
                try:
                    login_user(user)
                    response["usuario"] = current_user.to_json()
                except Exception as e:
                    response = {'Retorno': "impossivel fazer login", 'erro': str(e)}
                return Response(json.dumps(response), status=200, mimetype="application/json")

        except Exception as e:
            response = {'Retorno': "Parametros invalidos ou ausentes", 'erro': str(e)}


    return '''
    <!doctype html>
    <html>
        <head>
          <title>Login</title>
        </head>
        <body>
          <h1>Email/Senha</h1>
          <form method="POST" action="http://localhost:8080/login_page" enctype="multipart/form-data">
            <input type="text" name="usuario" accept="image/*">
            <input type="text" name="senha" accept="image/*">
            <input type="submit" value="Enviar">
          </form>
        </body>
    </html>
    '''
