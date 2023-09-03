import pymysql
from tabulate import tabulate
import pymongo
import json
import requests
from colorama import Fore, Style  # Import colorama for colored output

print(Fore.GREEN + "[PROCESS] Reiniciando Banco de dados")

# Conectar ao banco de dados MySQL
conn = pymysql.connect(
    host="mysql",  # Endereço do servidor MySQL
    user="root",       # Nome de usuário
    password="root",   # Senha
    database="arduck"  # Nome do banco de dados
)

# Criar um cursor para interagir com o banco de dados
cursor = conn.cursor()

#file_path = 'api\\app\\models\\sql\\reset_table.sql'

#with open(file_path, 'r') as sql_file:
#    commands = sql_file.read()

commands = '''
DROP TABLE IF EXISTS usuario;
DROP TABLE IF EXISTS questoes;

CREATE TABLE IF NOT EXISTS usuario (
    id INT PRIMARY KEY AUTO_INCREMENT,
    password VARCHAR(150) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    turma VARCHAR(50) DEFAULT 'default',
    privilegio VARCHAR(50) DEFAULT 'usuario'
);

CREATE TABLE questoes (
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

'''

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

mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
mongoDB = mongoClient["ARduck"]

try:
    mongoDB.Trilhas.drop()
    mongoDB.Permissoes.drop()
    mongoDB.Progresso.drop()
except:
    mongoDB.create_collection("Trilhas")
    mongoDB.create_collection("Permissoes")
    mongoDB.create_collection("Progresso")

try:
    mongoDB.create_collection("Trilhas")
    mongoDB.create_collection("Permissoes")
    mongoDB.create_collection("Progresso")
except:
    print("*")

trilha_data = {
	"colecao":"Eletronica",
	"trilha_nome":"ARduck",
	"order":1,
	"turma":"defult",
	"validacao_pratica":"multimetro",
	"AR":True,
	"AR_id":"...",
	"descricao":"Resistores resistem",
	"habilitado_padrao":True,
    "Quiz_dic":[
        {
            "pergunta":"Quem é você?",
            "resposta_certa":"Sou o principio e o fim",
            "alternativa 1":"Jesus"
        }
    ]
    }

user_data = {
    'nome': 'Otavio Admin',
    'email': 'otavio.admin',
    'password': '123456',
    "privilegio": "administrador",
    "turma": "defult"
}

user_json = json.dumps(user_data)
registration_url = 'http://localhost:80/signup'
try:
    response = requests.post(registration_url, data=user_json, headers={'Content-Type': 'application/json'})

    if response.status_code == 200:
        print(Fore.GREEN + "[PROCESS] Registration successful!")
    elif response.status_code == 400:
        print(Fore.RED + "[ERRO] Registration failed. User data is invalid.")
    else:
        print(Fore.RED + "[ERRO] Registration failed with status code:", response.status_code)

except requests.exceptions.RequestException as e:
    print(Fore.RED + "[ERRO] An error occurred during registration:", str(e))

trilha_json = json.dumps(trilha_data)
registration_url = 'http://localhost:80/criartrilha'
try:
    response = requests.post(registration_url, data=trilha_json, headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        print(Fore.GREEN + "[PROCESS] Registration successful!")
    elif response.status_code == 400:
        print(Fore.RED + "[ERRO] Registration failed. User data is invalid.")
    else:
        print(Fore.RED + "[ERRO] Registration failed with status code:", response.status_code)

except requests.exceptions.RequestException as e:
    print(Fore.RED + "[ERRO] An error occurred during registration:", str(e))

select_data_sql = '''
SELECT nome, email, CONCAT(SUBSTRING(password, 1, 6), '...') AS password, privilegio, turma FROM usuario;
'''

cursor.execute(select_data_sql)
rows = cursor.fetchall()

column_names = [desc[0] for desc in cursor.description]

table = tabulate(rows, headers=column_names, tablefmt='grid')

print(Fore.CYAN + "[INFO] Usuários disponíveis: ")
print(table)

cursor.close()
conn.close()

print(Fore.GREEN + "[INFO] Collections created successfully!")
print(Fore.YELLOW + f"[INFO] Your keys: user -> {user_data['email']}, password -> {user_data['password']}")

print(Style.RESET_ALL)
