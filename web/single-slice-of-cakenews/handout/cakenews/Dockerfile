# Dockerfile for web - Single Sign On Problems
FROM python:3.9-slim
WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV CAKENEWS_SECRET=secret_development_key

CMD ["python", "app.py"]
