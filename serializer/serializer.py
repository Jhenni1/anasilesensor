from flask_marshmallow import Marshmallow
from model.model import DadosMotor
ma = Marshmallow()
def configure(app):
    ma.init_app(app)

class DadosMotorSchema(ma.ModelSchema):
    class Meta:
        model = DadosMotor