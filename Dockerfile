FROM python:3.10-slim

WORKDIR /app

# Installer les dépendances
COPY requirements.txt .
RUN pip install --default-timeout=200 --retries 10 --no-cache-dir -r requirements.txt

# Copier l'application
COPY . .

# Variable d'environnement pour Docker
ENV DOCKER_ENV=true
ENV FLASK_APP=app.py

EXPOSE 5000

CMD ["python", "app.py"]