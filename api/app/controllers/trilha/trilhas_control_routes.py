from app import app, db, mongoDB
from flask import Response, request
from app.models.user_table import Usuario
import json

@app.route("/criartrilha", methods=["POST"])
def criartrilha():
    body = request.get_json()
    response = {}

    try:
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
            "imagem_path": imagem_path,
            "descricao": descricao,
            "teoria": teoria,
            "AR": {
                "Enable": AR,
                "id":AR_id
            },
            "Quiz": {
                "Enable": Quiz,
                "id":Quiz_id
            }
        }

        if ('Usuarios_habilitados' in body and body['Usuarios_habilitados']=="All"):
            try:
                users = Usuario.query.all()
                for user in users:
                    query = {"email": user.email}
                    update = {'$set': {trilha_nome: "Enable"}}
                    mongoDB.Permissoes.update_one(query, update, upsert=True);
            except Exception as e:
                print('Erro:', e, " ao cadastrar permissoes.")
                response['create'] = False
                response['erro'] = str(e)    
                return Response(json.dumps(response), status=200, mimetype="application/json")
        
        elif ('Usuarios_habilitados' in body):
            try:
                users = body["Usuarios_habilitados"]
                for user in users:
                    query = {"email": user}
                    update = {'$set': {trilha_nome: "Enable"}}
                    mongoDB.Permissoes.update_one(query, update, upsert=True);
            except Exception as e:
                print('Erro:', e, " ao cadastrar permissoes.")
                response['create'] = False
                response['erro'] = str(e)    
                return Response(json.dumps(response), status=200, mimetype="application/json")
            
        try:
            x = mongoDB.Trilhas.insert_one(trilha)

            print("Trilha Cadastrada.")
            response['create'] = x.acknowledged
            response["id"] = str(x.inserted_id)
            return Response(json.dumps(response), status=200, mimetype="application/json")
    
        except Exception as e:
            print('Erro', e, " ao cadastrar trilha.")
            response['create'] = False
            response['erro'] = str(e)
            
            return Response(json.dumps(response), status=200, mimetype="application/json")

    except Exception as e:
        response = {'Retorno': "Parametros invalidos ou ausentes", 'erro': str(e)}
    
        return Response(json.dumps(response), status=400, mimetype="application/json")