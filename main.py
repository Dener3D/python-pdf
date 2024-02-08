from flask import Flask, request, jsonify, send_file
from src.controllers.controllers import Controller
import os
import time
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

def delete_pdfs():
    try:
        # Diretório raiz do projeto
        root_directory = app.root_path

        # Obtém a lista de arquivos na raiz do projeto
        files_in_root = os.listdir(root_directory)

        # Filtra apenas os arquivos PDF
        pdf_files = [file for file in files_in_root if file.endswith('.pdf')]

        # Exclui cada arquivo PDF encontrado
        for pdf_file in pdf_files:
            pdf_filepath = os.path.join(root_directory, pdf_file)
            os.remove(pdf_filepath)

        return {'status': 'success', 'message': 'Arquivos PDF excluídos com sucesso'}

    except Exception as e:
        return {'status': 'error', 'message': str(e)}
    
def delete_pdfs_job():
    with app.app_context():
        delete_pdfs()

scheduler = BackgroundScheduler()

scheduler.add_job(func=delete_pdfs_job, trigger='interval', minutes=60)
scheduler.start()

controller = Controller()

@app.route('/join_pdf', methods=['POST'])
def join_pdf(): 
    files = request.files.getlist('pdfs')
    bytes_pdf = []
    for pdf in files:
        bytes_pdf.append(pdf.read())
    
    response = controller.join_pdf(bytes_pdf)
    
    return {"res": response}

@app.route('/split_pdf', methods=['POST'])
def split_pdf():
    pdf = request.files.get('pdf')
    return controller.split_pdf(pdf, app.root_path)

@app.route('/download_pdf', methods=['GET'])
def download_pdf():
    try:
        filename = request.args.get('filename')
        # Caminho para o arquivo PDF salvo localmente
        filepath = os.path.join(app.root_path, filename)
        print(filepath)
        # Verifica se o arquivo existe
        if os.path.exists(filepath):
            #with open(filepath, 'rb') as file:
            response = send_file(filepath, as_attachment=True, mimetype='application/pdf', download_name='merged_file.pdf')
            # Remove o arquivo após o download
            return response
        else:
            return {'status': 'error', 'message': 'Arquivo não encontrado'}

    except Exception as e:
        return {'status': 'error', 'message': str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
