from flask import Flask, jsonify
from flask_cors import CORS
from models.base import db
import models  # noqa: F401 — registra Tutor, Animal, Consulta no SQLAlchemy


def create_app() -> Flask:
    app = Flask(__name__)

    # ── Configurações ────────────────────────────────────────────────────── #
    app.config["SQLALCHEMY_DATABASE_URI"]        = "sqlite:///petclinic.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.json.sort_keys = False   # preserva a ordem dos campos no JSON

    # ── Extensões ────────────────────────────────────────────────────────── #
    db.init_app(app)
    CORS(app)

    # ── Blueprints ───────────────────────────────────────────────────────── #
    from routes.tutores import bp_tutores
    app.register_blueprint(bp_tutores)

    # Fase 3 — descomente quando as rotas estiverem prontas:
    # from routes.animais   import bp_animais
    # from routes.consultas import bp_consultas
    # app.register_blueprint(bp_animais)
    # app.register_blueprint(bp_consultas)

    # ── Handlers globais de erro ─────────────────────────────────────────── #
    @app.errorhandler(404)
    def nao_encontrado(e):
        return jsonify({"erro": "Rota não encontrada."}), 404

    @app.errorhandler(405)
    def metodo_nao_permitido(e):
        return jsonify({"erro": "Método HTTP não permitido nesta rota."}), 405

    @app.errorhandler(500)
    def erro_interno(e):
        return jsonify({"erro": "Erro interno no servidor."}), 500

    # ── Banco de dados ───────────────────────────────────────────────────── #
    with app.app_context():
        db.create_all()
        print("[DB] Tabelas verificadas/criadas com sucesso.")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
