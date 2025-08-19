# Dockerfile
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install pip packages
RUN pip install --no-cache-dir simple-salesforce

# Set default working directory
WORKDIR /app

# Entrypoint to run scripts passed from host
ENTRYPOINT ["python"]
