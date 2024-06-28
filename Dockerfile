FROM python:3.11.4-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt ./

# Install Python dependencies (requirements are pinned in requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

EXPOSE 8000

# Default run command (development). Replace with gunicorn in production.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
