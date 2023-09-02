from app import app, db, mongoDB, DATABASE_IMG_PATH
from flask import Response, request, render_template
from flask_login import current_user
from app.models.user_table import Usuario, authenticate
from app.models.questoes_table import Questoes
import json
from app.controllers import cor_vermelha, reset_prompt

@app.route("/criartrilha", methods=['GET'])
def render_cadastrar_trilha():
    
    return render_template('formulario_nova_trilha.html')

@app.route("/criartrilha", methods=["POST"])
def criartrilha():
    auth = authenticate("professor")
    if auth:
        return Response(json.dumps(auth), status=200, mimetype="application/json")
    
    body = request.get_json()
    response = {}

    try:
        if 'turma' in body:
            turma = body['turma']
        else: 
            turma = "default"
    
        trilha_colecao = body['colecao']
        trilha_order = body['order']
        trilha_nome = body['trilha_nome']
        descricao = body['descricao']

        if 'imagem_path' in body:
            imagem_path = body["imagem_path"]
        else: 
            imagem_path = DATABASE_IMG_PATH + turma + "\\" + trilha_nome + "\\icone.png"
        
        if 'teoria' in body:
            teoria = body["teoria"]
            img_teoria = body["img_teoria"]
        else: 
            teoria = "Disabled"
            img_teoria = "Disabled"

        if 'AR' in body:
            AR = body["AR"]
        else: 
            AR = False

        if 'validacao_pratica' in body:
            validacao_pratica_en = True
            validacao_pratica = body["validacao_pratica"]
        else: 
            validacao_pratica_en = False
            validacao_pratica = "Disabled"

        if 'Quiz' in body:
            Quiz = True
            Quiz_dic = body["Quiz_dic"]
        else: 
            Quiz = False
            Quiz_dic = "Disabled"

    except Exception as e:
        response = {'create':False,'Retorno': "Parametros invalidos ou ausentes", 'erro': str(e)}
        return Response(json.dumps(response), status=400, mimetype="application/json")
    
    trilha = {
        "trilha_nome":trilha_nome,
        "colecao": trilha_colecao,
        "order": trilha_order,
        "imagem_path": imagem_path,
        "descricao": descricao,
        "options":{
            "teoria": teoria,
            "img_teoria":img_teoria,
            "AR": AR,
            "Quiz": {
                "Enable": Quiz,
                "questions":Quiz_dic
            },
            "validacao_pratica":{
                "Enable": validacao_pratica_en,
                "type":validacao_pratica
            }
        },
        "habilitado_padrao": False
    }
            
    try:    
        if ('habilitado_padrao' in body and body['habilitado_padrao']==True):
            trilha["habilitado_padrao"]=True
            users = Usuario.query.all()
            for user in users: #Cadastra permissão no body do usuario
                query = {"email": user.email}
                update = {'$set': {trilha_nome: True}}
                x = mongoDB.Permissoes.update_one(query, update);
                print("[INFO] Permissão definida: ", x.acknowledged," / Para o usuário '", user.nome,"'")

        elif ('habilitado_padrao' in body and body['habilitado_padrao']!=False):
            users = body["habilitado_padrao"]
            for user in users:
                query = {"email": user}
                update = {'$set': {trilha_nome: False}}
                x = mongoDB.Permissoes.update_one(query, update, upsert=True);
                print("[INFO] Permissão definida (False): ", x.acknowledged," / Para o usuário '", user.nome,"'")
    
    except Exception as e:
        response['create'] = False
        response['erro'] = str(e)   
        response['Retorno'] = 'Erro ao definir permisssões'                
        print("[ERRO] Erro ao definir permisssões / ", e)

        return Response(json.dumps(response), status=200, mimetype="application/json")

    try:
        query = {"turma":turma, "autor":current_user.nome}
        update = {'$set': {trilha_nome:trilha}}
        x = mongoDB.Trilhas.update_one(query, update, upsert=True); #Cadastra permissão no body da trilhas
        
        if x.modified_count:
            print("[INFO] Trilha Cadastrada: ", x.acknowledged)
            response["create"] = x.acknowledged
        else:
            print("[INFO] Trilha Atualizada: ", x.acknowledged)
            response['create'] = 'Trilha atualizada'

    except Exception as e:
        response['erro'] = str(e)
        response['create'] = False
        response['Retorno'] = 'Erro ao criar trilha'
        print("[ERRO] Erro ao criar trilha / ", e)

        return Response(json.dumps(response), status=200, mimetype="application/json")
    
    try:
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
        
                if trilha["options"]["AR"]:
                    key = "Elementos." + str(trilha_nome) + ".AR.progresso"
                    update = {'$set': {key:""}}
                    x = mongoDB.Progresso.update_one(query, update, upsert=True);
    
                if trilha["options"]["validacao_pratica"]["Enable"] != "Disable":
                    key = "Elementos." + str(trilha_nome) + ".validacao_pratica.progresso"
                    update = {'$set': {key:""}}
                    x = mongoDB.Progresso.update_one(query, update, upsert=True);
        return Response(json.dumps(response), status=200, mimetype="application/json")
    
    except Exception as e:
        response['create'] = False
        response['erro'] = str(e)
        response['Retorno'] = 'Erro ao sincronizar usuários a trilha'
        print("[ERRO] Erro ao sincronizar usuários a trilha / ", e)

        return Response(json.dumps(response), status=200, mimetype="application/json")

