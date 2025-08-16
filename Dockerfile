FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies, Chromium, and Firefox
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    firefox-esr \
    wget \
    unzip \
    curl \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk1.0-0 \
    libcups2 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Install Geckodriver (for Firefox)
RUN GECKO_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest \
    | grep '"tag_name":' | sed -E 's/.*"v([^"]+)".*/\1/') \
    && wget -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v$GECKO_VERSION/geckodriver-v$GECKO_VERSION-linux64.tar.gz \
    && tar -xzf /tmp/geckodriver.tar.gz -C /usr/local/bin \
    && rm /tmp/geckodriver.tar.gz

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run main script using Xvfb for virtual display
CMD ["python", "Utilities/common.py"]

