FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies first (layer caching)
COPY ./src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./src/main.py .
COPY ./src/templates/ templates/
COPY ./src/static/ static/

# Expose port
EXPOSE 8000

# Run with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]