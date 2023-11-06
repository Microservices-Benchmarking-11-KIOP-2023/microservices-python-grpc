FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /gateway

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY services/gateway .

EXPOSE 8080

CMD ["python", "main.py"]