# Importações para utilização do Flask e Flask_sqlalchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Instânciamento do Flask para uso
app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
db = SQLAlchemy(app)

# Modelação
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

# Execução do servidor Flask
@app.route('/')
def hello_world():
    return 'Hello World!'

# Checagem para saber se o arquivo está sendo usado diretamento ou importado por uma outra API
if __name__ == "__main__":
    app.run(debug=True)