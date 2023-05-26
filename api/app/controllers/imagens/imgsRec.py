from app.models.user_table import authenticate
from flask import request, Response
from flask_login import current_user
from app import app
import json
import os

@app.route('/validacao_medidas', methods=['GET', 'POST'])
def upload_file():
    auth = authenticate("log")
    if auth:
        return Response(json.dumps(auth), status=200, mimetype="application/json")

    if request.method == 'POST':
        if 'image' not in request.files:
            return 'Nenhuma imagem selecionada', 400
    
        image = request.files['image']
    
        if image.filename == '':
            return 'Nenhum arquivo selecionado', 400

        try:
            # Define o diretório onde a imagem será salva
            save_dir = 'api\\app\models\\imgs\\validacao_multimetro'
            nome_usuario = current_user.nome        
            user_dir = os.path.join(save_dir, nome_usuario)
            if not os.path.exists(user_dir):
                os.makedirs(user_dir)

            lista_arquivos = os.listdir(user_dir)
            numero = 1
            for i in range(len(lista_arquivos)):
                numero = numero+1

            filerequestname = image.filename
            file_name,file_extension = os.path.splitext(filerequestname)

            nome = str(numero) + file_extension
            path_dir = os.path.join(user_dir, nome)

            image.save(path_dir)

            return 'Upload de imagem realizado com sucesso!'
        
        except Exception as e:
            print('Erro ', e)
            return str(e)

    return '''
    <!doctype html>
    <html>
        <head>
          <title>Upload de Imagem</title>
        </head>
        <body>
          <h1>Upload de Imagem</h1>
          <form method="POST" action="http://localhost:8080/validacao_medidas" enctype="multipart/form-data">
            <input type="file" name="image" accept="image/*">
            <input type="submit" value="Enviar">
          </form>
        </body>
    </html>
    '''


@app.route('/perfil', methods=['GET', 'POST'])
def upload_perfil():
    auth = authenticate("log")
    if auth:
        return Response(json.dumps(auth), status=200, mimetype="application/json")

    if request.method == 'POST':
        if 'image' not in request.files:
            return 'Nenhuma imagem selecionada', 400
    
        image = request.files['image']
    
        if image.filename == '':
            return 'Nenhum arquivo selecionado', 400

        try:
            # Define o diretório onde a imagem será salva
            save_dir = 'api\\app\models\\imgs\\foto_de_perfil'
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            nome_usuario = current_user.email        
            path_usuario = os.path.join(save_dir, nome_usuario)

            filerequestname = image.filename
            file_name,file_extension = os.path.splitext(filerequestname)

            save = path_usuario+ file_extension

            image.save(save)

            return 'Upload de imagem realizado com sucesso!'
        
        except Exception as e:
            print('Erro ', e)
            return str(e)

    return '''
    <!doctype html>
    <html>
        <head>
          <title>Upload de Imagem</title>
        </head>
        <body>
          <h1>Upload de Imagem</h1>
          <form method="POST" action="http://localhost:8080/perfil" enctype="multipart/form-data">
            <input type="file" name="image" accept="image/*">
            <input type="submit" value="Enviar">
          </form>
        </body>
    </html>
    '''