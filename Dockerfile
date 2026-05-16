FROM python:3.12-slim

WORKDIR /app

COPY backend/pyproject.toml backend/uv.lock ./

RUN pip install uv
RUN uv pip install --system .

COPY backend/ .
COPY frontend /app/frontend

# Copy and setup entrypoint
COPY backend/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]