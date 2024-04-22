from ocr_processor import extract_data_
from base64 import b64decode
from fastapi import FastAPI, HTTPException, Request
from logger import setup_logger

app = FastAPI()

@app.post("/api/conneqtion/upload/scanned")
async def upload_file(request: Request):
    data = await request.json()
    try:
        if 'file'not in data:
            return {'error': 'No file part in JSON payload'}
        pdf_data = b64decode(data['file'])
        extracted_data = extract_data_(pdf_data)
        return extracted_data
    except Exception as e:
        logger = setup_logger()
        logger.error(f"Error: " + e)