FROM ubuntu:22.04

# Evitar interactivos en instalación
ENV DEBIAN_FRONTEND=noninteractive

# Instalar LibreOffice y Python
RUN apt-get update && apt-get install -y \
    libreoffice \
    python3 \
    python3-pip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar Python packages
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Crear directorio de trabajo
WORKDIR /app
COPY app.py .

# Puerto para FastAPI
EXPOSE 8000

CMD ["python3", "app.py"]