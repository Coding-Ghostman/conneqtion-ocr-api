from ocr_processor import extract_data_, pdf2png_extract
from base64 import b64decode
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from ai_formatter.format_main import format_changer


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
        return extracted_data
    except Exception as e:
        print(e)
        return {"error": f"An error occurred while processing the file: {e}"}
    
  
@app.post("/api/conneqtion/convert/pdf/png")
async def upload_file_pdf_png(request: Request):
    data = await request.json()
    try:
        if 'file'not in data:
            return {'error': 'No file part in JSON payload'}
        pdf_data = b64decode(data['file'])
        extracted_data = pdf2png_extract(pdf_data)
        # return FileResponse(extracted_data)
        return {"image":extracted_data}
    except Exception as e:
        print(e)
        return {"error": f"An error occurred while processing the file: {e}"}
    
@app.post("/api/conneqtion/ai/updater")
async def change_data(request: Request):
    data = await request.json()
    try:
        requested_delivery_date, need_identification_date, actual_or_estimated = format_changer(data["requested_delivery_date"], data["need_identification_date"], data["actual_or_estimated"])
        return {"requested_delivery_date" : requested_delivery_date, 
                "need_identification_date" : need_identification_date,
                "actual_or_estimated" : actual_or_estimated}
    except Exception as e:
        print(e)
        return {"warning": "Issue a proper format please"}
    
