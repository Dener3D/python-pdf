from typing import Dict
import io
from io import BytesIO
import PyPDF2
import uuid
import os
from PyPDF2 import PdfReader, PdfWriter
from flask import jsonify
from datetime import datetime
import re

class Controller:
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
        

            return {'status': 'success', 'message': 'Arquivos PDF excluídos com sucesso'}

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
            print(f'Ocorreu um erro ao criar a pasta: {e}')
        
        
        uid = str(uuid.uuid1())
        path = "files/" + str(now) + "/" + uid +'.pdf'
        
        with open(path, 'wb') as output_file:
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
                print(f'Ocorreu um erro ao criar a pasta: {e}')

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

            return jsonify({'status': 'success', 'message': 'PDF dividido e salvo com sucesso', "files": output_files})

        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
