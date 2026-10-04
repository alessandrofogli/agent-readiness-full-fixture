FROM python:3.12-slim

WORKDIR /app

COPY packages/api /app/packages/api
RUN pip install --no-cache-dir /app/packages/api

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
