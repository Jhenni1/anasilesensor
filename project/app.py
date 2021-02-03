from flask import Flask, request, send_file
from project.model.model import configure as db_config
from project.serializer.serializer import  configure as ma_config
from flask_migrate import Migrate
from project.serializer.serializer import DadosMotorSchema
from datetime import date, datetime
from project.model.model import DadosMotor

import os
import csv
##kd os from??w

app = Flask(__name__) ## nome
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False ## suas funcionalidades
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:xw1102@localhost:5432/postgres'  ## ?
app.config['SECRET_KEY'] = 'e7c0596d00d6d1d17e64d6547cd732cf' ## ?
db_config(app) ## inserindo exteões
ma_config(app) ## ? bd
Migrate(app,app.db) ## ?

#primeira rota
@app.route('/')
def home(): #def = função
   return "Oi"

#segunda rota
@app.route('/dados',methods = ['POST']) #dizer o metodo da rota, nesse caso é post
def receber(): #o tipo da função
   dado=request.json#requisitando um arquivo json
   print(dado)#mostra
   data_atual = date.today() #date é a lib
   data_atual = "{}/{}/{}".format(data_atual.day, data_atual.month,data_atual.year) # formatando a data contatenar dados
   now = datetime.now() #agora pegar a hora
   hour = str(now.hour) + ":" + str(now.minute) #concatenar o foamato da hora
   dado["data"]= data_atual #adicionando o campo data no dado
   dado["hora"]= hour #mesma coisa
   dm=DadosMotorSchema() #chamando/instanciando os dados pra armazenar no banco de dados
   Dado=dm.load(dado) #transformando o dados emquery pra armazenar no bd
   app.db.session.add(Dado) #adiconando o Dado no nosso banco
   app.db.session.commit() #confirmando que os dados estão ai, são necessarios pra salvar
   return "deu tudo certo"

#terceira rota de baixar os dados em formato de excel
@app.route("/baixar_dado")
def baixar_dado ():
   dms = DadosMotorSchema(many=True)
   dados = DadosMotor.query.all()
   result = dms.dumps(dados)
   result = eval(result)
   cols = ['data', 'hora', 'sensor1', 'id']
   with open("../output.csv", 'w') as f:
      wr = csv.DictWriter(f, fieldnames=cols)
      wr.writeheader()
      wr.writerows(result)
   print(result)
   path = os.getcwd()+"/output.csv"
   return send_file(path, as_attachment=True)




##app.run(debug=True)
app.run(host='0.0.0.0', debug=False) ## ainda ta criando meu servidor global?



