from app import app,db

@app.route('/hello')
def index():
    return "Hello World"
