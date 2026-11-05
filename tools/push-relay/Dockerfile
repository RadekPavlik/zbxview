# ZbxView push relay as a container, for a Zabbix server that runs in Docker.
# config.ini and service-account.json are not in the image: docker-compose.yml
# mounts them read-only. See https://radekpavlik.github.io/zbxview/push.html#docker
FROM python:3.12-slim
RUN pip install --no-cache-dir firebase-admin \
    && useradd --system --uid 10001 --no-create-home --shell /usr/sbin/nologin relay
COPY push_relay.py /opt/zbxview-push-relay/push_relay.py
USER 10001
CMD ["python3", "-u", "/opt/zbxview-push-relay/push_relay.py"]
