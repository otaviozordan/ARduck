import pymysql
from tabulate import tabulate
import pymongo

#Se erro acesse o terminal para alterar sua senha para 'root':
# mysqlsh --sql --user=root --password=<sua_password>
# ALTER USER 'root'@'localhost' IDENTIFIED WITH 'mysql_native_password' BY 'root';

print("[PROCESS] Reiniciando Banco de dados")
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

# Executar os comandos SQL em um loop
try:
    for command in command_list:
        if command.strip():
            cursor.execute(command)
    conn.commit()
    print("[INFO] Comandos executados com sucesso.")
except pymysql.Error as err:
    print(f"[ERRO] Erro ao executar os comandos: {err}")

# Consultar dados da tabela
select_data_sql = '''
SELECT * FROM usuario;
'''
cursor.execute(select_data_sql)
rows = cursor.fetchall()

# Obter os nomes das colunas
column_names = [desc[0] for desc in cursor.description]

# Formatar os resultados como uma tabela
table = tabulate(rows, headers=column_names, tablefmt='grid')

print("[INFO] Usuários disponiveis: ")
# Exibir a tabela no console
print(table)

# Fechar o cursor e a conexão com o banco de dados
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