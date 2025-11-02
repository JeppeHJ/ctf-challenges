FROM python:3.9-slim
WORKDIR /app

# Install Chromium browser and the matching driver
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install -r requirements.txt

# Normalize line endings and make script executable (fixes "no such file or directory" if CRLF snuck in)
RUN sed -i 's/\r$//' start_bots.sh && chmod +x start_bots.sh

ENV ADMIN_PASSWORD=secret_admin_password
ENV JOURNALIST_PASSWORD=secret_journalist_password

CMD ["./start_bots.sh"]
