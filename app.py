from flask import jsonify
from flask_openapi3 import OpenAPI, Info
from flask_cors import CORS
from models.base import db
import models

info = Info(title="PetClinic API", version="1.0.0", description="Prontuário eletrônico veterinário")


def create_app():
    app = OpenAPI(__name__, info=info)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///petclinic.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.json.sort_keys = False

    db.init_app(app)
    CORS(app)

    from routes.tutores import bp_tutores
    from routes.animais import bp_animais
    from routes.consultas import bp_consultas

    app.register_api(bp_tutores)
    app.register_api(bp_animais)
    app.register_api(bp_consultas)

    @app.errorhandler(404)
    def nao_encontrado(e):
        return jsonify({"erro": "Rota não encontrada."}), 404

    @app.errorhandler(405)
    def metodo_nao_permitido(e):
        return jsonify({"erro": "Método HTTP não permitido nesta rota."}), 405

    @app.errorhandler(500)
    def erro_interno(e):
        return jsonify({"erro": "Erro interno no servidor."}), 500

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5001)
