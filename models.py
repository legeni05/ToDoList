# models.py
from werkzeug.security import generate_password_hash, check_password_hash
from db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Méthode pour définir le mot de passe
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Méthode pour vérifier le mot de passe
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)



class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    date = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(5), nullable=False)


