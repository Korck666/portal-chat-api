# routers/file_man.py
import asyncio
from fastapi import APIRouter
from utils import config
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi import UploadFile, HTTPException
from typing import List
import os
from utils import config

router = APIRouter()

router.mount(f"{config.WORKDIR}/upload",
             StaticFiles(directory="upload"), name="upload")


async def save_file(file: UploadFile):
    if file.filename.endswith('.pdf'):
        with open(f"{config.WORKDIR}/upload/{file.filename}", "wb") as buffer:
            while True:
                # TODO: Add error handling, if chunk is too big, we can ajust the chunk size dinamically
                # TODO: Add a progress bar
                # TODO: Add error recovery retries
                chunk = await file.read(config.FILE_CHUNCK[config.DEFAULT_FILE_CHUNCK_INDEX])
                if not chunk:  # End of file
                    break
                buffer.write(chunk)
    else:
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only PDFs are accepted.")


@router.get("/list_pdfs/")
def list_files():
    files = os.listdir(f"{config.WORKDIR}/upload")
    return JSONResponse(status_code=200, content={"files": files})


@router.get("/download_pdfs/{file_name}")
async def download_file(file_name: str):
    path = f"{config.WORKDIR}/upload/"
    if os.path.exists(f"{path}{file_name}"):
        return FileResponse(path=f"{path}{file_name}",
                            status_code=200,
                            filename=file_name,
                            media_type="application/pdf",
                            content_disposition_type="attachment")
    raise HTTPException(status_code=404, detail="File not found.")


@router.post("/upload_pdfs/")
async def upload_files(files: List[UploadFile] = []):
    tasks = []
    for file in files:
        tasks.append(asyncio.ensure_future(save_file(file)))
    await asyncio.gather(*tasks)
    return JSONResponse(status_code=200, content={"message": "Files uploaded successfully."})
