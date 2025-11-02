FROM python:3.9-slim
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    fonts-liberation \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdrm2 \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Download Chrome for Testing (adjust version as needed)
ENV CHROME_VERSION=138.0.7204.184
RUN wget -O /tmp/chrome-linux.zip https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROME_VERSION}/linux64/chrome-linux64.zip && \
    unzip /tmp/chrome-linux.zip -d /opt && \
    ln -s /opt/chrome-linux64/chrome /usr/bin/google-chrome && \
    rm /tmp/chrome-linux.zip

# Download ChromeDriver for Testing (matching version)
RUN wget -O /tmp/chromedriver-linux.zip https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROME_VERSION}/linux64/chromedriver-linux64.zip && \
    unzip /tmp/chromedriver-linux.zip -d /opt && \
    ln -s /opt/chromedriver-linux64/chromedriver /usr/bin/chromedriver && \
    rm /tmp/chromedriver-linux.zip

COPY . .

RUN pip install -r requirements.txt

# Normalize line endings and make script executable (fixes "no such file or directory" if CRLF snuck in)
RUN sed -i 's/\r$//' start_bots.sh && chmod +x start_bots.sh

ENV ADMIN_PASSWORD=expanse-overbite-tibia-refund-grafting-galore
ENV JOURNALIST_PASSWORD=tubby-obituary-superman-shorten-activism-myself

CMD ["./start_bots.sh"]
