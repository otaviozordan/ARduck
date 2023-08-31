# Use a imagem base que possui Python e as bibliotecas necessárias
FROM python:3.8

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências da sua aplicação
RUN pip install -r requirements.txt

# Copie todo o código fonte da sua aplicação para o contêiner
COPY . .

# Exponha a porta que sua aplicação Flask usa (por exemplo, 5000)
EXPOSE 80

# Inicie sua aplicação Flask
CMD ["python", "app.py"]
