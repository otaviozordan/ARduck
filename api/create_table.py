from app.models.user_table import create_login_table
from app.models.questoes_table import create_quiz_table
from app import mongoDB
from pymongo import ASCENDING

try: 
    mongoDB.create_collection("Permissoes")
    mongoDB.Permissoes.create_index([('email', -1)],unique=True)
except Exception as e:
    print('Erro: ', e, " [ao criar coleção Permissoes]")


try: 
    mongoDB.create_collection("Trilhas")
except Exception as e:
    print('Erro: ', e, " [ao criar coleção Trilhas]")

try: 
    mongoDB.create_collection("Progresso")
    mongoDB.Progresso.create_index([('email', -1)],unique=True)
except Exception as e:
    print('Erro: ', e, " [ao criar coleção Progresso]")

try:    
    create_quiz_table()
except Exception as e:
    print('Erro: ', e, " [ao criar tabelas]")

try:
    create_login_table()
except Exception as e:
    print('Erro: ', e, " [ao criar tabelas]")

print("\n=================================================")
print("Concluido")