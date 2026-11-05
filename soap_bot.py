#!/usr/bin/env python3
"""石鹸ボット: GitHub Actions の上で定時に目覚め、Bluesky へ「今日の泡」を投稿する。

認証情報は環境変数から読む (GitHub Secrets 経由):
  BLUESKY_HANDLE        例: sekken-fukaxa.bsky.social
  BLUESKY_APP_PASSWORD  Bluesky のアプリパスワード

使い方:
  python3 soap_bot.py           投稿する
  python3 soap_bot.py --dry-run 投稿文だけ表示する (投稿しない)
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

from facts import FACTS

JST = timezone(timedelta(hours=9))
API = "https://bsky.social/xrpc"


def call(path, payload, token=None):
    req = urllib.request.Request(
        API + path,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def todays_text(now_jst):
    idx = now_jst.toordinal() % len(FACTS)
    greeting, fact = FACTS[idx]
    return f"今日の泡🫧 {greeting}\n{fact}"


def main():
    dry_run = "--dry-run" in sys.argv
    text = todays_text(datetime.now(JST))
    print(text)
    print(f"({len(text)} chars)")
    if dry_run:
        return 0
    if len(text) > 300:
        print("error: post exceeds 300 chars", file=sys.stderr)
        return 1
    handle = os.environ["BLUESKY_HANDLE"]
    password = os.environ["BLUESKY_APP_PASSWORD"]
    session = call("/com.atproto.server.createSession",
                   {"identifier": handle, "password": password})
    record = {
        "$type": "app.bsky.feed.post",
        "text": text,
        "createdAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "langs": ["ja"],
    }
    result = call("/com.atproto.repo.createRecord",
                  {"repo": session["did"], "collection": "app.bsky.feed.post",
                   "record": record},
                  token=session["accessJwt"])
    print("posted:", result.get("uri"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
