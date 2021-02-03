from flask_marshmallow import Marshmallow
from project.model.model import DadosMotor
ma = Marshmallow()
def configure(app):
    ma.init_app(app)
#pq todos estão com import?
class DadosMotorSchema(ma.ModelSchema):
    class Meta:
        model = DadosMotor