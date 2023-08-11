from flask import request, Response
from app import db, app, mongoDB
from app.models.user_table import Usuario, authenticate
from app.models.questoes_table import Questoes
from flask_login import current_user, login_user
from app.controllers import cor_vermelha, reset_prompt,cor_azul

import json

@app.route('/signup', methods=['POST'])
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
            print(cor_azul,"[INFO]",reset_prompt,"Usuário cadastrado")

    except Exception as e:
        response['create'] = False
        response['erro'] = str(e)
        response['Retorno'] = 'Erro ao cadastrar usuário'
        print(cor_vermelha,"[ERRO]",reset_prompt,"Erro ao cadastrar usuário / ", e)
        return Response(json.dumps(response), status=200, mimetype="application/json")

    try:
        userPermissao = {"usuario":nome, "email":email}
        x = mongoDB.Permissoes.insert_one(userPermissao)

        #Busca nome das trilhas criadas já
        trilhas_existentes =  mongoDB.Trilhas.find({"turma": turma})
        for trilhas_existentes_dic in trilhas_existentes:
            trilha_nomes = [chave for chave in trilhas_existentes_dic.keys() if chave not in ("_id", "autor", "turma")]
        print(cor_azul,"[INFO]",reset_prompt,"Trilhas do usuario: ", trilha_nomes)

        #Envia em progresso false para todas os quis com misão 
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
        print(cor_azul,"[INFO]",reset_prompt,"Sincronizado Quiz de usuário: ", email)

        # Fazer a query para encontrar os documentos com "habilitado padrão" igual a true
        filtro = {
            "$or": [
            ]
        }
        for n in trilha_nomes:
            key = n+".habilitado_padrao"
            filtro["$or"].append({key:True})
        documentos_selecionados = mongoDB.Trilhas.find(filtro)

        for docs in documentos_selecionados:
            docs_key_selec = [chave for chave in docs.keys() if chave not in ("_id", "autor", "turma")]

        for key_selec in docs_key_selec:
            print(cor_azul,"[INFO]",reset_prompt,"Sincronizando '", key_selec, "'  na lista de permissões para:", email)
            query = {"email": email}
            update = {'$set': {key_selec: "Enable"}}  # Use o campo "_id" da trilha
            mongoDB.Permissoes.update_one(query, update, upsert=True)

        query = {"email":email}
        trilhas_existentes =  mongoDB.Trilhas.find({"turma": turma})
        for tl_ex in trilhas_existentes:
            for k in trilha_nomes:
                print(cor_azul,"[INFO]",reset_prompt,"Sincronizando '", k, "'  na lista de progresso para:", email)
                if tl_ex[k]["options"]["AR"]["Enable"]:
                    key = "Elementos." + str(trilha_nome) + ".AR.progresso"
                    update = {'$set': {key:""}}
                    x = mongoDB.Progresso.update_one(query, update, upsert=True);

                    if tl_ex[k]["options"]["validacao_pratica"]["Enable"] != "Disable":
                        key = "Elementos." + str(trilha_nome) + ".validacao_pratica.progresso"
                        update = {'$set': {key:""}}
                        x = mongoDB.Progresso.update_one(query, update, upsert=True);

        response["create"]=True
        user = Usuario.query.filter_by(email=email).first()
        login_user(user)
        return Response(json.dumps(response), status=200, mimetype="application/json")
        
    except Exception as e:
        response['create'] = False
        response['erro'] = str(e)
        response['Retorno'] = 'Erro ao sicronizar usuário'
        print(cor_vermelha,"[ERRO]",reset_prompt,"Erro ao sicronizar usuário / ", e)
        excluir_usuario(email);
        return Response(json.dumps(response), status=200, mimetype="application/json")
    
def excluir_usuario(email):
    response = {}
    try:
        # Excluir usuário
        user_to_delete = Usuario.query.filter_by(email=email).first()  # Adicione .first() para obter a primeira correspondência
        if user_to_delete:
            print(cor_azul,"[INFO]",reset_prompt,"Excluindo conta de: '", email,"'")
            db.session.delete(user_to_delete)
            db.session.commit()
            filtro = {"email": {"$regex": email}}
            result = mongoDB.Permissoes.delete_many(filtro)
            print(cor_azul,"[INFO]",reset_prompt,"Excluindo permissões: ", result.deleted_count)
            result = mongoDB.Progresso.delete_many(filtro)
            print(cor_azul,"[INFO]",reset_prompt,"Excluindo progresso: ", result.deleted_count)

    except Exception as e:
        print(cor_vermelha,"[ERRO]",reset_prompt,"Erro crash de exclusão / ", e)