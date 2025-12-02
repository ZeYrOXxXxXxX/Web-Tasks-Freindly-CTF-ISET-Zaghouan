# Utiliser une image Python légère
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les dépendances et les installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier uniquement les fichiers nécessaires de l'application
COPY app.py ./
COPY templates ./templates
COPY static ./static
COPY internal_memos ./internal_memos

# Créer l'utilisateur non-root pour la sécurité et ajuster les permissions
RUN useradd --no-create-home appuser && chown -R appuser:appuser /app
USER appuser

# Exposer le port et lancer l'application
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
