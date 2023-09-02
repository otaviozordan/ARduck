import pymysql
from tabulate import tabulate
import pymongo
import json
import requests
from colorama import Fore, Style  # Import colorama for colored output

print(Fore.GREEN + "[PROCESS] Criando Banco de dados")

# Conectar ao banco de dados MySQL
conn = pymysql.connect(
    host="localhost",  # Endereço do servidor MySQL
    user="root",       # Nome de usuário
    password="root",   # Senha
)

# Criar um cursor para interagir com o banco de dados
cursor = conn.cursor()

file_path = 'api\\app\\models\\sql\\criar_database.sql'

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