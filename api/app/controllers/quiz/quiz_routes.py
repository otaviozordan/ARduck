from app import app, db, mongoDB
from app.models.questoes_table import Questoes, verificarRespostaCorreta
from app.models.user_table import Usuario
from flask import Response, request
import json

@app.route('/questao/<id>', methods=['GET'])
def carregar_questao(id):
    questao = Questoes.query.filter_by(id=id).first()
    response = {}
    response["colecao"] = questao.colecao
    response["titulo"] = questao.titulo
    response["texto"] = questao.texto
    response["imgPath"] = questao.imgPath
    response["respostaCorreta"] = questao.respostaCorreta
    response["alternativa1"] = questao.alternativa1
    response["alternativa2"] = questao.alternativa2
    response["alternativa3"] = questao.alternativa3
    response["alternativa4"] = questao.alternativa4
    return Response(json.dumps(response), status=200, mimetype="application/json")

@app.route("/listquestoes", methods=["GET"])
def listquestoes():
    questoes_objeto = Questoes.query.all()
    questoes_json = [questao.to_json() for questao in questoes_objeto]
    return Response(json.dumps(questoes_json), status=200, mimetype="application/json")

@app.route("/listquestoes/<colecao>", methods=["GET"])
def listquestoes_porcolecao(colecao):
    questoes_objeto = Questoes.query.filter_by(colecao=colecao).all()
    questoes_json = [questao.to_json() for questao in questoes_objeto]
    return Response(json.dumps(questoes_json), status=200, mimetype="application/json")

@app.route("/createquestao", methods=["POST"])
def createquestao():
    body = request.get_json()
    response = {}
    
    try:
        colecao = body["colecao"]
        titulo = body["titulo"]
        texto = body["texto"]
        imgPath = body["imgPath"]
        respostaCorreta = body["respostaCorreta"]
        alternativa1 = body["alternativa1"]    
        alternativa2 = body["alternativa2"]
        alternativa3 = body["alternativa3"]
        alternativa4 = body["alternativa4"]
    except Exception as e:
        print('Erro', e)
        response['create'] = False
        response['erro'] = str(e)
        return Response(json.dumps(response), status=400, mimetype="application/json")
    
    #try:
    questao = Questoes(colecao=colecao, titulo=titulo, texto=texto, imgPath=imgPath, respostaCorreta=respostaCorreta, alternativa1=alternativa1, alternativa2=alternativa2, alternativa3=alternativa3, alternativa4=alternativa4)
    db.session.add(questao)
    db.session.commit()
    users = Usuario.query.all()
    if mongoDB.Trilhas.count_documents({"nome": colecao}) > 0:
        for user in users:
                email = user.email
                nunQuestao = Questoes.query.filter_by(colecao=colecao).count()
                query = {"email": email}
                key = "Elementos."+str(colecao)+".quiz."+str(nunQuestao)
                update = {'$set': {key:False}}
                print("X")
                x = mongoDB.Progresso.update_one(query, update, upsert=True);
                print(x.matched_count)
    
    print("Quiz Cadastrado.")
    response['create'] = True
    return Response(json.dumps(response), status=200, mimetype="application/json")
    #except Exception as e:
        #print('Erro', e, " ao cadastrar Quiz.")
        #response['create'] = False
        #response['erro'] = str(e)
        #return Response(json.dumps(response), status=400, mimetype="application/json")
    
@app.route("/verificarquiz", methods=["POST"]) #Editar
def verificarquiz():
    body = request.get_json()
    response = {}
    
    try:
        colecao = body["colecao"]
        titulo = body["titulo"]
        texto = body["texto"]
        imgPath = body["imgPath"]
        respostaCorreta = body["respostaCorreta"]
        alternativa1 = body["alternativa1"]    
        alternativa2 = body["alternativa2"]
        alternativa3 = body["alternativa3"]
        alternativa4 = body["alternativa4"]
    except Exception as e:
        print('Erro', e)
        response['create'] = False
        response['erro'] = str(e)
        return Response(json.dumps(response), status=400, mimetype="application/json")
    
    try:
        questao = Questoes(colecao=colecao, titulo=titulo, texto=texto, imgPath=imgPath, respostaCorreta=respostaCorreta, alternativa1=alternativa1, alternativa2=alternativa2, alternativa3=alternativa3, alternativa4=alternativa4)
        db.session.add(questao)
        db.session.commit()
        print("Quiz Cadastrado.")
        response['create'] = True
        return Response(json.dumps(response), status=200, mimetype="application/json")
    except Exception as e:
        print('Erro', e, " ao cadastrar Quiz.")
        response['create'] = False
        response['erro'] = str(e)
        return Response(json.dumps(response), status=400, mimetype="application/json")