from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import subprocess
import os
import uuid
import shutil
from pathlib import Path

app = FastAPI(title="LibreOffice Converter API")

# Configuración
ALLOWED_EXTENSIONS = {'.doc', '.rtf', '.odt', '.xls'}
OUTPUT_DIR = Path("/tmp/conversions")
OUTPUT_DIR.mkdir(exist_ok=True)

def allowed_file(filename: str) -> bool:
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS

@app.post("/convert")
async def convert_to_pdf(file: UploadFile = File(...)):
    """
    Convierte un documento a PDF usando LibreOffice
    """
    # Validar extensión
    if not allowed_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"Formato no permitido. Permite: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Crear directorio de trabajo único
    work_dir = OUTPUT_DIR / str(uuid.uuid4())
    work_dir.mkdir(exist_ok=True)
    
    try:
        # Guardar archivo de entrada
        input_path = work_dir / file.filename
        with open(input_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Nombre del archivo de salida (mismo nombre, extensión pdf)
        output_filename = input_path.stem + ".pdf"
        output_path = work_dir / output_filename
        
        # Convertir con LibreOffice (headless)
        # --headless: sin interfaz gráfica
        # --convert-to pdf: convierte a PDF
        # --outdir: directorio de salida
        result = subprocess.run([
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(work_dir),
            str(input_path)
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail=f"Error en conversión: {result.stderr}"
            )
        
        if not output_path.exists():
            raise HTTPException(
                status_code=500,
                detail="LibreOffice no generó el archivo PDF"
            )
        
        # Copiar a una ubicación permanente antes de retornar
        # (FileResponse no bloquea, así que necesitamos el archivo fuera del dir temporal)
        final_path = OUTPUT_DIR / f"{uuid.uuid4()}_{output_filename}"
        shutil.copy2(output_path, final_path)
        
        # Limpiar directorio de trabajo ahora
        if work_dir.exists():
            shutil.rmtree(work_dir)
        
        return FileResponse(
            path=final_path,
            filename=output_filename,
            media_type="application/pdf"
        )
        
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=500, detail="Tiempo de conversión agotado")
    except Exception as e:
        # Limpiar en caso de error
        if work_dir.exists():
            shutil.rmtree(work_dir)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)