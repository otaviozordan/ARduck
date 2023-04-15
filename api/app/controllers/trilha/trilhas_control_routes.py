from app import app, db, mongoDB
from flask import Response, request
from app.models.user_table import Usuario
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
            "nome": trilha_nome,
            "colecao": trilha_colecao,
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
            elif ('habilitado_padrao' in body):
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


