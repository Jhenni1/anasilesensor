from flask import Flask, request, send_file
from project.model.model import configure as db_config
from project.serializer.serializer import  configure as ma_config
from flask_migrate import Migrate
from project.serializer.serializer import DadosMotorSchema
from datetime import date, datetime
from project.model.model import DadosMotor

import os
import csv
from flask_cors import CORS
from project.model.model import create_tables

app = Flask(__name__) ## nome
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False ## suas funcionalidades
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://xoehqsvxqhisvt:64fc782f4ab85557e9fa15427dcee485a6627fb7dbfcaaea16d5ec83aa3956e4@ec2-18-204-101-137.compute-1.amazonaws.com:5432/dcub541uu809c8'  ## ?
app.config['SECRET_KEY'] = 'e7c0596d00d6d1d17e64d6547cd732cf' ## ?
db_config(app) ## inserindo exteões
ma_config(app) ## ? bd
Migrate(app,app.db) ## ?
app.cli.add_command(create_tables)

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
   dms = DadosMotorSchema(many=True)#requistar todos os dados de uma tabela especifica
   dados = DadosMotor.query.all()#retorne os todos os dados
   result = dms.dumps(dados) # dumps= transforma o dado de bd pra json ou python e retorna em formato de texto
   result = eval(result) # transdormar (eval) de string pra json valendo
   cols = ['data', 'hora', 'sensor1', 'id'] #titulo da coluna botando do mesmo jeito do bd
   with open("output.csv", 'w') as f: #to abrindo um arquivo csv
      wr = csv.DictWriter(f, fieldnames=cols) #organizador
      wr.writeheader() #titulo
      wr.writerows(result) #dados de cada coluna
   print(result)
   path = os.getcwd()+"/output.csv" #caminho do codigo atual
   return send_file(path, as_attachment=True) #send_file do flask pegue o arquivo do direotiro pra poder baixar

@app.route("/visualizar_dado")
def visualizar_dado ():
   dms= DadosMotorSchema(many=True)
   result = DadosMotor.query.all()
   return dms.jsonify(result)




##app.run(debug=True)
#app.run(host='0.0.0.0', debug=False) ## to dizendo que to usando o ip do wifi

cors = CORS(app, resource={r"/*": {"origins": "*"}})

def main():
    app.db.create_all()
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()

