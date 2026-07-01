FROM python:3.12-slim

WORKDIR /app

# Install uv for faster dependency management
COPY pyproject.toml requirements.txt ./
RUN pip install uv && uv pip install -r requirements.txt

# Copy application code
COPY ./app ./app

# Create logs directory
RUN mkdir -p logs

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
