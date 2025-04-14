from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import pandas as pd
import plotly.express as px
import plotly.io as pio
import os

# Inicializando o Flask e o SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Função para processar o arquivo Excel
def process_file(file_path):
    try:
        # Tentando abrir o arquivo com o engine adequado
        df = pd.read_excel(file_path, engine='openpyxl')  # Usando openpyxl para arquivos .xlsx
    except ValueError:
        # Se falhar, tentar o engine 'xlrd' para arquivos mais antigos .xls
        df = pd.read_excel(file_path, engine='xlrd')

    # Verifica se as colunas "Categoria" e "Valor" existem
    if "Categoria" not in df.columns or "Valor" not in df.columns:
        raise ValueError('As colunas "Categoria" e "Valor" são necessárias no arquivo.')

    # Exemplo de criação de um gráfico simples (ajuste conforme seus dados)
    fig = px.bar(df, x="Categoria", y="Valor", title="Gráfico de Categorias")
    
    # Convertendo o gráfico para HTML
    graph_html = pio.to_html(fig, full_html=False)
    
    return graph_html

@app.route('/')
def index():
    return render_template('index.html')

# Rota para upload de arquivo
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file', 400

    # Salva o arquivo no diretório
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    try:
        # Processa o arquivo e gera o gráfico
        graph_html = process_file(file_path)
    except ValueError as e:
        # Em caso de erro nas colunas
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        # Para outros erros
        return jsonify({'message': 'Erro ao processar o arquivo: ' + str(e)}), 500

    # Emite o gráfico para o cliente via WebSockets
    print('Emitindo gráfico via WebSocket...')  # Adicionando log
    socketio.emit('update_graph', {'graph_html': graph_html})

    return jsonify({'message': 'Arquivo processado com sucesso'})

# Conexão via WebSocket
@socketio.on('connect')
def handle_connect():
    print('Cliente conectado')

# Inicia o servidor
if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')  # Cria a pasta para armazenar os arquivos
    socketio.run(app, debug=True)
