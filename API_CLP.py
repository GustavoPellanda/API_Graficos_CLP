import urllib.request
import urllib.error
import csv
import json
from flask import Flask, render_template

IP = input("Insira o endereço IP: ")
CLP_Endereco = f"http://{IP}//getvar.csv"

# Classe que guarda as informações de cada variável do CLP
# Modelo de uma variável: "LT_Temp_IHM",73,"",REAL,R,"24.55"
class Variavel_CLP:
    def __init__(var, name, id, desc, type, access, val):
        var.name = name
        var.id = id
        var.desc = desc
        var.type = type
        var.access = access
        var.val = val

# Obtém e filtra o CSV em busca do valor de uma variável
def obtem_valor_atual():
    # Requisita o arquivo CSV para o CLP
    try:
        url = urllib.request.urlopen(CLP_Endereco)
        responseCode = url.getcode()
        if responseCode == 200:
            inputStream = url.read()
            CSV_Conteudo = inputStream.decode('utf-8')
            url.close()
        else:
            print("Falha na requisição GET. Erro: " + str(responseCode))
    except urllib.error.URLError as e:
        print("Não foi possível enviar a requisiçaõ GET. Erro: " + str(e.reason))

    # Divide o CSV recebido em uma linha para cada variável
    divide_linhas = CSV_Conteudo.splitlines()
    CSV_EmLinhas = csv.reader(divide_linhas)

    # Define o ID da variável que será buscada:
    CLP_var_ID = "75"
    
    # Distrubui as informações de cada variável em seus respectivos atributos
    CLP_var = []
    for cadaLinha in CSV_EmLinhas:
        if cadaLinha[1] == CLP_var_ID:
            addVar = Variavel_CLP(name=cadaLinha[0], id=cadaLinha[1], desc=cadaLinha[2], type=cadaLinha[3], access=cadaLinha[4], val=cadaLinha[5])
            CLP_var.append(addVar)

    return CLP_var

# Criação da rota de dados Flask para o valor extraído da variável:
class Variavel_CLP_Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Variavel_CLP):
            return obj.__dict__
        return super().default(obj)

app = Flask(__name__)

valor_atual = obtem_valor_atual()

# Busca o template HTML
@app.route('/')
def display_variables():
    return render_template('index.html', var1=valor_atual)

# Envia a variável à página Web:
@app.route('/obtem_valor_atual')
def obtem_valor_atual_route():
    valor_atual = obtem_valor_atual()
    return json.dumps(valor_atual, cls=Variavel_CLPEncoder)

if __name__ == '__main__':
    app.run()
