# Utiliser une image de base légère et sécurisée
FROM python:3.11-slim

# Créer un utilisateur non-root
RUN adduser --disabled-password --gecos '' appuser

# Définir le répertoire de travail
WORKDIR /home/appuser

# Copier les fichiers nécessaires
COPY ./Part1/extract_link_sleep.py .
COPY requirements.txt .
# Installer les dépendances avec sécurité
RUN pip install --no-cache-dir -r requirements.txt

# Donner la propriété des fichiers à l'utilisateur non-root
RUN chown -R appuser:appuser /home/appuser

# Passer à l'utilisateur non-root
USER appuser

# Lancer le script avec des arguments (entrypoint modifiable dynamiquement)
ENTRYPOINT ["python", "extract_link_sleep.py"]
