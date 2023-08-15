import subprocess

# Função para imprimir uma mensagem em vermelho
def print_red(text):
    print("\033[91m" + text + "\033[0m")

# Função para imprimir uma mensagem em verde
def print_green(text):
    print("\033[92m" + text + "\033[0m")

# Comando para instalar as dependências do requirements.txt
command = 'pip install -r api\\requirements.txt'

try:
    # Executa o comando usando o subprocess
    subprocess.check_call(command, shell=True)
    print_green("Dependências instaladas com sucesso.")
except subprocess.CalledProcessError:
    print_red("Erro ao instalar as dependências.")


# Comando para instalar as dependências do requirements.txt
command = 'py api\\app\models\\reiniciar_dbs.py'

try:
    # Executa o comando usando o subprocess
    subprocess.check_call(command, shell=True)
    print_green("Bancos de dados instaladas com sucesso.")
except subprocess.CalledProcessError:
    print_red("Erro ao instalar bancos.")
