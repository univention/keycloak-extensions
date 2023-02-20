FROM mcr.microsoft.com/playwright/python:v1.30.0-focal as build
WORKDIR /e2e/
COPY ./requirements_test.txt .
RUN pip install --no-cache-dir -r requirements_test.txt && playwright install --with-deps

FROM build as test
WORKDIR /e2e/
COPY . .
CMD ["pytest"]
