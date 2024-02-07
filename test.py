from flask import Flask, request, jsonify, send_file
from src.controllers.controllers import Controller
import os

app = Flask(__name__)

@app.route('/join_pdf', methods=['POST'])
def join_pdf():
    controller = Controller()
    files = request.files.getlist('pdfs')
     
    bytes_pdf = []
    for pdf in files:
        bytes_pdf.append(pdf.read())
    
    response = controller.join_pdf(bytes_pdf)
    
    return {"res": response}

@app.route('/download_pdf', methods=['GET'])
def download_pdf():
    try:
        filename = request.args.get('filename')
        # Caminho para o arquivo PDF salvo localmente
        filepath = os.path.join(app.root_path, filename)
        # Verifica se o arquivo existe
        if os.path.exists(filepath):
            # Envia o arquivo como resposta à solicitação GET
            return send_file(filepath, as_attachment=True)
        else:
            return {'status': 'error', 'message': 'Arquivo não encontrado'}

    except Exception as e:
        return {'status': 'error', 'message': str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
