import os, sys, json, html
from urllib import request

token = os.environ.get("PUSHPLUS_TOKEN")
if not token:
    print("no PUSHPLUS_TOKEN, skip notify")
    sys.exit(0)

title = sys.argv[1] if len(sys.argv) > 1 else "签到通知"
logfile = sys.argv[2] if len(sys.argv) > 2 else None
status = sys.argv[3].lower() if len(sys.argv) > 3 else ""

content = ""
if logfile:
    try:
        with open(logfile, encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        content = "read log error: %s" % e
content = content[-3500:]

status_map = {"success": " ✅ 成功", "failure": " ❌ 失败", "cancelled": " ⚠️ 取消"}
title = title + status_map.get(status, "")

payload = {
    "token": token,
    "title": title,
    "content": "<pre style='white-space:pre-wrap;word-break:break-all'>" + html.escape(content) + "</pre>",
    "template": "html",
}
req = request.Request(
    "https://www.pushplus.plus/send",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
)
try:
    with request.urlopen(req, timeout=20) as resp:
        print("pushplus:", resp.read().decode("utf-8", "ignore"))
except Exception as e:
    print("pushplus error:", e)
