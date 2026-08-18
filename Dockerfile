# Image Python légère
FROM python:3.10-slim

# Répertoire de travail
WORKDIR /app

# Installation des dépendances système nécessaires pour psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du script
COPY main.py .

# Commande de lancement
CMD ["python", "main.py"]
