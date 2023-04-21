from flask import request, Response
from app import db, app, mongoDB
from app.models.user_table import Usuario, authenticate
from flask_login import current_user
import json

@app.route('/registrar', methods=['POST'])
def registrar_acao():   
    body = request.get_json()
    try:
        pwd = body['password']
        nome = body['nome']
        email = body['email']

        if ('turma' in body):
            turma = body['turma']
        else :
            turma = None

        if ('privilegio' in body):
            privilegio = body['privilegio']
        else: 
            privilegio = None

        response = {}
        try:
            if nome and email and pwd:
                usuario = Usuario(password=pwd, nome=nome, email=email, turma=turma, privilegio=privilegio)
                db.session.add(usuario)
                db.session.commit()

                userPermissao = {"usuario":nome, "email":email}
                x = mongoDB.Permissoes.insert_one(userPermissao)
                x = mongoDB.Progresso.insert_one(userPermissao)
                print("Usuário Cadastrado.")
                response['create'] = True
                response['id_user_permissao'] = str(x.inserted_id)
    
        except Exception as e:
            print('Erro', e, " ao cadastrar usuário.")
            response['create'] = False
            response['erro'] = str(e)
            return Response(json.dumps(response), status=200, mimetype="application/json")
        
        trilhas_habilitadas =  mongoDB.Trilhas.find({"habilitado_padrao": True})
        for trilha_habilitada in trilhas_habilitadas:
                nome_da_trilhas = trilha_habilitada["nome"]
                query = {"email": email}
                update = {'$set': {nome_da_trilhas: "Enable"}}
                mongoDB.Permissoes.update_one(query, update, upsert=True);
        return Response(json.dumps(response), status=200, mimetype="application/json")

    except Exception as e:
        response = {'Retorno': "Parametros invalidos ou ausentes", 'erro': str(e)}
    
        return Response(json.dumps(response), status=400, mimetype="application/json")