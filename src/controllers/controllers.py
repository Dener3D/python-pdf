from typing import Dict
import io
from io import BytesIO
import PyPDF2
import uuid

url = 'https://pacific-earth-60757-12860c7b633c.herokuapp.com/'

class Controller:
    def join_pdf(self, pdf_bytes) -> Dict:
        pdf_merger = PyPDF2.PdfMerger()
        
        for pdf in pdf_bytes:
            pdf_file = PyPDF2.PdfReader(io.BytesIO(pdf))
            pdf_merger.append(pdf_file)
            
        uid = str(uuid.uuid1())
        path = url + '/merged_files/' + uid + '.pdf'
        
        with open(path, 'wb') as output_file:
            pdf_merger.write(output_file)
        
        return {"path": path}