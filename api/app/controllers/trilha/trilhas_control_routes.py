from app import app, db, mongoDB
from flask import Response, request
from flask_login import current_user
from app.models.user_table import Usuario, authenticate
import json

@app.route("/criartrilha", methods=["POST"])
def criartrilha():
    body = request.get_json()
    response = {}

    try:
        trilha_colecao = body['colecao']
        trilha_order = body['order']
        trilha_nome = body['trilha_nome']
        imagem_path = body['imagem_path']
        descricao = body['descricao']

        if('Teoria' in body):
            teoria = body["AR_id"]
        else: 
            teoria = "Disabled"

        if('AR' in body and body["AR"] == True):
            AR = True
            AR_id = body["AR_id"]
        else: 
            AR = False
            AR_id = "Disabled"

        if('Quiz' in body and body["Quiz"] == True):
            Quiz = True
            Quiz_id = body["Quiz_id"]
        else: 
            Quiz = False
            Quiz_id = "Disabled"

        trilha = {
            "colecao": trilha_colecao,
            "nome": trilha_nome,
            "order": trilha_order,
            "imagem_path": imagem_path,
            "descricao": descricao,
            "options":{
                "teoria": teoria,
                "AR": {
                    "Enable": AR,
                    "id":AR_id
                },
                "Quiz": {
                    "Enable": Quiz,
                    "id":Quiz_id
                }
            },
            "habilitado_padrao": False
        }

        try:
            x = mongoDB.Trilhas.insert_one(trilha)

            print("Trilha Cadastrada.")
            response['create'] = x.acknowledged
            response["id"] = str(x.inserted_id)
    
        except Exception as e:
            print('Erro', e, " ao cadastrar trilha.")
            response['create'] = False
            response['erro'] = str(e)
            
            return Response(json.dumps(response), status=200, mimetype="application/json")

        try:    
            if ('habilitado_padrao' in body and body['habilitado_padrao']==True):
                query = {'nome': trilha_nome}
                update = {'$set': {"habilitado_padrao": True}}
                x = mongoDB.Trilhas.update_one(query, update); #Cadastra permissão no body da trilhas
                print(x.matched_count)
                users = Usuario.query.all()
                for user in users: #Cadastra permissão no body do usuario
                    query = {"email": user.email}
                    update = {'$set': {trilha_nome: "Enable"}}
                    mongoDB.Permissoes.update_one(query, update);
            elif ('habilitado_padrao' in body and body['habilitado_padrao']!=False):
                users = body["habilitado_padrao"]
                for user in users:
                    query = {"email": user}
                    update = {'$set': {trilha_nome: "Enable"}}
                    mongoDB.Permissoes.update_one(query, update, upsert=True);
        except Exception as e:
            print('Erro:', e, " ao cadastrar permissoes.")
            response['create'] = False
            response['erro'] = str(e)    
            return Response(json.dumps(response), status=200, mimetype="application/json")
        
        return Response(json.dumps(response), status=200, mimetype="application/json")
    
    except Exception as e:
        response = {'Retorno': "Parametros invalidos ou ausentes", 'erro': str(e)}
    
        return Response(json.dumps(response), status=400, mimetype="application/json")

@app.route("/carregartrilhas/<string:colecao>", methods=["GET"])
def carregartrilhas(colecao):
    #try:
        auth = authenticate("log")
        if auth:
            return Response(json.dumps(auth), status=200, mimetype="application/json")
        
        enable_lists = []
        query = mongoDB.Trilhas.find({"colecao": colecao},{}).sort("order", 1)
        email = current_user.email
        permissoes = mongoDB.Permissoes.find({"email": email},{})
        for permissao in permissoes:
            permissao.pop('_id')
            permissao.pop('usuario')
            permissao.pop('email')
            for key in permissao.keys():
                enable_lists.append(key)

        response = {}
        response["Trilhas encontradas"] = []
        for j in query:
            j.pop('_id')
            j.pop('colecao')
            j.pop('habilitado_padrao')
            j.pop('order')
            j.pop('options')

            nome_da_trilha = j['nome']
            if nome_da_trilha in enable_lists:
                j["enable"] = True
            else:
                j["enable"] = False
            response["Trilhas encontradas"].append(j)

        return Response(json.dumps(response), status=200, mimetype="application/json")
    
    #except Exception as e:
        response = {'Erro:': str(e)}
        return Response(json.dumps(response), status=400, mimetype="application/json")