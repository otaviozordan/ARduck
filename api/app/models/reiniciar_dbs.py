import pymysql
from tabulate import tabulate
import pymongo
import json
import requests
from colorama import Fore, Style  # Import colorama for colored output

print(Fore.GREEN + "[PROCESS] Reiniciando Banco de dados")

# Conectar ao banco de dados MySQL
conn = pymysql.connect(
    host="localhost",  # Endereço do servidor MySQL
    user="root",       # Nome de usuário
    password="root",   # Senha
    database="arduck"  # Nome do banco de dados
)

# Criar um cursor para interagir com o banco de dados
cursor = conn.cursor()

file_path = 'api\\app\\models\\sql\\reset_table.sql'

with open(file_path, 'r') as sql_file:
    commands = sql_file.read()

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

user_data = {
    'nome': 'Otavio Admin',
    'email': 'otavio.admin',
    'password': '123456',
    "privilegio": "administrador",
    "turma": "defult"
}

user_json = json.dumps(user_data)
registration_url = 'http://localhost:8080/signup'
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

print(Fore.GREEN + "[INFO] Collections created successfully!")
print(Fore.YELLOW + f"[INFO] Your keys: user -> {user_data['email']}, password -> {user_data['password']}")

print(Style.RESET_ALL)
