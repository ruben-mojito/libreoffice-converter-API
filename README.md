# LibreOffice Converter API

API para convertir documentos a PDF usando LibreOffice.

## Formatos soportados

- `.doc` - Microsoft Word
- `.rtf` - Rich Text Format
- `.odt` - OpenDocument Text
- `.xls` - Microsoft Excel

## Uso con Docker

```bash
# Clonar el repositorio
git clone https://github.com/ruben-mojito/libreoffice-converter-API.git
cd libreoffice-converter-API

# Construir y ejecutar
docker-compose up --build

# En background
docker-compose up --build -d
```

## Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/convert` | Convierte un archivo a PDF |
| GET | `/health` | Health check |

## Ejemplos

### Convertir un archivo

```bash
curl -X POST -F "file=@documento.doc" http://localhost:8000/convert -o resultado.pdf
```

Con otros formatos:
```bash
curl -X POST -F "file=@documento.rtf" http://localhost:8000/convert -o resultado.pdf
curl -X POST -F "file=@documento.odt" http://localhost:8000/convert -o resultado.pdf
curl -X POST -F "file=@spreadsheet.xls" http://localhost:8000/convert -o resultado.pdf
```

### Health check

```bash
curl http://localhost:8000/health
```

Respuesta: `{"status":"healthy"}`

## Desarrollo local (sin Docker)

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python3 app.py
```

## Notas

- La API convierte archivos usando LibreOffice en modo headless
- Timeout de conversión: 120 segundos
- Los archivos temporales se limpian automáticamente después de cada conversión