@app.route("/getEnableTrilhasByColecao/<string:colecao>", methods=["GET"])
def carregartrilhas_colecao(colecao):
    response = {}
    try:
        auth = authenticate("log")
        if auth:
            return Response(json.dumps(auth), status=401, mimetype="application/json")
        
        enable_lists = []
        turma = current_user.turma
        email = current_user.email

        query = mongoDB.Trilhas.find({"turma":turma})
        permissoes = mongoDB.Permissoes.find({"email": email},{})

    except Exception as e:
        response['find'] = False
        response['erro'] = str(e)
        response['Retorno'] = 'Erro ao carregar trilhas'
        print("[ERRO] Erro ao carregar trilhas / ", e)

        return Response(json.dumps(response), status=500, mimetype="application/json")

    try:
        for permissao in permissoes:
            permissao.pop('_id')
            permissao.pop('usuario')
            permissao.pop('email')
            for key in permissao.keys():
                enable_lists.append(key) #Carrega as trilhas já habilitadas 

        if len(enable_lists) == 0:
            print("[INFO] Coleção solicitada inesistente / Usuário solicitante: '", current_user.nome,"'")
            response['find'] = False
            response['Retorno'] = 'Coleção solicitada inexistente'
            return Response(json.dumps(response), status=400, mimetype="application/json")

        response["Trilhas encontradas"] = []
        print("[INFO] Buscado trilhas disponiveis para o usuário '", current_user.nome,"'")

        for q in query:
            if "autor" in q:
                q.pop('autor')
            q.pop('turma')
            q.pop('_id')

            for j in q:
                resultado = {j:{'enable':False}}
                if j in enable_lists:
                    resultado[j]["enable"] = True
                response["Trilhas encontradas"].append(resultado)

        return Response(json.dumps(response), status=200, mimetype="application/json")
    
    except Exception as e:
        response['find'] = False
        response['erro'] = str(e)
        response['Retorno'] = 'Erro ao filtrar trilhas'
        print("[ERRO] Erro ao filtrar trilhas / ", e)

        return Response(json.dumps(response), status=500, mimetype="application/json")
       
@app.route("/registrarprogresso", methods=["POST"])
def registrarprogresso():
    response ={}
    try:
        auth = authenticate("log")
        if auth:
            return Response(json.dumps(auth), status=200, mimetype="application/json")
       
        body = request.get_json()
        email = current_user.email
        turma = current_user.turma

        trilha = body["trilha"]
        elemento = body["elemento"]
        complemento = body["complemento"]
        status = body["status"]
       
    except Exception as e:
        response['create'] = False
        response['erro'] = str(e)
        response['Retorno'] = 'Valores invalidos ou ausentes'
        print("[ERRO] Erro ao cadastrar progresso/ Valores invalidos ou ausentes: ", e)
        return Response(json.dumps(response), status=400, mimetype="application/json")   

    try:   
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

        if len(completos) == len(progresso["Elementos"]):
            query = {"email": email}
            key = "Concluido."+str(trilha)
            update = {'$set': {key:True}}
            x = mongoDB.Progresso.update_one(query, update, upsert=True);
   
        response = {
            "status_da_query":x.acknowledged,
            "numero_de_modificacao":x.modified_count
        }
        return Response(json.dumps(response), status=200, mimetype="application/json")
    
    except Exception as e:
        response['create'] = False
        response['erro'] = str(e)
        response['Retorno'] = 'Erro ao cadastrar progresso'
        print("[ERRO] Erro ao cadastrar progresso: ", e)
        return Response(json.dumps(response), status=400, mimetype="application/json")   

def monitorar_progresso():
    auth = authenticate("log")
    if auth:
        return Response(json.dumps(auth), status=200, mimetype="application/json")
    
    email = current_user.email
    turma = current_user.turma

@app.route("/carregartrilha/<trilha_query>", methods=["GET"])
def carregartrilha(trilha_query):
    response ={}
    try:
        auth = authenticate("log")
        if auth:
            return Response(json.dumps(auth), status=200, mimetype="application/json")
       
        email = current_user.email
        turma = current_user.turma

        filtro = {}

        # Buscar a trilha correspondente à turma do aluno
        query = {
            "turma": turma,
            trilha_query: {"$exists": True}
        }
        trilha_load = mongoDB.Trilhas.find_one(query, {trilha_query: 1})

        if trilha_load and trilha_load[trilha_query]:
            del trilha_load[trilha_query]["habilitado_padrao"]
            del trilha_load[trilha_query]["colecao"]
            del trilha_load[trilha_query]["order"]

            response["get"]=True
            response["trilha"]=trilha_load[trilha_query]
        else:
            response["get"]=False
            response["trilha"]="Trilha não encontrada para a turma do aluno"
        return Response(json.dumps(response), status=200, mimetype="application/json")
       
    except Exception as e:
        response['get'] = False
        response['erro'] = str(e)
        response['Retorno'] = "Erro ao buscar trilha"
        print("[ERRO] Erro ", e, " ao buscar trilha", trilha_query, "/ vindo de: ", email)
        return Response(json.dumps(response), status=400, mimetype="application/json")