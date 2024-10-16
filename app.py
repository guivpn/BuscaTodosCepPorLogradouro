from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Função para buscar CEPs por logradouro
def buscar_cep_por_logradouro(logradouro, uf, cidade):
    url = f"https://viacep.com.br/ws/{uf}/{cidade}/{logradouro}/json/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Rota principal que renderiza a interface
@app.route('/')
def index():
    return render_template('index.html')

# Rota para buscar CEPs
@app.route('/buscar_ceps', methods=['GET'])
def buscar_ceps():
    logradouro = request.args.get('logradouro')
    uf = request.args.get('uf')
    cidade = request.args.get('cidade')

    if not logradouro or not uf or not cidade:
        return jsonify({'erro': 'Informe o logradouro, cidade e UF'}), 400

    # Busca os CEPs do logradouro
    ceps = buscar_cep_por_logradouro(logradouro, uf, cidade)

    if ceps:
        return jsonify(ceps)
    else:
        return jsonify({'erro': 'Nenhum CEP encontrado'}), 404

    
if __name__ == '__main__':
    app.run(debug=True)
