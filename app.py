from flask import Flask, request, send_file
from model.model import configure as db_config
from serializer.serializer import  configure as ma_config
from flask_migrate import Migrate
from serializer.serializer import DadosMotorSchema
from datetime import date, datetime
from model.model import DadosMotor

import os
import csv
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:xw1102@localhost:5432/postgres'
app.config['SECRET_KEY'] = 'e7c0596d00d6d1d17e64d6547cd732cf'
db_config(app)
ma_config(app)
Migrate(app,app.db)

@app.route('/')
def home(): #def = função
   return "Oi"

@app.route('/dados',methods = ['POST'])
def receber ():
   dado=request.json
   print(dado)
   data_atual = date.today()
   data_atual = "{}/{}/{}".format(data_atual.day, data_atual.month,data_atual.year)
   now = datetime.now()
   hour = str(now.hour) + ":" + str(now.minute)
   dado["data"]= data_atual
   dado["hora"]= hour
   dm=DadosMotorSchema()
   Dado=dm.load(dado)
   app.db.session.add(Dado)
   app.db.session.commit()
   return "deu tudo certo"

@app.route("/baixar_dado")
def baixar_dado ():
   dms = DadosMotorSchema(many=True)
   dados = DadosMotor.query.all()
   result = dms.dumps(dados)
   result = eval(result)
   cols = ['data', 'hora', 'sensor1', 'id']
   with open("output.csv", 'w') as f:
      wr = csv.DictWriter(f, fieldnames=cols)
      wr.writeheader()
      wr.writerows(result)
   print(result)
   path = os.getcwd()+"/output.csv"
   return send_file(path, as_attachment=True)




##app.run(debug=True)
app.run(host='0.0.0.0', debug=False)



