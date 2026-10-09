# ZbxView push relay

Files for push notifications through your own Firebase project. The step by
step guide is at https://radekpavlik.github.io/zbxview/#push.

- `push_relay.py` - small Python service: receives the Zabbix webhook, sends
  to Firebase Cloud Messaging (HTTP v1) with the project's service account.
- `config.ini.example` - copy to `config.ini` (listen address, port, shared
  secret, path to `service-account.json`).
- `zbxview-push-relay.service` - systemd unit (runs as the `zabbix` user,
  Python from `/opt/zbxview-push-relay/venv`).
- `media_type_zbxview_push.yaml` - the Zabbix media type "ZbxView Push",
  importable (Alerting → Media types → Import); set `Auth` to the shared
  secret afterwards.
- `media_type_script.js` - the same webhook script for a manual set-up.

The app registers the phone's token as the user's "ZbxView Push" media by
itself; an action "Send message to users via ZbxView Push" delivers problems.
