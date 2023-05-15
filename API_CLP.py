from flask import Flask, request, render_template, json, redirect, session
import urllib.request
import urllib.error
import csv
import json
import requests

CLP_IP = "133.2.103.186"

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
            return {
                'name': obj.name,
                'val': obj.val,
            }
        return json.JSONEncoder.default(self, obj)

# Requisita o arquivo CSV completo para o CLP:
def comunica_CLP_todas(CLP_IP):
    try:
        url = urllib.request.urlopen(f"http://{CLP_IP}/getvar.csv")
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
    CSV_Conteudo = comunica_CLP_todas(CLP_IP)

    # Filtra variáveis REAL e INT
    variaveis_disponiveis = []
    for cadaLinha in CSV_Conteudo:
        if len(cadaLinha) == 6 and (cadaLinha[3] == "REAL" or cadaLinha[3] == "INT"):
            variaveis_disponiveis.append(cadaLinha)

    return variaveis_disponiveis

# Requisita uma variável específica para o CLP:
def comunica_CLP_variavel(CLP_IP, id_var):
    try:
        url = urllib.request.urlopen(f"http://{CLP_IP}/getvar.csv?id={id_var}")
        responseCode = url.getcode()
        if responseCode == 200:
            inputStream = url.read()
            VAR_Conteudo = inputStream.decode('utf-8')
            url.close()
        else:
            print("Falha na requisição GET. Erro: " + str(responseCode))
    except urllib.error.URLError as e:
        print("Não foi possível enviar a requisiçaõ GET. Erro: " + str(e.reason))

    return VAR_Conteudo

# Salva a variável selecionada em CLP_var:
def obtem_valor_atual():
    # Busca o valor do ID recebido pelo POST do primeiro template
    id_var = session.get('id_var_selecionada', None)

    # Formata o valor do ID como string e sem espaço
    id_var = str(id_var).strip() 

    # Receve o retorno da variável específica:
    VAR_Conteudo = comunica_CLP_variavel(CLP_IP, id_var)

    # Distrubui as informações de cada variável em seus respectivos atributos:
    CLP_var = []
    reader = csv.reader(VAR_Conteudo.splitlines())
    next(reader)  # Pula a primeira linha

    for valor_separado in reader:
        addVar = Variavel_CLP(
            name=valor_separado[0].strip('"'),
            id=valor_separado[1],
            desc=valor_separado[2].strip('"'),
            type=valor_separado[3],
            access=valor_separado[4],
            val=valor_separado[5].strip('"')
        )
        CLP_var.append(addVar)

    return CLP_var

app = Flask(__name__, static_folder='static')
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

    return render_template('variaveis.html', variables=obtem_variaveis_disponiveis())

# Segunda Página:
@app.route('/template_grafico')
def display_variaveis():
    return render_template('display_grafico.html')

# Alimenta a rota com Variavel_CLP atualizada:
@app.route('/valor_atual')
def valor_atual_route():
    valor_atual = obtem_valor_atual()
    return json.dumps(valor_atual, cls=Variavel_CLP_Encoder)

# Recebe o valor da variável a ser alterada:
@app.route('/altera_variavel', methods=['POST'])
def altera_variavel_CLP():
    if request.method == 'POST':
        name = request.form['name']
        value = request.form['value']
        url = f"http://{CLP_IP}/setvar.csv"
        data = {name: value}
        # Envia ao CLP:
        requests.post(url, data=data)
        return render_template('display_grafico.html')

if __name__ == '__main__':
    app.run(debug=True)
