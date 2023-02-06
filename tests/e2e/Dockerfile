FROM mcr.microsoft.com/playwright/python:v1.30.0-focal
WORKDIR /e2e/
COPY . .
RUN pip install --no-cache-dir -r requirements.txt && playwright install --with-deps
CMD ["pytest", "--base-url", "$PROXY_BASE_URL"]