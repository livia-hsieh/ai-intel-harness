"""Email notifier — short subject + GitHub URL only, never digest content.

Per SCOPE.md: email is push-trigger only. Body has the GitHub URL for the
week's digest; user taps → reads on GitHub → marks ✅/⚠️/❌ → done. Email
content rendering is bad on phone, accumulating 52 emails clutters the
inbox, and recruiters can't see them — all reasons to keep email minimal.

SMTP via env vars (set as GitHub Secrets):
- SMTP_HOST (e.g., smtp.gmail.com)
- SMTP_PORT (e.g., 587)
- SMTP_USER (sender email)
- SMTP_PASS (app password — NOT your real Gmail password)
- NOTIFY_EMAIL (recipient — Livia's address)

Tested with Gmail SMTP using app password. SendGrid free tier (100 emails/
day) also works with the same env shape.
"""

from __future__ import annotations

import argparse
import os
import smtplib
import sys
from email.message import EmailMessage


def send_success_email(week: str, repo: str, *, smtp_host: str, smtp_port: int,
                       smtp_user: str, smtp_pass: str, recipient: str) -> None:
    digest_url = f"https://github.com/{repo}/blob/main/digests/{week}.md"
    foundation_url = f"https://github.com/{repo}/blob/main/digests/{week}/foundation.md"

    msg = EmailMessage()
    msg["Subject"] = f"[AI Intel] {week} ready"
    msg["From"] = smtp_user
    msg["To"] = recipient
    msg.set_content(
        f"本週 digest 已發布：\n\n"
        f"• 主週報（5 Pillar Pulse）：\n  {digest_url}\n\n"
        f"• Foundation 深讀：\n  {foundation_url}\n\n"
        f"建議讀法：\n"
        f"1. 滑開頁面看 TL;DR + provenance pie\n"
        f"2. 5 個 Pillar 各看 Top 3（繁中先讀，英文當練習）\n"
        f"3. Foundation 深讀（含 Mermaid 圖）\n"
        f"4. 在每個 Top 3 下勾 ✅ / ⚠️ / ❌（git commit 進 repo）\n\n"
        f"Health monitor 與成本紀錄一併更新。\n"
    )
    _send(msg, smtp_host, smtp_port, smtp_user, smtp_pass)


def send_failure_email(week: str, repo: str, run_id: str, *, smtp_host: str,
                       smtp_port: int, smtp_user: str, smtp_pass: str,
                       recipient: str) -> None:
    log_url = f"https://github.com/{repo}/actions/runs/{run_id}"

    msg = EmailMessage()
    msg["Subject"] = f"[AI Intel] {week} ❌ FAILED"
    msg["From"] = smtp_user
    msg["To"] = recipient
    msg.set_content(
        f"本週 digest pipeline 失敗，未產出 {week} 週報。\n\n"
        f"完整 log：\n{log_url}\n\n"
        f"常見原因：\n"
        f"• ANTHROPIC_API_KEY 過期或額度不足\n"
        f"• 某 source 改版導致 collect 大量失敗\n"
        f"• Pulse / Foundation 撞 rate limit\n\n"
        f"處理建議：\n"
        f"1. 點 log URL 看哪一步失敗\n"
        f"2. 修好之後可以手動觸發 workflow（GitHub Actions → Weekly AI Intel Digest → Run workflow）\n"
        f"3. 不修也沒關係，下週五會自動再跑\n"
    )
    _send(msg, smtp_host, smtp_port, smtp_user, smtp_pass)


def _send(msg: EmailMessage, host: str, port: int, user: str, password: str) -> None:
    with smtplib.SMTP(host, port) as server:
        server.starttls()
        server.login(user, password)
        server.send_message(msg)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="notify", description="Send digest notification email.")
    p.add_argument("--week", required=True, help="Week label e.g. 2026-W19")
    p.add_argument("--status", required=True, choices=["success", "failure"])
    p.add_argument("--repo", required=True, help="GitHub repo e.g. livia-hsieh/ai-intel-harness")
    p.add_argument("--run-id", default="", help="GitHub Actions run id (failure only)")
    args = p.parse_args(argv)

    cfg = {
        "smtp_host": os.environ.get("SMTP_HOST"),
        "smtp_port": int(os.environ.get("SMTP_PORT", "587")),
        "smtp_user": os.environ.get("SMTP_USER"),
        "smtp_pass": os.environ.get("SMTP_PASS"),
        "recipient": os.environ.get("NOTIFY_EMAIL"),
    }
    missing = [k for k, v in cfg.items() if not v]
    if missing:
        print(f"❌ Missing env: {missing}", file=sys.stderr)
        return 2

    try:
        if args.status == "success":
            send_success_email(args.week, args.repo, **cfg)
        else:
            send_failure_email(args.week, args.repo, args.run_id, **cfg)
        print(f"✅ Email sent to {cfg['recipient']}")
        return 0
    except Exception as e:  # noqa: BLE001
        print(f"❌ Email send failed: {type(e).__name__}: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
