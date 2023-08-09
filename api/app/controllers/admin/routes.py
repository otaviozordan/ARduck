from app import app,db
from flask import render_template, redirect
from flask_login import current_user
from app.models.user_table import Usuario, authenticate

@app.route('/')
def index():
    auth = authenticate("professor")
    if auth:
        return redirect("/login")
    print("[INFO] Sessão iniciada por: ", current_user.nome)
    return render_template('home/index.html')


@app.route('/login', methods=['GET'])
def login_render():
    return render_template('auth/login.html')