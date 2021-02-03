from flask_marshmallow import Marshmallow
from project.model.model import DadosMotor
ma = Marshmallow() #lib pra fazer as transformações
def configure(app):
    ma.init_app(app)
#pq todos estão com import?
class DadosMotorSchema(ma.ModelSchema):  #conversa entre o bd e meu codigo, o q tem no banco pro codigo e o outro
    class Meta:
        model = DadosMotor