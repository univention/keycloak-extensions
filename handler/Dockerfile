FROM python:3.8-slim-buster
WORKDIR /usr/app/src
COPY *.py ./
COPY requirements.txt ./
RUN apt update
RUN apt install -y git
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
CMD [ "bash", "-c", "sleep 30 && python main.py --realm $KC_REALM --kc-admin-auth-url $KC_AUTH_URL --mail-pass $MAIL_PASS --mail-user $MAIL_USER --admin-mail $ADMIN_MAIL --mail-server $MAIL_SERVER --kc-admin-user $KC_USER --kc-admin-pass $KC_PASS --kc-proxy $KC_PROXY --udm-rest-base-url $UDM_REST_BASE_URL --udm-rest-user $UDM_REST_USER --udm-rest-password $UDM_REST_PASSWORD"]
