from flask import Flask
from routes import registrar_rotas
 
 
def create_app():
    app = Flask(__name__)
    registrar_rotas(app)
    return app
 
 
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)