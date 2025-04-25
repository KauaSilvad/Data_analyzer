import json
import os

from .file_handler import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_text_from_pptx,
    extract_text_from_html,
    convert_to_markdown
)

def convert_file_to_json_and_md(path, ext, file_id):
    # 1. Extrair conteúdo bruto do arquivo
    if ext == "pdf":
        text, estrutura = extract_text_from_pdf(path)
    elif ext == "docx":
        text, estrutura = extract_text_from_docx(path)
    elif ext == "pptx":
        text, estrutura = extract_text_from_pptx(path)
    elif ext == "html":
        text, estrutura = extract_text_from_html(path)
    else:
        raise ValueError("Extensão de arquivo não suportada.")

    # 2. Salvar JSON
    json_data = {
        "id": file_id,
        "tipo": ext,
        "texto": text,
        "estrutura": estrutura
    }

    json_path = os.path.join("output", f"{file_id}.json")
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, indent=4, ensure_ascii=False)

    # 3. Converter para Markdown
    markdown_text = convert_to_markdown(text)
    md_path = os.path.join("output", f"{file_id}.md")
    with open(md_path, "w", encoding="utf-8") as md_file:
        md_file.write(markdown_text)

    return json_path, md_path
