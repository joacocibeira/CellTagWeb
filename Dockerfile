# Use Python 3.12 slim image
FROM python:3.12-slim

# Set environment variables
ENV POETRY_VERSION=1.8.2 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock /app/

# Install dependencies directly into system Python (no venv)
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi

# Copy the full app
COPY . /app

# Set PYTHONPATH to make `from app...` imports work
ENV PYTHONPATH=/app

# Disable Streamlit usage tracking
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Expose Streamlit port
EXPOSE 8501

# Start the app
CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]