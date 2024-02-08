from typing import Dict
import io
from io import BytesIO
import PyPDF2
import uuid
import os
from PyPDF2 import PdfReader, PdfWriter
from flask import jsonify

class Controller:
    def join_pdf(self, pdf_bytes) -> Dict:
        pdf_merger = PyPDF2.PdfMerger()
        
        for pdf in pdf_bytes:
            pdf_file = PyPDF2.PdfReader(io.BytesIO(pdf))
            pdf_merger.append(pdf_file)
            
        uid = str(uuid.uuid1())
        path = uid + '.pdf'
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

            # Itera sobre cada página do PDF e salva como um novo arquivo
            for page_number in range(len(pdf_reader.pages)):
                # Cria um escritor de PDF para a página atual
                pdf_writer = PdfWriter()
                pdf_writer.add_page(pdf_reader.pages[page_number])

                # Salva o PDF dividido localmente
                output_filepath = os.path.join(output_directory, f'{uid}_page_{page_number + 1}.pdf')
                output_files.append(f'{uid}_page_{page_number + 1}.pdf')
                with open(output_filepath, 'wb') as output_file:
                    pdf_writer.write(output_file)

            return jsonify({'status': 'success', 'message': 'PDF dividido e salvo com sucesso', "files": output_files})

        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
