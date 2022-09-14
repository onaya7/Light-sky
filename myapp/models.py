from flask_sqlalchemy import SQLAlchemy


# instanciating sqlalchemy
db = SQLAlchemy()

# database schema
class Cityname(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"Cityname('id:{self.id}','name:{self.name}')"