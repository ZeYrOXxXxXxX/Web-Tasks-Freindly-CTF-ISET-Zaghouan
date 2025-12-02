# Use a slim and secure base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the challenge directory into the container at /app
COPY ./challenge/ .

# Install Flask, Gunicorn, and a version of Werkzeug known to be compatible with Flask 2.2.2
# This is the corrected line to fix the pip installation failure.
RUN pip install --no-cache-dir Flask==2.2.2 gunicorn==20.1.0 Werkzeug==2.2.2

# --- Security Best Practices ---
# Create a non-root user to run the application
RUN useradd --no-create-home ctf

# Switch to the non-root user
USER ctf

# Expose the port the app runs on
EXPOSE 5000

# The command to run when the container starts
# Use gunicorn to run the app with 4 worker processes
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]