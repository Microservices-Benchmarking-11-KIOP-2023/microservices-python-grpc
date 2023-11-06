FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /geo

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY services/geo .

CMD ["python", "main.py"]