FROM gitregistry.knut.univention.de/univention/customers/dataport/upx/container-ucs-base/ucs-base-505:v0.6.0

COPY . /app
WORKDIR /app

RUN apt update \
    && apt -y install nodejs npm \
    && npm install \
    && rm -fr /var/lib/apt/lists/* /var/cache/apt/archives/*

ENV PORT 8181
EXPOSE 8181

CMD ["nodejs", "app.js"]
