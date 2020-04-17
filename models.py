from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

"""
class Todos(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    tareas = db.Column(db.String(500), nullable=True)

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "tareas": self.tareas
        }

"""