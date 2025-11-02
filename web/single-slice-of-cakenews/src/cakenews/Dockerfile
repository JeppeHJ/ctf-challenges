# Dockerfile for web - Single Sign On Problems
FROM python:3.9
WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV CAKENEWS_SECRET=cubical-fidelity-reveler-refusal-decree-ride

CMD ["python", "app.py"]
