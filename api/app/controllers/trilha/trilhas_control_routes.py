from app import app, db, mongoDB
from flask import Response, request
from flask_login import current_user
from app.models.user_table import Usuario, authenticate
from app.models.questoes_table import Questoes
import json

@app.route("/criartrilha", methods=["POST"])
def criartrilha():
    body = request.get_json()
    response = {}

    try:
        trilha_colecao = body['colecao']
        trilha_order = body['order']
        trilha_nome = body['trilha_nome']
        descricao = body['descricao']

        if 'imagem_path' in body:
            imagem_path = body["imagem_path"]
        else: 
            imagem_path = "api\\app\\models\\imgs\\trilhas\\" + trilha_nome + "\\icone.png"

        if 'teoria' in body:
            teoria = body["teoria"]
            img_teoria = body["img_teoria"]
        else: 
            teoria = "Disabled"
            img_teoria = "Disabled"

        if 'AR' in body and body["AR"] == True:
            AR = True
            AR_id = body["AR_id"]
        else: 
            AR = False
            AR_id = "Disabled"

        if 'validacao_pratica' in body:
            validacao_pratica_en = True
            validacao_pratica = body["validacao_pratica"]
        else: 
            validacao_pratica_en = False
            validacao_pratica = "Disabled"

        if 'Quiz' in body and body["Quiz"] == True:
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
                "img_teoria":img_teoria,
                "AR": {
                    "Enable": AR,
                    "id":AR_id
                },
                "Quiz": {
                    "Enable": Quiz,
                    "id":Quiz_id
                },
                "validacao_pratica":{
                    "Enable": validacao_pratica_en,
                    "type":validacao_pratica
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
        
        trilhaAndElementos = {}
        trilhaAndElementos[trilha_nome] = {}
        trilhaAndElementos[trilha_nome]["quiz"] = {}
        nunQuestao = 1
        questoes = Questoes.query.filter_by(colecao=trilha_nome)
        users = Usuario.query.all()
        for user in users: #Cadastra permissão no body do usuario
                nome = user.nome
                email = user.email
                for questao in questoes:
                    trilhaAndElementos[trilha_nome]["quiz"][str(nunQuestao)] = False
                    nunQuestao = nunQuestao+1
                query = {"email": email}
                quiz = trilhaAndElementos[trilha_nome]
                key = "Elementos."+str(trilha_nome)
                update = {'$set': {key:quiz}}
                x = mongoDB.Progresso.update_one(query, update, upsert=True);
        
                if trilha["options"]["AR"]["Enable"]:
                    key = "Elementos." + str(trilha_nome) + ".AR.progresso"
                    update = {'$set': {key:""}}
                    x = mongoDB.Progresso.update_one(query, update, upsert=True);
        
                if trilha["options"]["validacao_pratica"]["Enable"] is not "Disable":
                    key = "Elementos." + str(trilha_nome) + ".validacao_pratica.progresso"
                    update = {'$set': {key:""}}
                    x = mongoDB.Progresso.update_one(query, update, upsert=True);
   
        return Response(json.dumps(response), status=200, mimetype="application/json")
    
    except Exception as e:
        response = {'Retorno': "Parametros invalidos ou ausentes", 'erro': str(e)}
        return Response(json.dumps(response), status=400, mimetype="application/json")

@app.route("/carregartrilhas/<string:colecao>", methods=["GET"])
def carregartrilhas(colecao):
    try:
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
    
    except Exception as e:
        response = {'Erro:': str(e)}
        return Response(json.dumps(response), status=400, mimetype="application/json")
    
@app.route("/registrarprogresso", methods=["POST"])
def registrarprogresso():
    try:
        auth = authenticate("log")
        if auth:
            return Response(json.dumps(auth), status=200, mimetype="application/json")
        
        body = request.get_json()
        email = current_user.email

        try:
            trilha = body["trilha"]
            elemento = body["elemento"]
            complemento = body["complemento"]
            status = body["status"]

            query = {"email": email}
            key = "Elementos."+trilha+"."+elemento+"."+complemento

            filtro = {key: {"$exists": True}}
            resultado = mongoDB.Progresso.find_one(filtro)
            if resultado is None:
                response = {"Erro:":"Nenhum elemento correspondente"}
                return Response(json.dumps(response), status=400, mimetype="application/json")

            update = {'$set': {key:status}}
            x = mongoDB.Progresso.update_one(query, update, upsert=True);

            progresso = mongoDB.Progresso.find_one({"email":email})
            trilha_em_progresso = progresso["Elementos"][trilha]

            completos = []
            for item in trilha_em_progresso:
                for elemento in item:
                    if elemento is not True:
                        break;
                completos.append(item)
            print(completos)
            if len(completos) == len(progresso["Elementos"]):
                query = {"email": email}
                key = "Concluido."+str(trilha)
                update = {'$set': {key:True}}
                print("X")
                x = mongoDB.Progresso.update_one(query, update, upsert=True);
    

            response = {
                "status_da_query":x.acknowledged,
                "numero_de_modificacao":x.modified_count
            }
        
        except Exception as e:
            response = {'Retorno': "Parametros invalidos ou ausentes", 'erro': str(e)}
            return Response(json.dumps(response), status=400, mimetype="application/json")

        return Response(json.dumps(response), status=200, mimetype="application/json")
    
    except Exception as e:
        response = {'Erro:': str(e)}
        return Response(json.dumps(response), status=400, mimetype="application/json")