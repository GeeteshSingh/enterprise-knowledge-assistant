# Stage 1: Builder — install dependencies
FROM python:3.13-slim AS builder

WORKDIR /app

# Install dependencies in a separate layer for caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime — copy application code only
FROM python:3.13-slim AS runtime

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application source code
COPY config/ ./config/
COPY src/ ./src/
COPY utils/ ./utils/
COPY data/ ./data/

# Create directories for logs and FAISS index
RUN mkdir -p logs index

# The .env file is not copied into the image.
# Pass GEMINI_API_KEY as an environment variable at runtime:
# docker run -e GEMINI_API_KEY=your_key ...

EXPOSE 8000

# Run the FastAPI server with uvicorn
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
