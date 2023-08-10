from flask import render_template, request, redirect, url_for, Response
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.models.user_table import Usuario
import json
from app.controllers import cor_vermelha, reset_prompt,cor_azul


@app.route('/login', methods=['POST'])
def login_acao():
    body = request.get_json()
    response = {}

    try:
        email = body['email']
        pwd = body['password']
    except Exception as e:
        response['login'] = False
        response['erro'] = str(e)   
        response['Retorno'] = 'Parametros invalidos ou ausentes'                
        print("[ATENCAO] Parametros invalidos ou ausentes: ", e)
        return Response(json.dumps(response), status=200, mimetype="application/json")

    user = Usuario.query.filter_by(email=email).first()
    if not user or user.verify_password(pwd):
        response['login'] = False
        response["mensagem"] = "Usuario ou senha incorreta"
        print("[ATENÇAO] Login incorreto. Tentativa de acessar: ", email)
        return Response(json.dumps(response), status=200, mimetype="application/json")
    else:
        try:
            login_user(user)
            response["usuario"] = current_user.to_json()
            response["login"] = True
            print(cor_azul,"[INFO]",reset_prompt,"Usuário logado: ", current_user.email)
            return Response(json.dumps(response), status=200, mimetype="application/json")
        except Exception as e:
            response['login'] = False
            response['erro'] = str(e)   
            response['Retorno'] = 'Parametros invalidos ou ausentes'                
            print(cor_vermelha,"[ERRO]",reset_prompt,"Impossivel fazer login \ ", e)
            return Response(json.dumps(response), status=200, mimetype="application/json")

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    print(cor_azul,"[INFO]",reset_prompt,"Sessão encerrada de: ", current_user.nome)
    logout_user()
    response = {"usuario": False, "Mensagem:":"Usuário desconectado"}
    return Response(json.dumps(response), status=200, mimetype="application/json")

