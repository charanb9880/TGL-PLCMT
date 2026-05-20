FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies and explicitly upgrade fastapi to fix the Router TypeError
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --upgrade fastapi==0.111.0 uvicorn pydantic

# Copy application files
COPY . .

# Expose port
EXPOSE 8000

# Command to run the backend server
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
