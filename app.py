# Importações para utilização do Flask e Flask_sqlalchemy
from flask import Flask, request, jsonify
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
    
# Rotas

@app.route('/api/products/add', methods=["POST"])
def add_product():
    data = request.json
    
    if "name" in data and "price" in data:
        # data["CHAVE"] -> retorna o valor da chave, porém se não encontrar, da erro
        # data.get("CHAVE", "VALOR CASO NAO ENCONTRE") -> retorna o valor da chave, porém se não encontrar, substitui por outro valor escolhido
        product = Product(name=data["name"], price=data["price"], description=data.get("description", ""))
        
        db.session.add(product)
        db.session.commit()
    
        return jsonify({"message": "Product added sucessfully"}), 200
    return jsonify({"message": "Invalid product data"}), 400

@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({"message": "Product deleted sucessfully"})
    return jsonify({"message": "Product not found"}), 404
    
@app.route('/api/products/<int:product_id>', methods=["GET"])
def get_product_details(product_id):
    product = Product.query.get(product_id)
    
    if product:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        })
        
    return jsonify({"message": "Product not found"}), 404
    
@app.route('/api/products/update/<int:product_id>', methods=["PUT"])
def update_product(product_id):
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({"message": "Product not found"}), 404
    
    data = request.json
    
    if "name" in data:
        product.name = data["name"] 
    
    if "price" in data:
        product.price = data["price"]
        
    if "description" in data:
        product.description = data["description"]
        
    db.session.commit()
        
    return jsonify({"message": "Product updated sucessfully"})

@app.route('/api/products', methods=["GET"])
def get_products():
    products = Product.query.all()
    
    product_list = []
    
    for product in products:
        product_data = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
        }
        
        product_list.append(product_data)

    return jsonify(product_list)

# Execução do servidor Flask
@app.route('/')
def hello_world():
    return 'Hello World!'

# Checagem para saber se o arquivo está sendo usado diretamento ou importado por uma outra API
if __name__ == "__main__":
    app.run(debug=True)