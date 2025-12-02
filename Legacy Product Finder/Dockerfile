# 1. Use a slim, secure Python base image
FROM python:3.9-slim

# 2. Set the working directory
WORKDIR /app

# 3. Create a non-root user for security
RUN useradd --create-home appuser

# 4. Copy and install dependencies from requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application code
COPY ./app .

# 6. Switch to the non-root user
USER appuser

# 7. Add the user's local bin directory to the PATH to find gunicorn
ENV PATH="/home/appuser/.local/bin:${PATH}"

# 8. Expose the port the application will run on
EXPOSE 8000

# 9. Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
