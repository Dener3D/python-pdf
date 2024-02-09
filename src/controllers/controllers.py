from typing import Dict
import io
from io import BytesIO
import PyPDF2
import uuid
import os
from PyPDF2 import PdfReader, PdfWriter
from flask import jsonify, request, send_file
from datetime import datetime
import re

class Controller:
    def download_pdf(self, root_path):
        filename = request.args.get('filename')
        now = datetime.now().date()
        # Caminho para o arquivo PDF salvo localmente
        filepath = os.path.join(root_path, 'files/'+ str(now) + "/" + filename)
        # Verifica se o arquivo existe
        if os.path.exists(filepath):
            #with open(filepath, 'rb') as file:
            response = send_file(filepath, as_attachment=True, mimetype='application/pdf', download_name='merged_file.pdf')
            # Remove o arquivo após o download
            return response
        else:
            return {'status': 'error', 'message': 'File not found'}
    # Deletar os pdfs na origem do projeto
    def delete_pdfs(self, root_path) -> Dict:
        try:
            now = datetime.now().date()
            # Diretório raiz do projeto
            root_directory = root_path + "/files/" + str(now)

            # Obtém a lista de arquivos na raiz do projeto
            files_in_root = os.listdir(root_directory)

            # Filtra apenas os arquivos PDF
            pdf_files = [file for file in files_in_root if file.endswith('.pdf')]
            
            # Exclui cada arquivo PDF encontrado
            for pdf_file in pdf_files:
                pdf_filepath = os.path.join(root_directory, pdf_file)
                os.remove(pdf_filepath)
        

            return {'status': 'success', 'message': 'Files successfully deleted'}

        except Exception as e:
            return {'status': 'error', 'message': str(e)}
        
    def join_pdf(self, pdf_bytes) -> Dict:
        pdf_merger = PyPDF2.PdfMerger()
        
        for pdf in pdf_bytes:
            pdf_file = PyPDF2.PdfReader(io.BytesIO(pdf))
            pdf_merger.append(pdf_file)
            
        now = datetime.now().date()
        
        # Cria uma nova pasta
        try:
            os.mkdir("files/" + str(now))
        except FileExistsError:
            pass
        except Exception as e:
            print(f'There was an error trying to create the folder: {e}')
        
        
        uid = str(uuid.uuid1())
        path = uid +'.pdf'
        
        
        with open("files/" + str(now) + "/" + path, 'wb') as output_file:
            pdf_merger.write(output_file)
            
        return {"path": path}
    
    def split_pdf(self, pdf, root_path) -> Dict:
        output_files = []
        try:
            # Obtém o arquivo PDF em bytes do corpo da requisição
            pdf_bytes = pdf.read()

            # Cria um leitor de PDF a partir dos bytes recebidos
            pdf_reader = PdfReader(io.BytesIO(pdf_bytes))

            # Diretório onde os PDFs divididos serão salvos
            output_directory = root_path  # Pode ser ajustado conforme necessário
            
            uid = str(uuid.uuid1())
            
            now = datetime.now().date()
            
            try:
                os.mkdir("files/" + str(now))
            except FileExistsError:
                pass
            except Exception as e:
                print(f'There was an error trying to create the folder: {e}')

            # Itera sobre cada página do PDF e salva como um novo arquivo
            for page_number in range(len(pdf_reader.pages)):
                # Cria um escritor de PDF para a página atual
                pdf_writer = PdfWriter()
                pdf_writer.add_page(pdf_reader.pages[page_number])

                # Salva o PDF dividido localmente
                output_filepath = os.path.join(output_directory, f'files/{str(now)}/{uid}_page_{page_number + 1}.pdf')
                output_files.append(f'{uid}_page_{page_number + 1}.pdf')
                with open(output_filepath, 'wb') as output_file:
                    pdf_writer.write(output_file)

            return jsonify({'status': 'success', 'message': 'PDF successfully splited', "files": output_files})

        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})

    def extract_text_from_pdf(self, pdf) -> Dict:
        pdf_bytes = pdf.read()
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + ",\n"
            
        return {'status': 'success', 'extracted_text': text.replace('\n', ' ')}
                