// Zabbix media type "ZbxView Push" (type Webhook) - the script. Parameters:
// RelayURL, Auth, SendTo ({ALERT.SENDTO}), Subject ({ALERT.SUBJECT}),
// Message ({ALERT.MESSAGE}), EventId ({EVENT.ID}), Host ({HOST.NAME}),
// Severity ({EVENT.SEVERITY}), Status ({EVENT.STATUS}).
try {
    var p = JSON.parse(value);
    var req = new HttpRequest();
    req.addHeader('Content-Type: application/json');
    req.addHeader('X-Auth: ' + p.Auth);
    var body = JSON.stringify({
        token: p.SendTo,
        title: p.Subject,
        body: p.Message,
        data: {
            eventid: p.EventId,
            host: p.Host,
            severity: p.Severity,
            status: p.Status
        }
    });
    var resp = req.post(p.RelayURL, body);
    var code = req.getStatus();
    if (code < 200 || code > 299) {
        throw 'relay HTTP ' + code + ': ' + resp;
    }
    return 'OK';
} catch (error) {
    Zabbix.log(3, '[ZbxView Push] ' + error);
    throw 'ZbxView Push failed: ' + error;
}
