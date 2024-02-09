from flask import Flask, request, jsonify, send_file, Response, json, abort
from src.controllers.controllers import Controller
import os
import time
from apscheduler.schedulers.background import BackgroundScheduler
from flask_basicauth import BasicAuth
from werkzeug.exceptions import HTTPException, Unauthorized
import werkzeug
from datetime import datetime

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = os.environ.get("USERNAME")
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get("PASSWORD")

basic_auth = BasicAuth(app)

# Job que roda para deletar os pdfs do dia
def delete_pdfs_job():
    with app.app_context():
        controller.delete_pdfs(app.root_path)

scheduler = BackgroundScheduler()

scheduler.add_job(func=delete_pdfs_job, trigger='cron', hour=23, minute=59)
scheduler.start()

controller = Controller()

def check_credentials():
    if not basic_auth.authenticate():
        raise werkzeug.exceptions.Unauthorized

@app.errorhandler(werkzeug.exceptions.Unauthorized)
def custom_401(e):
    return {"Error": 401, "Message": "Unauthorized"}


@app.route('/join_pdf', methods=['POST'])
def join_pdf():
    try: 
        check_credentials()
        files = request.files.getlist('pdfs')
        bytes_pdf = []
        for pdf in files:
            bytes_pdf.append(pdf.read())
        
        response = controller.join_pdf(bytes_pdf)
        
        return {"res": response}
    except werkzeug.exceptions.Unauthorized as e:
        abort(401, description=str(e))


@app.route('/split_pdf', methods=['POST'])
def split_pdf():
    try:
        check_credentials()
        pdf = request.files.get('pdf')
        return controller.split_pdf(pdf, app.root_path)
    except werkzeug.exceptions.Unauthorized as e:
        abort(401, description=str(e))

@app.route('/download_pdf', methods=['GET'])
def download_pdf():
    check_credentials()
    return controller.download_pdf(app.root_path)

@app.route('/extract_text', methods=['POST'])
def extract_text():
    check_credentials()
    try:
        check_credentials()
        pdf = request.files.get('pdf')
        return controller.extract_text_from_pdf(pdf)
    except Exception as e:
        return {'status': 'error', 'message': e}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
