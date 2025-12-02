# --- Build Stage ---
# Use a full Python image to build dependencies, keeping the final image slim.
FROM python:3.11-slim AS builder

# Set the working directory
WORKDIR /usr/src/app

# Install build tools
RUN apt-get update && apt-get install -y build-essential

# Copy requirements file and install dependencies into a virtual environment
COPY requirements.txt ./
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# --- Final Stage ---
# Use a minimal Python image for the final container
FROM python:3.11-slim

# Set the working directory
WORKDIR /usr/src/app

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy the application source code
COPY server.py ./

# Make port 8765 available to the world outside this container
EXPOSE 8765

# Define environment variable for the python path
ENV PATH="/opt/venv/bin:$PATH"

# Run the application
CMD ["python", "server.py"]
