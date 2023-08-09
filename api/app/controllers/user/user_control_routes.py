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
                turma = "defult"
            if ('privilegio' in body):
                privilegio = body['privilegio']
            else: 
                privilegio = "usuario"

    except Exception as e:
        response['create'] = False
        response['erro'] = str(e)
        response['Retorno'] = 'Parametros invalidos ou ausentes'
        print("[ATENCAO] Parametros invalidos ou ausentes / ", e)

        return Response(json.dumps(response), status=400, mimetype="application/json")

    try:
        if nome and email and pwd:
            usuario = Usuario(password=pwd, nome=nome, email=email, turma=turma, privilegio=privilegio)
            usuario.get_id
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

        #Busca nome das trilhas criadas já
        trilhas_existentes =  mongoDB.Trilhas.find({"turma": turma})
        for trilhas_exixtentes_dic in trilhas_existentes:
            trilha_nomes = [chave for chave in trilhas_exixtentes_dic.keys() if chave not in ("_id", "autor", "turma")]
        print("[INFO] Trilhas do usuario: ", trilha_nomes)

        #Envia em progresso false para todas as trilhas com misão 
        trilhaAndElementos = {}
        for trilha_nome in trilha_nomes:
            trilhaAndElementos[trilha_nome] = {}
            trilhaAndElementos[trilha_nome]["quiz"] = {}
            nunQuestao = 1
            questoes = Questoes.query.filter_by(colecao=trilha_nome)
            for questao in questoes:
                trilhaAndElementos[trilha_nome]["quiz"][str(nunQuestao)] = False
                nunQuestao = nunQuestao+1
        progressoDefult = {
            "usuario":nome, "email":email,
            "Elementos":trilhaAndElementos
        }
        x = mongoDB.Progresso.insert_one(progressoDefult)
        print("[INFO] Sincronizado Quiz de usuário: ", nome)

        # Fazer a query para encontrar os documentos com "habilitado padrão" igual a true
        filtro = {
        "trilha": {
            "$elemMatch": {
                "habilitado_padrao": True
                }
            }
        }
        trilhas_habilitadas = mongoDB.Trilha.find(filtro)
        print(vars(trilhas_habilitadas))
        for n in trilhas_habilitadas: 
            print(n)
        for trilha_habilitada in trilhas_habilitadas:
            print(trilha_habilitada)
            query = {"email": email}
            update = {'$set': {trilha_habilitada["_id"]: "Enable"}}  # Use o campo "_id" da trilha
            mongoDB.Permissoes.update_one(query, update, upsert=True)


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

        
        Response(json.dumps(response), status=200, mimetype="application/json")
        
    except Exception as e:
        response['create'] = False
        response['erro'] = str(e)
        response['Retorno'] = 'Erro ao sicronizar usuário'
        print("[ERRO] Erro ao sicronizar usuário / ", e)
        excluir_usuario(email);
        return Response(json.dumps(response), status=200, mimetype="application/json")
    
def excluir_usuario(email):
    response = {}
    try:
        # Excluir usuário
        user_to_delete = Usuario.query.filter_by(email=email).first()  # Adicione .first() para obter a primeira correspondência
        if user_to_delete:
            print("[INFO] Excluindo conta de: '", email,"'")
            db.session.delete(user_to_delete)
            db.session.commit()
            filtro = {"email": {"$regex": email}}
            result = mongoDB.Permissoes.delete_many(filtro)
            print("[INFO] Excluindo permissões: ", result.deleted_count)
            result = mongoDB.Progresso.delete_many(filtro)
            print("[INFO] Excluindo progresso: ", result.deleted_count)

    except Exception as e:
        print("[ERRO] Erro crash de exclusão / ", e)