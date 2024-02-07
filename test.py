from flask import Flask, request, jsonify
from barcode import Code128
from barcode.writer import ImageWriter
from src.controllers.controllers import Controller

app = Flask(__name__)

@app.route('/join_pdf', methods={'POST'})
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
    app.run(host=' https://pacific-earth-60757-12860c7b633c.herokuapp.com/', port=3000, debug=False)