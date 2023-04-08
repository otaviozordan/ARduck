from app import db, mongoDB, app
from app.models.user_table import delete_login_table
from app.models.questoes_table import delete_quiz_table

try:
    delete_login_table()
except Exception as e:
    print('Erro: ', e, "[ao deletar tabela]")

try:
    delete_quiz_table()
except Exception as e:
    print('Erro: ', e, "[ao deletar tabela]")

try: 
    mongoDB.Permissoes.drop()
except Exception as e:
    print('Erro: ', e, " [ao deletar coleção]")

try: 
    mongoDB.Trilhas.drop()
except Exception as e:
    print('Erro: ', e, " [ao deletar coleção]")

import create_table
