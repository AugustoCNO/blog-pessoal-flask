from flask import Flask, request, jsonify
from flask_login import current_user, login_required, login_user, logout_user, LoginManager
from models.database import db
from models.user import User


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
app.config["SECRET_KEY"] = 'your_secret_key'
login_manager = LoginManager()

login_manager.init_app(app)
db.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#rota para criação de uma nova postagem
@app.route("/new_post", methods=['POST'])
def new_post():
    data = request.json
    title = data.get("title")
    content = data.get("content")
    author = data.get("author")


    if not title or not content or not author:
        return jsonify({"message": "campos obrigatorios não preenchidos"}),400
    
    #salvando nova postagem e comitando no banco de dados
    post = User(title=title, content=content, author=author)
    db.session.add(post)
    db.session.commit()
    return jsonify({"message": "nova postagem criada com sucesso"})


#rota para visualizar todas as postagens
@app.route("/", methods=['GET'])
def all_post():
    posts = User.query.all()
    result = []

    if not posts:
        return jsonify({"message": "sem novas postagem no momento"})
    
    #laço de repetição para percorrer meus posts e salvar dentro de uma lista para que eu consiga visualizar todas as postagens
    for post in posts:
        result.append({
            "title": post.title,
            "content": post.content,
            "author": post.author
        })
    return jsonify(result)


#rota para obter um post especifico
@app.route("/post/<int:id>", methods=['GET'])
def post_id(id):
    post = User.query.get(id)

    if not post:
        return jsonify({"message": "postagem não encontrada"}), 400
    
    #retorno a postagem especifica baseado no id
    return jsonify({"title": post.title, "content": post.content, "author": post.author})


#rota para editar um post especifico
@app.route("/edit_post/<int:id>", methods=['PUT'])
def edit_post(id):
    data = request.json
    post = User.query.get(id)

# aqui eu estou obtendo as informaçoes do json guardando no meu titulo, content e author e tambem commitando a mudança no banco de dados
    if post and data.get("title") and data.get("content") and data.get("author"):
        post.title = data.get("title")
        post.content = data.get("content")
        post.author = data.get("author")
        db.session.commit()
        return jsonify({"message": "postagem atualizada com sucesso"})


#rota para deletar uma postagem
@app.route("/delete_post/<int:id>", methods=['DELETE'])
def delete_post(id):
    post = User.query.get(id)

    if post:
        db.session.delete(post)
        db.session.commit()
        return jsonify({"message": "postagem deletada com sucesso"})


if __name__ == "__main__":
    app.run(debug=True)