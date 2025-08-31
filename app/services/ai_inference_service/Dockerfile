# Base image with uv (fast dependency resolver/installer)
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

# Install dependencies using uv
COPY pyproject.toml requirements.txt* ./
RUN uv pip install --system --no-cache -r requirements.txt

# Copy source code
COPY src ./src

# Models will be mounted at runtime
VOLUME ["/models"]

EXPOSE 8000

# Run the FastAPI app with uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
