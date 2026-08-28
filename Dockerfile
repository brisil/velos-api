# Étape 1 : Builder
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Étape 2 : Image finale non-root
FROM python:3.11-slim
WORKDIR /app
RUN groupadd -r appuser && useradd -r -g appuser appuser
COPY --from=builder /root/.local /home/appuser/.local
COPY app.py .
ENV PATH=/home/appuser/.local/bin:$PATH
USER appuser

EXPOSE 8000
CMD ["python", "app.py"]
