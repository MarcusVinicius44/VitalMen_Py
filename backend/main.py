import os
from flask import Flask, send_from_directory, render_template_string
from flask_cors import CORS

from backend.controllers import (
    post_controller,
    tarefa_controller,
    user_controller,
    listas_controller,
    comments
)

from backend.database.db_config import DATABASE_URL
from backend.models import db, User


app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_size": 1,
    "max_overflow": 0,
    "pool_pre_ping": True
}

db.init_app(app)

# Blueprints
app.register_blueprint(post_controller.post_bp)
app.register_blueprint(tarefa_controller.tarefa_bp)
app.register_blueprint(user_controller.user_bp)
app.register_blueprint(listas_controller.lista_bp)
app.register_blueprint(comments.comment_bp)


# Criar tabelas automaticamente
with app.app_context():
    db.create_all()


# Caminho do frontend
FRONT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "frontend")
)


# -----------------------------
# Rotas HTML
# -----------------------------

@app.route("/")
@app.route("/home")
def index():
    return send_from_directory(os.path.join(FRONT_DIR, "index"), "index.html")


@app.route("/<page>/")
def page(page):
    return send_from_directory(os.path.join(FRONT_DIR, page), f"{page}.html")


# -----------------------------
# Arquivos estáticos
# -----------------------------

@app.route("/<page>/<path:filename>")
def page_files(page, filename):
    return send_from_directory(os.path.join(FRONT_DIR, page), filename)


# -----------------------------
# Página 404
# -----------------------------

@app.errorhandler(404)
def page_not_found(e):
    error_page = os.path.join(FRONT_DIR, "errors", "404.html")

    if os.path.exists(error_page):
        return send_from_directory(
            os.path.join(FRONT_DIR, "errors"),
            "404.html"
        ), 404

    return render_template_string(
        "<h1>404</h1><p>Página não encontrada.</p>"
    ), 404


# -----------------------------
# Rodar localmente
# -----------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)