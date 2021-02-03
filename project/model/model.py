from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
def configure(app):
    db.init_app(app)
    app.db=db


class DadosMotor(db.Model):
    __name__ = "dadosmotor"
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(150))
    hora = db.Column(db.String(150))
    sensor1 = db.Column(db.String(150))

    def __init__(self, data, hora, sensor1):
        self.data = data
        self.hora = hora
        self.sensor1 = sensor1

