from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import JSONResponse
import os
import shutil
from datetime import datetime

transfer_router = APIRouter()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@transfer_router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return JSONResponse(content={"status": "success", "file_url": f"/files/{filename}", "filename": filename})
