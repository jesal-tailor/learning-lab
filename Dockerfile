# Lightweight Python base
FROM python:3.11-slim

# Prevents Python from writing .pyc files and buffers
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (better caching)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src /app/src
COPY pytest.ini /app/pytest.ini

# Default command (can be overridden)
CMD ["python", "src/learning_lab/summarise_csv.py", "--help"]

