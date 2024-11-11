FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /app/venv ./venv
COPY app app

EXPOSE 8000
CMD ["venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
