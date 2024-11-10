FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends netcat-traditional


WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY consumer.py .
COPY wait-for-rabbitmq.sh .
RUN chmod +x wait-for-rabbitmq.sh

CMD ["./wait-for-rabbitmq.sh", "rabbitmq", "python", "consumer.py"]
