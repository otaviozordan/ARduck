from app.models.user_table import authenticate
from flask import request, Response
from flask_login import current_user
from app import app, DATABASE_IMG_PATH
import json
import os

@app.route('/validar_multimetro_upimg', methods=['GET', 'POST'])
def validar_multimetro_upimg():
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
            save_dir = DATABASE_IMG_PATH + 'validacao_multimetro'
            nome_usuario = current_user.email        
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


@app.route('/perfil_upimg', methods=['GET', 'POST'])
def perfil_upimg():
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
            save_dir = DATABASE_IMG_PATH + 'foto_de_perfil'
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            nome_usuario = current_user.email        
            path_usuario = os.path.join(save_dir, nome_usuario)

            filerequestname = image.filename
            file_name,file_extension = os.path.splitext(filerequestname)

            save = path_usuario+file_extension

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

@app.route('/criartrilha_upimg', methods=['GET', 'POST'])
def criartrilha_upimg():
    auth = authenticate("log")
    if auth:
        return Response(json.dumps(auth), status=200, mimetype="application/json")

    if request.method == 'POST':
        if not request.files:
            return 'Nenhuma imagem selecionada', 400
    
        images = request.files
    
        if len(images) == 0:
            return 'Nenhum arquivo selecionado', 400

        try:
            # Define o diretório onde a imagem será salva
            save_dir = DATABASE_IMG_PATH + 'trilhas'

            nome_trilha = request.form['trilha']    
            path_trilha = os.path.join(save_dir, nome_trilha)

            if not os.path.exists(path_trilha):
                os.makedirs(path_trilha)

            print("*")
            for field_name, file in request.files.items():
                # Verificar se o campo é um arquivo
                if file.filename == '':
                    continue
                
                # Salvar o arquivo com o nome do campo
                caminho_arquivo = os.path.join(path_trilha, field_name)
                
                filerequestname = file.filename
                file_name,file_extension = os.path.splitext(filerequestname)

                save = caminho_arquivo+file_extension
                file.save(save)

            return 'Arquivos salvos com sucesso.'
        
        except Exception as e:
            print('Erro ', e)
            return str(e)

    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Formulário de Trilha</title>
</head>
<body>
    <form action="http://localhost:8080/criartrilha_upimg" method="post" enctype="multipart/form-data">
        <label for="trilha">Nome da Trilha:</label>
        <input type="text" id="trilha" name="trilha" required><br><br>
        
        <label for="icone">Selecione um ícone:</label>
        <input type="file" id="icone" name="icone" accept="image/*" required><br><br>
        
        <div id="seletores">
            <label for="campo_imagem">Nome do Campo da Imagem:</label>
            <input type="text" id="campo_imagem" name="campo_imagem" required>
            <input type="file" id="arquivo_imagem" name="arquivo_imagem" accept="image/*" required><br><br>
        </div>
        
        <button type="button" onclick="adicionarSelecionador()">+</button><br><br>
        
        <input type="submit" value="Enviar">
    </form>

    <script>
        function adicionarSelecionador() {
            var divSeletores = document.getElementById("seletores");

            var novoLabel = document.createElement("label");
            novoLabel.for = "campo_imagem_" + divSeletores.children.length;
            novoLabel.textContent = "Nome do Campo da Imagem:";
            divSeletores.appendChild(novoLabel);

            var novoSelecionador = document.createElement("input");
            novoSelecionador.type = "text";
            novoSelecionador.id = "campo_imagem_" + divSeletores.children.length;
            novoSelecionador.name = "campo_imagem_" + divSeletores.children.length;
            novoSelecionador.required = true;
            divSeletores.appendChild(novoSelecionador);

            var novoArquivo = document.createElement("input");
            novoArquivo.type = "file";
            novoArquivo.id = novoSelecionador.id
            novoArquivo.name = novoSelecionador.name
            novoArquivo.accept = "image/*";
            novoArquivo.required = true;

            novoArquivo.addEventListener('change', function() {
                novoSelecionador.value = this.files[0].name;
            });

            divSeletores.appendChild(novoArquivo);
            divSeletores.appendChild(document.createElement("br"));
        }
    </script>
</body>
</html>

    '''

