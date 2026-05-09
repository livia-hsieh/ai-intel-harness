# Operating Guide — ai-intel-harness

> Day-to-day operating reference for Livia. When to trigger what, where outputs land, what to watch for.

---

## 自動排程一覽

| 工作 | 觸發時間 (UTC) | 觸發時間 (Asia/Taipei) | Cron |
|---|---|---|---|
| **Weekly Digest** | 每週四 22:00 | 每週五 06:00 | `0 22 * * 4` |
| **Quarterly Synthesis** | 3/25, 6/25, 9/25, 12/25 22:00 | 隔天 06:00 | `0 22 25 3,6,9,12 *` |

兩個都會：commit 結果到 repo + 寄 email 通知。

---

## 觸發時間建議（手動操作）

### Pulse (`pulse --all`)

**自動每週跑，不需手動**。

例外：
- 出差錯過、想補跑某週 → `pulse --all --write 2026-W19`
- 改了 prompt 想試新格式 → 手動跑 1 個 Pillar 看效果（`pulse --pillar 4`）

### Foundation (`foundation`)

**自動每週跑，curriculum 自動輪轉**。

| 場景 | 建議 |
|---|---|
| 想看特定 Track 的內容（不等輪到）| `foundation --track D --write` |
| 想 sync 到本機 wiki | 同上，因為 GitHub Actions 不會寫 OneDrive |

### Quarterly Synthesis (`synthesize-quarter`)

**自動 4 次/年（3/25, 6/25, 9/25, 12/25）**。

**首次有意義時間點**：
- 累積 < 4 個 Track essays → 提早跑會說「partial coverage」
- 累積 4~5 個 Track → 半完整視角，可看
- 累積 6 個 Track（12 週後）→ 完整 cycle，最有價值

**建議**：
- **第 1 季**（剛上線）→ 等自動跑（6/25）；不用提早
- **跑了 3 個 Track 之後**（~6 週後）→ 可以提早手動試一次看格式
- **常態**：依賴自動排程

### Collect (`collect`)

**自動每週跑**。

例外：
- 加新 source 進 sources.yaml → 手動 `collect --source <new-id>` 立刻抓
- 想要全 source 補 backlog → `collect`（無 --source 參數）

### Triage (`triage`)

**自動每週跑（在 weekly-digest workflow 裡）**。

例外：
- 改了 triage prompt → 手動 reset 部分 items 重評分

### Health (`health`)

**自動每週跑（紅燈會在 email 裡警示）**。

例外：
- 任何時候想看當下系統狀態：`health`

---

## 寫入路徑對照表

| 工件 | 自動跑時寫到 | 手動 Mac 跑時寫到 |
|---|---|---|
| Weekly digest | `digests/<week>.md` | 同左 |
| Foundation 深讀 | `digests/<week>/foundation.md` | `digests/...` + `<wiki>/concepts/track-X.md` |
| Quarterly synthesis | `digests/perspectives/<quarter>.md` | `digests/...` + `<wiki>/perspectives/<quarter>.md` |
| Health report | `data/health_latest.md` | 同左 |
| Cost log | `data/cost_log.jsonl` | 同左 |

`<wiki>` = `/Users/liviahsieh/Library/CloudStorage/OneDrive-IBM/AI 知識庫/wiki`

**自動跑只寫 repo**（GitHub Actions 看不到 OneDrive）。
**手動跑會同時寫 repo + wiki**（你 Mac 看得到 OneDrive）。

---

## 每週讀完 digest 之後的 routine

1. 📱 收到 email 推播 → tap → GitHub 開 digest
2. 滑開讀完（~10~15 分鐘）
3. 在 Top 3 段落下勾 ✅ / ⚠️ / ❌（用 GitHub web 編輯 → commit）
4. （選擇性）開 Cowork 跟 Claude 聊 5 分鐘上週 digest review，產出 `engagement_log.md` 紀錄
5. （選擇性）如果想 sync wiki：在 Mac 跑 `foundation --week <該週> --write`

---

## Cost 預期（每週/每年）

| 項目 | 每週 | 每年 |
|---|---|---|
| Triage incremental | ~$0.30 | $16 |
| Pulse 5-Pillar | ~$0.50 | $26 |
| Foundation Opus | ~$0.50 | $26 |
| Quarterly synthesis | (季) ~$1.50 × 4 | $6 |
| **總計** | **~$1.30/週** | **~$74/年** |

預算上限 $150/年；目前用量約 50%，富餘充足。

---

## 異常處理

| 狀況 | 通知方式 | 你要做什麼 |
|---|---|---|
| Hard fail（程式 crash / API 502 等）| email subject `[AI Intel] WNN ❌ FAILED` + GitHub Actions log URL | 點 log 看哪步壞，修了下次再跑 |
| Cost 超 $5/週警報 | health monitor 紅燈 + 下次 weekly run 自動 abort | 去 Anthropic console 看花費明細 |
| 某 source 連續 4 週 0 items | health monitor 黃燈，digest 加 source 健康警告 | 決定 demote 或修 yaml |
| Triage 分數壓縮（quality drift）| health 黃燈 | 改 triage prompt（review TRIAGE_SYSTEM in synthesizer/prompts.py）|

### Kill Switch（緊急停掉 pipeline）

GitHub web → Settings → Variables → set `PIPELINE_DISABLED = 1`

下次 cron 觸發時 workflow 會立刻 exit 0，不會跑任何步驟。改回 `0` 或刪掉 variable 即恢復。

---

## 常用指令速查

```bash
# 進入專案 + 啟動 venv（terminal 重開後第一件事）
cd "/Users/liviahsieh/Documents/Claude/Projects/推廣 AI at Scale Solution"
source .venv/bin/activate

# 看當前狀態
health

# 手動跑全套（如果某次自動跑壞了想補跑）
collect
triage
pulse --all > /tmp/pulse.md 2>&1
foundation --write
assemble-digest -i /tmp/pulse.md

# 個別操作
pulse --pillar 4 --dry-run     # 預估某個 Pillar 成本
foundation --track D --write   # 手動跑某 Track 深讀
synthesize-quarter --dry-run   # 預估 quarterly 成本

# 看上週 digest
open "https://github.com/livia-hsieh/ai-intel-harness/blob/main/digests/$(date -u -v -1w +'%Y-W%V').md"
```

---

## 設定速查

| 在哪設 | 變數名 | 用途 |
|---|---|---|
| GitHub Secrets | `AIINTELHARNESS` | Anthropic API key |
| GitHub Secrets | `SMTP_HOST` / `SMTP_PORT` / `SMTP_USER` / `SMTP_PASS` / `NOTIFY_EMAIL` | Email 通知 |
| GitHub Variables | `PIPELINE_DISABLED` | Kill switch (1=停, 不設或 0=跑) |
| Anthropic console | Spend limit | 防 key 洩漏 blast radius；建議 $30/月 |
| Anthropic console | API key 名稱 | `ai-intel-harness-prod`（與個人主 key 分離）|
