from flask import render_template, request, redirect, url_for, Response
from flask_login import current_user
from app import app, db
import json

@app.route('/home/<privilegio>', methods=['GET'])
def carregarhome(privilegio):
    response = {}
    usuario = current_user.is_authenticated
    if usuario: 
        usuario = current_user
        if (usuario.privilegio == privilegio):
            return
        else:
            response['Acesso'] = "negado"
            response['Necessario'] = privilegio
    else:
        response['Acesso'] = "negado"
        response['Necessario'] = "Estar logado"      
    return Response(json.dumps(response), status=200, mimetype="application/json")