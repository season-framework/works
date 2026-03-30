import datetime
import json
import subprocess
import sys

config = wiz.model("portal/works/config")
orm = wiz.model("portal/season/orm")
pushdb = orm.use("push_subscription", module="works")

logger = wiz.logger("push", "struct")

PUSH_WORKER_SCRIPT = """
import sys, json
from pywebpush import webpush
payload = json.loads(sys.stdin.read())
result = webpush(
    subscription_info=payload['subscription_info'],
    data=payload['data'],
    vapid_private_key=payload['vapid_private_key'],
    vapid_claims=payload['vapid_claims']
)
print(json.dumps({"status_code": result.status_code}))
"""

PYTHON_BIN = sys.executable or "/opt/anaconda3/envs/wiz/bin/python"

def _send_webpush_subprocess(subscription_info, data, vapid_private_key, vapid_claims):
    payload = json.dumps({
        "subscription_info": subscription_info,
        "data": data,
        "vapid_private_key": vapid_private_key,
        "vapid_claims": vapid_claims
    })
    result = subprocess.run(
        [PYTHON_BIN, "-c", PUSH_WORKER_SCRIPT],
        input=payload,
        capture_output=True,
        text=True,
        timeout=30
    )
    if result.returncode != 0:
        raise Exception(result.stderr.strip().split("\n")[-1] if result.stderr else "subprocess failed")
    return json.loads(result.stdout)

class Model:
    @staticmethod
    def subscribe(user_id, subscription_info):
        endpoint = subscription_info.get('endpoint', '')
        keys = subscription_info.get('keys', {})
        p256dh = keys.get('p256dh', '')
        auth = keys.get('auth', '')
        user_agent = subscription_info.get('user_agent', '')

        if not endpoint or not p256dh or not auth:
            raise Exception("Invalid subscription info")

        existing = pushdb.get(user_id=user_id, endpoint=endpoint)
        now = datetime.datetime.now()
        if existing:
            pushdb.update(dict(p256dh=p256dh, auth=auth, user_agent=user_agent, updated=now), id=existing['id'])
            return existing['id']

        data = dict()
        data['user_id'] = user_id
        data['endpoint'] = endpoint
        data['p256dh'] = p256dh
        data['auth'] = auth
        data['user_agent'] = user_agent
        data['created'] = now
        data['updated'] = now
        return pushdb.insert(data)

    @staticmethod
    def unsubscribe(user_id, endpoint):
        pushdb.delete(user_id=user_id, endpoint=endpoint)

    @staticmethod
    def send(user_id, title, body, url="", icon=""):
        rows = pushdb.rows(user_id=user_id)
        if not rows:
            return

        try:
            push_config = wiz.config("push")
            vapid_private_key = push_config.VAPID_PRIVATE_KEY
            vapid_claims_email = push_config.VAPID_CLAIMS_EMAIL
        except Exception:
            return

        if not vapid_private_key:
            return

        payload = json.dumps(dict(
            title=title,
            body=body,
            url=url,
            icon=icon or "/assets/portal/season/brand/icon-192.png",
            badge="/assets/portal/season/brand/icon-192.png"
        ))

        for sub in rows:
            subscription_info = {
                "endpoint": sub['endpoint'],
                "keys": {
                    "p256dh": sub['p256dh'],
                    "auth": sub['auth']
                }
            }
            try:
                result = _send_webpush_subprocess(
                    subscription_info=subscription_info,
                    data=payload,
                    vapid_private_key=vapid_private_key,
                    vapid_claims={"sub": f"mailto:{vapid_claims_email}"}
                )
                logger(f"Push OK: user={user_id}, status={result.get('status_code')}")
            except Exception as e:
                error_str = str(e)
                logger(f"Push failed: user={user_id}, error={error_str[:200]}", level=logger.LOG_ERROR)
                if "410" in error_str or "404" in error_str or "403" in error_str:
                    try:
                        pushdb.delete(id=sub['id'])
                    except Exception:
                        pass

    @staticmethod
    def send_bulk(user_ids, title, body, url="", icon=""):
        for uid in user_ids:
            try:
                Model.send(uid, title, body, url, icon)
            except Exception:
                pass
