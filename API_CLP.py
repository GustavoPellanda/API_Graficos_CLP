from flask import Flask, request, render_template, json, redirect, session
import urllib.request
import urllib.error
import csv
import json

IP = input("Insira o endereço IP: ")
CLP_Endereco = f"http://{IP}//getvar.csv"

# Classe para guardar as informações de cada variável do CLP
# Modelo de uma variável: "LT_Temp_IHM",73,"descrição",REAL,R,"24.55"
class Variavel_CLP:
    def __init__(var, name, id, desc, type, access, val):
        var.name = name
        var.id = id
        var.desc = desc
        var.type = type
        var.access = access
        var.val = val

# Converte instâncias de Variavel_CLP para JSON:
class Variavel_CLP_Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Variavel_CLP):
            return obj.__dict__
        return super().default(obj)

# Requisita o arquivo CSV para o CLP:
def comunica_CLP(CLP_Endereco):
    try:
        url = urllib.request.urlopen(CLP_Endereco)
        responseCode = url.getcode()
        if responseCode == 200:
            inputStream = url.read()
            CSV_Bruto = inputStream.decode('utf-8')
            url.close()
        else:
            print("Falha na requisição GET. Erro: " + str(responseCode))
    except urllib.error.URLError as e:
        print("Não foi possível enviar a requisiçaõ GET. Erro: " + str(e.reason))

    # Divide o CSV recebido em uma linha para cada variável:
    CSV_Conteudo = csv.reader(CSV_Bruto.splitlines())

    return CSV_Conteudo


# Obtém todas as variáveis que serão disponibilizadas para escolha:
def obtem_variaveis_disponiveis():
    CSV_Conteudo = comunica_CLP(CLP_Endereco)

    # Filtra variáveis REAL e INT
    variaveis_disponiveis = []
    for cadaLinha in CSV_Conteudo:
        if len(cadaLinha) == 6 and (cadaLinha[3] == "REAL" or cadaLinha[3] == "INT"):
            variaveis_disponiveis.append(cadaLinha)

    return variaveis_disponiveis

# Obtém e filtra o CSV em busca do valor de uma variável:
def obtem_valor_atual():
    CSV_Conteudo = comunica_CLP(CLP_Endereco)

    # Busca o valor do ID recebido pelo POST do primeiro template
    id_var_selecionada = session.get('id_var_selecionada', None)
    if id_var_selecionada is None:
        id_var_selecionada = 0

    # Formata o valor do ID como string e sem espaço
    CLP_var_ID = str(id_var_selecionada).strip() 

    # Distrubui as informações de cada variável em seus respectivos atributos:
    CLP_var = []
    for cadaLinha in CSV_Conteudo:
        if cadaLinha[1] == CLP_var_ID:
            addVar = Variavel_CLP(
                name=cadaLinha[0], 
                id=cadaLinha[1], 
                desc=cadaLinha[2], 
                type=cadaLinha[3], 
                access=cadaLinha[4], 
                val=cadaLinha[5]
            )
            CLP_var.append(addVar)

    return CLP_var

app = Flask(__name__)
app.secret_key = '12345'

# Primeira Página:
@app.route('/', methods=['GET', 'POST'])
def tabela_disponiveis():
    if request.method == 'POST':
        # Recebe a variável escolhida e salva o ID em id_var_selecionada:
        var_selecionada = request.form.get('variable')
        id_var_selecionada = var_selecionada.split(',')[1].strip('"')
        session['id_var_selecionada'] = id_var_selecionada
        # Redireciona para o template do gráfico:
        return redirect('/template_grafico')

    return render_template('index.html', variables=obtem_variaveis_disponiveis())

# Segunda Página:
@app.route('/template_grafico')
def display_variaveis():
    return render_template('display_grafico.html')

# Alimenta a rota com Variavel_CLP atualizada:
@app.route('/valor_atual')
def valor_atual_route():
    valor_atual = obtem_valor_atual()
    return json.dumps(valor_atual, cls=Variavel_CLP_Encoder)

if __name__ == '__main__':
    app.run(debug=True)
