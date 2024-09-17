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


if __name__ == "__main__":
    app.run(debug=True)