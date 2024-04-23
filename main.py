from ocr_processor import extract_data_
from base64 import b64decode
from fastapi import FastAPI, HTTPException, Request
from logger import setup_logger

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app = FastAPI()

@app.post("/api/conneqtion/upload/scanned")
async def upload_file(request: Request):
    data = await request.json()
    try:
        if 'file'not in data:
            return {'error': 'No file part in JSON payload'}
        pdf_data = b64decode(data['file'])
        extracted_data = extract_data_(pdf_data)
        if "Requestor(s) Name" not in extracted_data:
            extracted_data['Requestor(s) Name'] = extracted_data["Requestor_s_Name"]
            del extracted_data["Requestor_s_Name"]
            
        return extracted_data
    except Exception as e:
        logger = setup_logger()
        logger.error(f"Error: " + str(e))
        return {'error': f'An error occurred while processing the file: {e}'}