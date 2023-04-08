from app.models.user_table import create_login_table
from app.models.questoes_table import create_quiz_table
from app import mongoDB

try: 
    mongoDB.create_collection("Permissoes")
except Exception as e:
    print('Erro: ', e, " [ao criar coleção]")

try: 
    mongoDB.create_collection("Trilhas")
except Exception as e:
    print('Erro: ', e, " [ao criar documento]")

try:    
    create_quiz_table()
except Exception as e:
    print('Erro: ', e, " [ao criar tabelas]")

try:
    create_login_table()
except Exception as e:
    print('Erro: ', e, " [ao criar tabelas]")

print("\n================================")
print("Trabelas criadas...")