FROM python:3.9-slim
WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV BRUNNERNELOGIN_SECRET=secret_development_key
ENV ADMIN_PASSWORD=secret_admin_password
ENV JOURNALIST_PASSWORD=secret_journalist_password
ENV FLAG=brunner{REDACTED}

CMD ["python", "app.py"]
