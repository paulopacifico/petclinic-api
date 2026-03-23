from flask_sqlalchemy import SQLAlchemy

# Instância única do SQLAlchemy compartilhada por todos os models.
# É importada em cada model e inicializada no app.py com db.init_app(app).
db = SQLAlchemy()
