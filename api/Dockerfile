FROM ubuntu:22.04

EXPOSE 8000

RUN apt-get update && apt-get install -y python3.10 python3-pip

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt .
RUN python3 -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

CMD ["gunicorn", "-c", "gunicon.conf.py", "app:app"]