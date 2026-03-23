from flask import Flask
from flask_cors import CORS
from models.base import db
import models  # noqa: F401 — registra Tutor, Animal, Consulta no SQLAlchemy


def create_app() -> Flask:
    """
    Factory function que cria e configura a aplicação Flask.
    Usar factory facilita testes e evita importações circulares.
    """
    app = Flask(__name__)

    # ------------------------------------------------------------------ #
    # Configurações do banco de dados                                      #
    # ------------------------------------------------------------------ #
    # SQLite local: o arquivo petclinic.db é criado na raiz do projeto.
    # Em produção, trocar pela URI do banco desejado sem mudar mais nada.
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///petclinic.db"

    # Desliga o rastreamento de modificações (economiza memória e é
    # desnecessário aqui pois não usamos signals do SQLAlchemy).
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ------------------------------------------------------------------ #
    # Extensões                                                            #
    # ------------------------------------------------------------------ #
    db.init_app(app)      # vincula o SQLAlchemy a esta instância do Flask
    CORS(app)             # permite que o index.html (file://) chame a API

    # ------------------------------------------------------------------ #
    # Rotas (serão registradas nas próximas fases via Blueprints)          #
    # ------------------------------------------------------------------ #
    # from routes.tutores   import bp_tutores
    # from routes.animais   import bp_animais
    # from routes.consultas import bp_consultas
    # app.register_blueprint(bp_tutores)
    # app.register_blueprint(bp_animais)
    # app.register_blueprint(bp_consultas)

    # ------------------------------------------------------------------ #
    # Criação das tabelas                                                  #
    # ------------------------------------------------------------------ #
    with app.app_context():
        db.create_all()
        print("[DB] Tabelas criadas com sucesso.")

    return app


# Ponto de entrada para rodar com:  python app.py
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
