FROM python:3.11-slim

WORKDIR /app

# Copy dependency map
COPY pyproject.toml .

# Install dependencies parsing the toml
RUN pip install --no-cache-dir .

# Copy application layer
COPY app /app/app

# Create upload spooling directory
RUN mkdir -p uploads

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
