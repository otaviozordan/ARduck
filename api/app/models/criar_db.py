import pymysql
import pymongo
from colorama import Fore, Style  # Import colorama for colored output

print(Fore.GREEN + "[PROCESS] Criando Banco de dados")

# Conectar ao banco de dados MySQL
conn = pymysql.connect(
    host="localhost",  # Endereço do servidor MySQL
    user="root",       # Nome de usuário
    password="root",   # Senha
    database="arduck"
)

# Criar um cursor para interagir com o banco de dados
cursor = conn.cursor()

#file_path = 'ARduck/api/app/models/sql/criar_database.sql'
#
#with open(file_path, 'r') as sql_file:
#    commands = sql_file.read()

commands = """
CREATE DATABASE IF NOT EXISTS arduck;

USE arduck;

CREATE TABLE IF NOT EXISTS usuario (
    id INT PRIMARY KEY AUTO_INCREMENT,
    password VARCHAR(150) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    turma VARCHAR(50) DEFAULT 'default',
    privilegio VARCHAR(50) DEFAULT 'usuario'
);

CREATE TABLE IF NOT EXISTS questoes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    colecao VARCHAR(50) NOT NULL,
    titulo VARCHAR(50) NOT NULL,
    texto VARCHAR(244) NOT NULL,
    imgPath VARCHAR(50) DEFAULT NULL,
    respostaCorreta VARCHAR(50) NOT NULL,
    alternativa1 VARCHAR(50),
    alternativa2 VARCHAR(50),
    alternativa3 VARCHAR(50),
    alternativa4 VARCHAR(50)
);
"""

# Dividir os comandos em uma lista
command_list = commands.split(';')

try:
    for command in command_list:
        if command.strip():
            cursor.execute(command)
    conn.commit()
    print(Fore.GREEN + "[INFO] Comandos executados com sucesso.")
except pymysql.Error as err:
    print(Fore.RED + f"[ERRO] Erro ao executar os comandos: {err}")

cursor.close()
conn.close()

mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
mongoDB = mongoClient["ARduck"]

try:
    mongoDB.create_collection("Trilhas")
    mongoDB.create_collection("Permissoes")
    mongoDB.create_collection("Progresso")
except:
    print(Fore.YELLOW + "[AVISO] As coleções já existem.")

# Redefinir cores ao final
print(Style.RESET_ALL)