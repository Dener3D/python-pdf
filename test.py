from flask import Flask, request, jsonify
from src.controllers.controllers import Controller
import os

app = Flask(__name__)

@app.route('/join_pdf', methods=['POST'])
def join_pdf():
    controller = Controller()
    files = request.files.getlist('pdfs')
    print(files)
     
    bytes_pdf = []
    for pdf in files:
        bytes_pdf.append(pdf.read())
    
    response = controller.join_pdf(bytes_pdf)
    
    return {"res": response}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=3000, debug=True)