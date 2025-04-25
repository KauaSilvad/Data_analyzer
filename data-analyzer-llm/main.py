from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
from utils.converters import convert_file_to_json_and_md

app = FastAPI()

# Liberar acesso de outros domínios (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "output"

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename
    ext = filename.split(".")[-1].lower()

    # Verifica se a extensão é suportada
    if ext not in ["pdf", "docx", "pptx", "html"]:
        raise HTTPException(status_code=400, detail="Tipo de arquivo não suportado.")

    # Nome temporário único
    file_id = str(uuid.uuid4())
    temp_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.{ext}")

    # Salva o arquivo no servidor
    with open(temp_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Converte o conteúdo
    json_path, md_path = convert_file_to_json_and_md(temp_path, ext, file_id)

    return {
        "message": "Arquivo processado com sucesso.",
        "json_download_url": f"/download/json/{file_id}",
        "markdown_download_url": f"/download/markdown/{file_id}"
    }

@app.get("/download/json/{file_id}")
async def download_json(file_id: str):
    path = os.path.join(UPLOAD_FOLDER, f"{file_id}.json")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Arquivo JSON não encontrado.")
    return FileResponse(path, media_type='application/json', filename=f"{file_id}.json")

@app.get("/download/markdown/{file_id}")
async def download_markdown(file_id: str):
    path = os.path.join(UPLOAD_FOLDER, f"{file_id}.md")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Arquivo Markdown não encontrado.")
    return FileResponse(path, media_type='text/markdown', filename=f"{file_id}.md")
