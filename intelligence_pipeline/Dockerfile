FROM python:3.11-slim

WORKDIR /app

# Copy the requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Ensure FastAPI and Uvicorn are installed since they might not be in the original requirements
RUN pip install --no-cache-dir fastapi uvicorn pydantic

# Copy the rest of the app
COPY . .

# Expose port
EXPOSE 8001

# Command to run the agent backend
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
