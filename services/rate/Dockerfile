FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /rate

RUN apt-get update && apt-get install -y unzip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY services/rate/data/inventory.zip .

RUN unzip inventory.zip -d data

COPY services/rate .

CMD ["python", "main.py"]