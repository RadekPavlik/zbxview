#!/usr/bin/env python3
"""ZbxView push relay.

Receives problem/recovery events from the Zabbix "ZbxView Push" webhook media
type and forwards them to Firebase Cloud Messaging (HTTP v1). A relay is needed
because FCM v1 requires an OAuth2 token signed (RS256) from the service account,
which the Zabbix webhook JS cannot mint.

The token travels with the alert ({ALERT.SENDTO}) — variant A — so the relay
does no token lookup: it just sends to the token it receives.

Config: config.ini next to this file (chmod 600). Deps: firebase-admin
(`pip3 install firebase-admin`).
"""
import configparser
import json
import logging
import pathlib
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import firebase_admin
from firebase_admin import credentials, messaging

log = logging.getLogger('push-relay')

# Zabbix severity colours (Administration → General → Trigger displaying options, defaults),
# keyed by {EVENT.SEVERITY} as the server sends it - the English names and the Czech ones.
SEVERITY_COLORS = {
    'not classified': '#97AAB3', 'nezařazeno': '#97AAB3',
    'information': '#7499FF', 'informace': '#7499FF',
    'warning': '#FFC859', 'varování': '#FFC859',
    'average': '#FFA059', 'průměrná': '#FFA059',
    'high': '#E97659', 'vysoká': '#E97659',
    'disaster': '#E45959', 'katastrofa': '#E45959',
}
UPDATE_COLOR = '#7499FF'
RESOLVED_COLOR = '#59DB8F'
UPDATE_PREFIXES = ('aktualizace', 'update', 'updated')
RESOLVED_PREFIXES = ('vyřešeno', 'resolved')


def notification_style(title, data):
    """(kind, icon, colour) of an alert for the Android notification: the app ships
    ic_stat_problem / ic_stat_update / ic_stat_resolved. An update is data "update" = "1"
    ({EVENT.UPDATE.STATUS}) or a subject starting "Aktualizace:" / "Update:" (the media
    type's update template); resolved is status RESOLVED or "Vyřešeno:" / "Resolved:"."""
    head = title.strip().lower()
    status = str(data.get('status') or '').strip().upper()
    if status == 'RESOLVED' or head.startswith(RESOLVED_PREFIXES):
        return 'resolved', 'ic_stat_resolved', RESOLVED_COLOR
    if str(data.get('update') or '') == '1' or head.startswith(UPDATE_PREFIXES):
        return 'update', 'ic_stat_update', UPDATE_COLOR
    color = SEVERITY_COLORS.get(str(data.get('severity') or '').strip().lower(), SEVERITY_COLORS['warning'])
    return 'problem', 'ic_stat_problem', color


def load_config():
    cfg = configparser.ConfigParser()
    path = pathlib.Path(__file__).with_name('config.ini')
    if not cfg.read(path):
        log.error('config.ini not found next to %s', __file__)
        sys.exit(1)
    return cfg['relay']


class Handler(BaseHTTPRequestHandler):
    secret = ''

    def _reply(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path.rstrip('/') != '/send':
            return self._reply(404, {'ok': False, 'error': 'not found'})
        if self.headers.get('X-Auth', '') != self.secret:
            return self._reply(401, {'ok': False, 'error': 'unauthorized'})
        try:
            n = int(self.headers.get('Content-Length', '0'))
            payload = json.loads(self.rfile.read(n) or b'{}')
        except Exception as e:  # noqa: BLE001
            return self._reply(400, {'ok': False, 'error': 'bad json: %s' % e})

        token = str(payload.get('token') or '').strip()
        if not token:
            return self._reply(400, {'ok': False, 'error': 'missing token'})
        # FCM data values must be strings.
        data = {k: str(v) for k, v in (payload.get('data') or {}).items()}
        title = str(payload.get('title') or 'Zabbix')
        kind, icon, color = notification_style(title, data)
        data['kind'] = kind
        msg = messaging.Message(
            token=token,
            notification=messaging.Notification(
                title=title,
                body=str(payload.get('body') or ''),
            ),
            data=data,
            # Older app builds lack the icons: Android then falls back to the app's default.
            android=messaging.AndroidConfig(
                priority='high',
                notification=messaging.AndroidNotification(icon=icon, color=color),
            ),
        )
        try:
            mid = messaging.send(msg)
            log.info('sent %s to %s…', mid, token[:12])
            return self._reply(200, {'ok': True, 'id': mid})
        except messaging.UnregisteredError:
            # Token no longer valid — 410 lets Zabbix flag it for cleanup.
            log.warning('token unregistered: %s…', token[:12])
            return self._reply(410, {'ok': False, 'error': 'unregistered'})
        except Exception as e:  # noqa: BLE001
            log.error('send failed: %s', e)
            return self._reply(502, {'ok': False, 'error': str(e)})

    def log_message(self, *args):  # silence default access logging
        pass


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s')
    cfg = load_config()
    Handler.secret = cfg.get('shared_secret', '')
    if not Handler.secret:
        log.error('shared_secret is empty — refusing to start')
        sys.exit(1)
    firebase_admin.initialize_app(
        credentials.Certificate(cfg.get('service_account_file')))
    host = cfg.get('listen', '0.0.0.0')
    port = cfg.getint('port', 8090)
    log.info('push-relay listening on %s:%s', host, port)
    ThreadingHTTPServer((host, port), Handler).serve_forever()


if __name__ == '__main__':
    main()
