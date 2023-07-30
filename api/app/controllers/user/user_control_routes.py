from flask import request, Response
from app import db, app, mongoDB
from app.models.user_table import Usuario, authenticate
from app.models.questoes_table import Questoes
from flask_login import current_user
import json

@app.route('/registrar', methods=['POST'])
def registrar_acao():   
    body = request.get_json()
    response = {}
    try:
        email = body['email']
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            response = {'Retorno': "Email já criado", "create":False}
            return Response(json.dumps(response), status=400, mimetype="application/json")
        else:
            pwd = body['password']
            nome = body['nome']
            if ('turma' in body):
                turma = body['turma']
            else:
                turma = None
            if ('privilegio' in body):
                privilegio = body['privilegio']
            else: 
                privilegio = None

    except Exception as e:
        response['create'] = False
        response['erro'] = str(e)
        response['Retorno'] = 'Parametros invalidos ou ausentes'
        print("[ATENCAO] Parametros invalidos ou ausentes / ", e)

        return Response(json.dumps(response), status=400, mimetype="application/json")

    try:
        if nome and email and pwd:
            usuario = Usuario(password=pwd, nome=nome, email=email, turma=turma, privilegio=privilegio)
            db.session.add(usuario)
            db.session.commit()
            print("[INFO] Usuário cadastrado")

    except Exception as e:
        response['create'] = False
        response['erro'] = str(e)
        response['Retorno'] = 'Erro ao cadastrar usuário'
        print("[ERRO] Erro ao cadastrar usuário / ", e)

        return Response(json.dumps(response), status=200, mimetype="application/json")

    try:
        userPermissao = {"usuario":nome, "email":email}
        x = mongoDB.Permissoes.insert_one(userPermissao)

        trilhas_existentes =  mongoDB.Trilhas.find()
        trilhaAndElementos = {}
        for trilha in trilhas_existentes:
            Trilha_nome = trilha["nome"]
            trilhaAndElementos[Trilha_nome] = {}
            trilhaAndElementos[Trilha_nome]["quiz"] = {}
            nunQuestao = 1
            questoes = Questoes.query.filter_by(colecao=Trilha_nome)
            for questao in questoes:
                trilhaAndElementos[Trilha_nome]["quiz"][str(nunQuestao)] = False
                nunQuestao = nunQuestao+1
        progressoDefult = {
            "usuario":nome, "email":email,
            "Elementos":trilhaAndElementos
        }
        x = mongoDB.Progresso.insert_one(progressoDefult)
        query = {"email":email}
        trilhas_existentes =  mongoDB.Trilhas.find()
        for trilha in trilhas_existentes:
            trilha_nome = trilha["nome"]
            if trilha["options"]["AR"]["Enable"]:
                key = "Elementos." + str(trilha_nome) + ".AR.progresso"
                update = {'$set': {key:""}}
                x = mongoDB.Progresso.update_one(query, update, upsert=True);

                if trilha["options"]["validacao_pratica"]["Enable"] != "Disable":
                    key = "Elementos." + str(trilha_nome) + ".validacao_pratica.progresso"
                    update = {'$set': {key:""}}
                    x = mongoDB.Progresso.update_one(query, update, upsert=True);

        trilhas_habilitadas =  mongoDB.Trilhas.find({"habilitado_padrao": True})
        for trilha_habilitada in trilhas_habilitadas:
                nome_da_trilhas = trilha_habilitada["nome"]
                query = {"email": email}
                update = {'$set': {nome_da_trilhas: "Enable"}}
                mongoDB.Permissoes.update_one(query, update, upsert=True);
        
        Response(json.dumps(response), status=200, mimetype="application/json")
        
    except Exception as e:
        response['create'] = False
        response['erro'] = str(e)
        response['Retorno'] = 'Erro ao cadastrar usuário'
        print("[ERRO] Erro ao definir usuário / ", e)

        return Response(json.dumps(response), status=200, mimetype="application/json")