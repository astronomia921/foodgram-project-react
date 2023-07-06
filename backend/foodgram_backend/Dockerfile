FROM python:3.10-slim

RUN apt-get update && apt-get install -y libgirepository1.0-dev libpango1.0-dev

WORKDIR /app

RUN pip install gunicorn==20.1.0

COPY requirements.txt ./

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "foodgram_backend.wsgi"]
