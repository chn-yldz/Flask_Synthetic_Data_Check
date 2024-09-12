from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

class UploadedData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200), nullable=False)  # İsim alanı
    last_name = db.Column(db.String(200), nullable=False)   # Soyisim alanı
    email = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    guid = db.Column(db.String(36), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"<UploadedData {self.first_name} {self.last_name}>"
