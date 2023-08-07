from app import db, mongoDB, app
from app.models.user_table import delete_login_table
from app.models.questoes_table import delete_quiz_table


print("Selecione o database a ser resetado...")
print("a) Tabelas de usuários")
print("b) Tabela de questões")
print("c) Documento de Trilhas")
print("d) Documento de Permissões")
print("e) Documento de Progresso")
print("All) Tudo")
comand = input()

if comand == 'a'  or comand == "All":
    try:
        delete_login_table()
    except Exception as e:
        print('Erro: ', e, "[ao deletar tabela]")

if comand == 'b' or comand == "All":
    try:
        delete_quiz_table()
    except Exception as e:
        print('Erro: ', e, "[ao deletar tabela]")

if comand == 'c' or comand == 'All':
    try: 
        mongoDB.Trilhas.drop()
    except Exception as e:
        print('Erro: ', e, " [ao deletar coleção]")

if comand == "d" or comand == "All":
    try: 
        mongoDB.Permissoes.drop()
    except Exception as e:
        print('Erro: ', e, " [ao deletar coleção]")

if comand == "e" or comand == "All":
    try: 
        mongoDB.Progresso.drop()
    except Exception as e:
        print('Erro: ', e, " [ao deletar coleção]")

print ("\n\n-----------------RECRIANDO TABELAS---------------")
import create_table
print ("\n\n")
