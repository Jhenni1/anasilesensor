from flask_sqlalchemy import SQLAlchemy #lib do sql pra criar o bd
import click
from flask.cli import with_appcontext
db = SQLAlchemy()
def configure(app):
    db.init_app(app)
    app.db=db

##esse n tá
class DadosMotor(db.Model):  #aqui eu to criando a tabela do banco de dados ne?
    __name__ = "dadosmotor"
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(150))
    hora = db.Column(db.String(150))
    sensor1 = db.Column(db.String(150))

    def __init__(self, data, hora, sensor1):
        self.data = data
        self.hora = hora
        self.sensor1 = sensor1


@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()