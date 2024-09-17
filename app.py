from flask import Flask, request, jsonify, render_template
from models.database import db
from models.post import Post


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
app.config["SECRET_KEY"] = 'your_secret_key'
db.init_app(app)


# Rota para criar uma nova postagem
@app.route("/new_post", methods=['POST'])
def new_post():
    data = request.json
    title = data.get("title")
    content = data.get("content")
    author = data.get("author")

    if not title or not content or not author:
        return jsonify({"message": "Campos obrigatórios não preenchidos"}), 400
    
    # Salvando nova postagem e comitando no banco de dados
    post = Post(title=title, content=content, author=author)
    db.session.add(post)
    db.session.commit()
    
    return jsonify({"message": "Nova postagem criada com sucesso!"}), 201

# Rota para visualizar todas as postagens
@app.route("/", methods=['GET'])
def all_post():
    posts = Post.query.all()
    result = []

    if not posts:
        return jsonify({"message": "Sem novas postagens no momento"})
    
    for post in posts:
        result.append({
            "title": post.title,
            "content": post.content,
            "author": post.author,
            "date_posted": post.date_posted.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return render_template('all_post.html', posts=posts)

# Rota para obter um post específico
@app.route("/post/<int:id>", methods=['GET'])
def post_id(id):
    post = Post.query.get(id)

    if not post:
        return jsonify({"message": "Postagem não encontrada"}), 404
    
    return render_template('post.html', post=post)

# Rota para editar um post específico
@app.route("/edit_post/<int:id>", methods=['PUT'])
def edit_post(id):
    data = request.json
    post = Post.query.get(id)

    if not post:
        return jsonify({"message": "Postagem não encontrada"}), 404

    if data.get("title"):
        post.title = data.get("title")
    if data.get("content"):
        post.content = data.get("content")
    if data.get("author"):
        post.author = data.get("author")

    db.session.commit()
    return render_template('update.html', post=post)

# Rota para deletar uma postagem
@app.route("/delete_post/<int:id>", methods=['DELETE'])
def delete_post(id):
    post = Post.query.get(id)

    if not post:
        return jsonify({"message": "Postagem não encontrada"}), 404

    db.session.delete(post)
    db.session.commit()
    return render_template('delete.html', post=post)

if __name__ == "__main__":
    app.run(debug=True)