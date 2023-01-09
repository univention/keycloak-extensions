FROM node:lts-alpine3.15

COPY . /app
WORKDIR /app

RUN npm install

ENV PORT 8181
EXPOSE 8181

CMD ["nodejs", "app.js"]
