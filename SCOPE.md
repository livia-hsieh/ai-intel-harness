# Bi-weekly AI Intel Pipeline — SCOPE

> **The contract.** 所有 downstream 設計(source、collector、synthesizer、delivery、meta-loop)都是這份 SCOPE 的後果。任何重大 design choice 違反這份 SCOPE,要麼回頭改 SCOPE 並升版,要麼放棄那個 design choice。
>
> **Version:** v0.1 (2026-05-03)

---

## 0. 為什麼 SCOPE 是 harness engineering 的第一塊磚

在 harness engineering 紀律裡,**scope 是契約,所有元件都是 scope 的後果**。每個 fetcher、每個 dedup 規則、每個 synthesizer prompt、每個 eval,都在編碼一個假設「scope 包含這個 / 排除那個」。寫不好的代價是全棧重做,不是改一個 prompt 能補。

這份文件就是這個 harness 的契約。

---

## 1. Consumer & Job-to-be-done

### Consumer 身份模型

**Practitioner-Strategist Hybrid**——技術深度 + 商業判斷不是 trade-off,是同一身份的兩個面向。Consumer 同時扮演兩個 role,皆全力推進,**不存在「主 / 副 / 第二職涯」的分配**:

- **Role A:IBM Consultant** — 客戶為金融業 + 製造業,簽單為 AI 轉型 / AI 治理專案,核心動作是與 C-Level 對話、提案、贏案
- **Role B:Harness Engineer in formation** — 累積技術力、portfolio、社群識別碼,以進入 frontier harness engineering 圈

### Five Growth Goals(這個 pipeline 必須同時餵的 5 條目標)

1. 技術 + 商業眼光的格局與執行力
2. 企業轉型 / 公司治理 / 商業策略 → 跟 C-Level 對話有談資
3. 金融業 / 製造業 AI 轉型趨勢 → 跟 C-Level 對話有談資
4. Harness engineer 技術力與圈內識別

每個 Pillar(下節)都至少對應 2 條 goal,沒有 goal 是孤兒,沒有 Pillar 是奢侈品。

### Job-to-be-done

每週收到 digest 後 consumer 會做的事:
- 在當週至少一次客戶對話 / 顧問同業會議 / 設計討論 中應用 digest 提到的概念、案例或觀點
- 把 Foundation 軌的深讀內容反向寫入 AI 知識庫(`wiki/concepts/` 或 `wiki/perspectives/`)
- 偶爾觸發行動:改 pitch、約客戶聊、寫一篇 design note、補一頁 wiki

**Digest 不是新聞消費,是資產建構。**

---

## 2. Five Pillars

| # | Pillar | 服務的 Growth Goals | 性質 |
|---|--------|------------------|------|
| 1 | **產業 AI 真實落地(BFSI + 製造業)** | #2 #3 | 案例 + 監管 + 競品 deck |
| 2 | **AI 戰略 / 治理 / 董事會層級論述** | #1 #2 | C-Level elite discourse |
| 3 | **Frontier 能力 + 模型動向** | #1 #4 | 能力動態 + 系統性學科累積 |
| 4 | **Harness Engineering 實作技藝** | #1 #4 | Curriculum-driven 學科建模 |
| 5 | **學派 / 社群 / 思想動態** | #1 #4 | 圈內認知地圖 |

### Pillar 1 — 產業 AI 真實落地

- **Pulse**:特定銀行 / 製造業者本期實際做了什麼(上線 / 失敗 / 回收 / 擴展)、監管動向、競品顧問業 deck 變化
- **Foundation**:每週深讀一個產業 case(Bloomberg AI、Morgan Stanley AI、Klarna、BoA Erica、玉山金秘書、北富銀鷹眼、緯創 OEE 等)
- **乾貨優先級**:有實際數字 / 架構 / 失敗紀錄的 case 優先,但**不強制**——含金量是第一篩,缺架構圖時 synthesizer 可以推論並標註(見 §4 紀律 3)

### Pillar 2 — AI 戰略 / 治理 / 董事會層級論述

- **Pulse**:橫跨七類 source 的本期動作:
  - **MBB**:McKinsey QuantumBlack / MGI、BCG GAMMA / X / Henderson Institute、Bain Vector
  - **AI-specialty boutique**:Palantir 部署團隊內容、Anthropic Applied AI、OpenAI Solutions
  - **Big Tech 顧問臂**:Microsoft Industry Solutions、Google Cloud Industry Practice
  - **Big 4**:PwC Strategy&、EY、KPMG、Deloitte AI Institute
  - **獨立 thought leader**:Stratechery、a16z、The Information AI、Decoder
  - **學術 think tank**:MIT Sloan CISR、Stanford HAI
  - **監管 / 董事會智庫**:金管會、歐盟 AI Act tracker、NACD、Spencer Stuart
- **Foundation**:系統性補強 C-Level 對話論述武器庫(AI 對 Porter 五力、Board AI Risk Oversight 框架、AI 時代 capital allocation、AI 對 BFSI cost-to-income / 製造業 OEE 數量級影響)
- **Type D 例外配額**:純非 AI 商業 / 治理內容上限 10~15%,只在「直接影響 AI 購買決策」時納入(銀行併購、央行利率、產業景氣)

### Pillar 3 — Frontier 能力 + 模型動向

- **Pulse**:模型 release 不報新聞,**只報「這個能力突破讓什麼新東西可以建構了」**——每篇必含「現在能做、之前不能做」對比
- **Foundation**:Track A 系統性補(scaling laws、post-training、capability eval、major model 家族對比)

### Pillar 4 — Harness Engineering 實作技藝

- **Pulse**:本期出現的新 pattern / failure mode post-mortem / 工具新版 / production 紀律新做法,排序後每期上限 3 件 + 觀察名單一行帶過
- **Foundation**:Curriculum-driven,**每週輪一個 track 深讀**,首輪順序 B → C → D → E → F → G(理由:由靠近模型 → 靠近 production,符合 0→100 學習路徑):

| 輪次 | Track | 主題 |
|------|-------|------|
| W1 | B | Prompt + Context Engineering |
| W3 | C | Agent 架構模式(ReAct/Reflexion/multi-agent/MCP) |
| W5 | D | Evals 設計(LLM-as-judge / online eval / synthetic eval) |
| W7 | E | 工具與基礎設施(framework / observability / vector DB / model gateway) |
| W9 | F | 部署運行紀律(cost / 可靠性 / 延遲 / 安全) |
| W11 | G | 治理與安全(NIST AI RMF / EU AI Act / RSP) |
| W13~ | 回到 B | v2 迭代(補 W1~W12 期間新發展) |

每篇 Foundation 深讀**直接寫入** AI 知識庫對應 wiki concept 頁,有版本歷史(v1 → v2 → v3)。

### Pillar 5 — 學派 / 社群 / 思想動態

- **Pulse**:本期 Latent Space / Dwarkesh / Interconnects / Decoder 哪一集有 signal,Anthropic / OpenAI / DeepMind / Eleuther / Berkeley AI 各派誰丟了什麼觀點
- **Foundation**:Track H + K + L,系統性建立「圈內地圖」(該認識的人 / 該訂的 newsletter / 該潛伏的社群)

---

## 3. Out of Scope(明寫的排除清單)

明寫排除是 SCOPE 紀律最容易被跳過卻最關鍵的一節。沒寫的東西半年後會 scope creep。

**預設排除:**

- 通用科技新聞(TechCrunch / The Verge 等)
- Crypto / Web3(除非與 AI 直接交叉)
- 個人 X/Twitter 熱議 take(訊噪比過低,個人 take 留給 Pillar 5 白名單作者)
- 影像 / 影片 generation 細節(除非與銀行 / 製造業務直接相關)
- 行銷話術型企業 PR(無技術或商業判斷實質)
- 純 AI 倫理哲學辯論(感性內容,非 actionable)
- 中文 AI 內容農場
- 求職 intelligence(暫時排除,等 Role B 進入正式求職階段再加)

**例外條件:**Type D(純非 AI 商業)只在 Pillar 2 的「直接影響 AI 購買決策」配額內。

---

## 4. 合成紀律(6 條鐵律)

1. **每個 Pillar 有明確 output shape 契約**——briefing 該長什麼樣、有哪些固定欄位
2. **合成規則是 guidelines 不是 gates**——不卡死必須有什麼,只卡知識含金量(signal-to-noise)。Synthesizer 可以推論 / 補架構圖 / 對應 code pattern,不要求來源材料先有
3. **Provenance + inference markers 強制**——所有合成段落明確標註:
   - `[原文]` 直接出自來源
   - `[推論]` 我合成的、有據可循,但你要查證
   - `[假設]` 我填補的空白,可能錯
4. **每篇 briefing 結尾附驗證提示**——「本篇含 N 段推論 + M 段假設,引用前建議查證以下三個關鍵點」
5. **強制 URL 引用**——每段提到的事實、數字、引述都要 hyperlink。`[原文]` 段必有 URL,`[推論]`/`[假設]` 段附「推論基於 [URL1][URL2]」。Digest 末尾整理「本期所有引用 URL 清單」方便 spot-check。**缺 URL 的段落直接不收**
6. **雙語輸出**——每篇 briefing 同時產出英文(主)+ 繁中專有名詞 inline 標註版本(衍生)。English-first synthesis,然後 cheap translation pass 產 bilingual。年度額外成本約 $50~$80(已含在 budget)。重複翻譯透過 `知識庫/_glossary.md` 快取避免

---

## 5. Output Shape:每週 digest 長什麼樣

```
=== W## YYYY-MM-DD Digest ===

# TL;DR(半頁)
本期最該注意的 1 件事:[一句話]
本期 Foundation 主題:[Pillar X · Track Y]
本期 N 段推論 + M 段假設,優先查證:[列 3 點]

# Pillar 1:產業 AI 真實落地
## Pulse(本期 Top 3)
1. [briefing 1: 數字 / 出處 / 對你客戶的具體含意]
2. [briefing 2]
3. [briefing 3]
## Watch list(一行帶過):...
## Foundation(本期深讀:[case 名])
[1~2 頁深讀]

# Pillar 2:AI 戰略 / 治理 / 董事會層級論述
[同結構]

# Pillar 3:Frontier 能力 + 模型動向
[同結構]

# Pillar 4:Harness Engineering 實作技藝
## Pulse
## Foundation(本週主題:Track X)
[深讀,直接寫入 wiki/concepts/]

# Pillar 5:學派 / 社群 / 思想動態
[同結構]

# Coverage Check
本期跟 HN top AI posts / Latent Space 比對,我們漏了什麼:[列出]
本期推論 / 假設總計:[N + M]
```

**事件觸發 rapid update**:1~2 頁,只針對該事件,跳過所有其他 Pillar。

---

## 6. Cadence

- **每週固定 run**:**週五交付**(週末讀 / 週一帶新詞進客戶會議)
- **事件觸發 rapid update**:重大事件(模型 release / 監管動作 / 大型併購) 觸發,3 天內出
- **每季 meta-loop**:每 12 週跑一次完整 self-correction(見 §10)

---

## 7. 視覺產出規格

- **主力**:Mermaid(`flowchart` / `sequenceDiagram` / `mindmap` / `xychart`),純文字、git diff-friendly、GitHub & Obsidian 直接 render
- **複雜時**:inline SVG
- **比較資料**:Markdown table
- **量化複雜時**:產 Python matplotlib code 給 consumer 自己跑(不嵌入 digest)
- **不做**:照片寫實圖、動畫(對技術內容無 leverage)

---

## 8. Memory Layer:Dedup + Context Cache

避免重複處理已看過內容 + 避免重複 LLM 處理已處理過 URL,設計分五層:

| Level | 機制 | 抓什麼 |
|-------|------|------|
| **L0 Content cache** | 該 URL 已處理過、已提取的 facts / 已產的 briefing 片段直接 reuse | **避免同 URL 重新 LLM query 浪費 token** |
| L1 | URL hash | 同連結重抓 |
| L2 | 內容 hash(normalize 後) | 同內容換 URL 重發 |
| L3 | Semantic embedding(text-embedding-3-small)cosine > 0.92 | 改寫過的轉貼 |
| L4 | LLM 邊緣判定(0.85~0.92 區間) | 留 future option |

**採用 L0+L1+L2+L3,L4 留 future option。**

**儲存**:`url + content_hash + embedding(1536-d float)+ first 200 chars + processed_date + pillar_assignment + extracted_facts(json) + briefing_snippet(已產過的合成結果)`,SQLite 檔案直接 commit 進 repo,**不存全文**(浪費 + 版權風險)。一年估算 < 80MB。

**雙語 glossary 快取**:`知識庫/_glossary.md`(LLM-readable)維護專有名詞翻譯對照(harness、scaffolding、ontology 等),翻譯前先讀此檔避免重複翻譯。Glossary 同時是 Livia 英文學習進度的紀錄。

---

## 9. Token Budget & Model Strategy

**混合模型策略**(年度目標 **$150~$200**):

| 階段 | 模型 | 理由 |
|------|------|------|
| 相關性篩選 / 簡單去重判定 | Haiku 4.5 | 便宜、快、夠用 |
| Pulse 合成 | Sonnet 4.6 | 平衡品質與成本 |
| Foundation 深讀 | Opus 4.6 | 該段值得最高品質,反正每週只跑一次 |
| Embedding (dedup) | text-embedding-3-small | 成本趨近 0 |

**成本上限警報**:任何單週 run > $5 觸發 alert,排查是否 source 爆量或 prompt 失控。

---

## 10. Success Criteria & Meta-loop Triggers

### Eval seeds(怎麼判斷這個 pipeline 在 work)

1. **Vocabulary hit rate**:digest 浮現的詞 → 多久後在 consumer 客戶端 / 顧問同業 / 業界 newsletter 出現(套利時間差量化)
2. **Coverage**:每期 digest 對 HN top AI posts / Latent Space 主題的覆蓋率
3. **Actual usage**:consumer 在客戶對話 / wiki / design notes 引用 digest 內容的頻率
4. **Portfolio signal**:GitHub stars / README 訪客 / 面試官對 design notes 的反應

### Meta-loop trigger 條件

| 類別 | 訊號 | 觸發後動作 |
|------|------|----------|
| **Digest 品質下滑** | 連續 3 期 consumer 評 ≤3/5;連續 2 期「沒看到新東西」;客戶提到 digest 漏抓的重要訊息 | Synthesizer prompt 重調 + source 補強 |
| **Source 健康度** | 某 source 連續 4 週無新內容;內容變行銷化;新影響力作者未進清單 | 移除停產 / 降權劣化 / 加入新 source |
| **角色 / 領域漂移** | Consumer 客戶產業變;職涯目標調;harness eng 領域分裂出新子領域 | SCOPE.md 重寫、Pillar 結構檢討 |
| **系統衛生** | Token 成本跑高(> $5/週);推論準確率降;知識庫頁數跨階段門檻 | 架構升級(向量化 / manifest / archive) |

**自動觸發**:每 12 週(季度)排程跑一次完整 meta-loop,輸出「pipeline 自我健檢報告」。
**手動觸發**:Consumer 隨時可下指令 `/pipeline-健檢`。

### Source list 的三通路自我更新(Mechanism A 維護)

外部權威清單會過時,設計三條通路同時跑:

| 通路 | 觸發 | 作用 |
|------|------|------|
| **A1 排程交叉驗證** | 每 12 週(季度) | 系統自動重跑 Mechanism A:抓 Latent Space top list / a16z canon / Hamel reading / conference speakers,跟現有 source 算交集差集,自動提名升降 |
| **A2 Consumer 主動 flag** | 隨時 | Consumer 看到誰冒出來,直接告訴系統「加入 X」,X 進 T2 reserve 觀察 4 週,有 signal 才升 T1 |
| **A3 系統自我發現** | 每週 run 自動 | Synthesizer 跑 Pulse 時,**追蹤「被頻繁引用但不在 source list」的人/公司**(例如 Anthropic blog 連續 3 週引用 Sholto Douglas,但他不在 source list)→ 自動產生候補加入提名,digest 結尾顯示 |

A3 是核心:**pipeline 讀自己抓的內容,反向發現權威人物,自我擴張 source map**。

---

## 11. Stack & Tooling

- **Language**:Python(harness engineering 圈主流,求職訊號最強)
- **GitHub**:Day 1 public,build in public
- **Visuals**:Mermaid 主力
- **Cowork → Claude Code 切點**:Task #3(寫真 code)時切換,Cowork 處理策略對話 + markdown 寫作,Claude Code 處理 codebase + git workflow

---

## 12. Pending Decisions(尚未拍板)

- [ ] GitHub username + repo name(strawman:`ai-intel-harness` / `frontier-pulse`)
- [ ] Source list 本身(Task #2,從這份 SCOPE 倒推)
- [ ] Delivery channel(email / Notion / GitHub README auto-commit / 純檔案,可暫時延後)
- [ ] Foundation curriculum 順序是否要調(預設 B→C→D→E→F→G,Consumer 可優先排其他)

---

## 13. Engagement & Eval Loop(consumer 怎麼餵 signal 回系統)

**問題**:之前定義的 `livia_engagement_score` 沒指明 consumer 實際怎麼把 signal 餵回 pipeline。沒這層,所有 eval 是空的,Mechanism A1/A2 不知道憑什麼觸發。本節補上。

### Layer 1 — Inline Checkbox(被動,git-tracked)

每篇 briefing 結尾強制標準格式:

```markdown
---
**Rate this briefing**:
- [ ] ✅ useful — 已用 / 會用
- [ ] ⚠️ meh — 太老 / 重述過的
- [ ] ❌ skip — 不相關 / 偏題
```

Consumer 勾一個 + commit。下一次 pipeline run 讀上週 digest 的勾選狀態,per-source 計分:

| 勾選 | 分數 |
|---|---|
| ✅ useful | 1.0 |
| ⚠️ meh | 0.5 |
| ❌ skip | 0.0 |
| (未勾) | 0.3(neutral default,不懲罰忘記) |

優點:**0 infra、git history 自然紀錄、綠色 ✅ 在 repo 累積本身是 portfolio 訊號**(hiring manager 看到 GitHub 有 60 週累積的 engagement marks,直接加分)。

### Layer 2 — Weekly Cowork Review(主動,qualitative)

Consumer 每週收到 digest 後,**回 Cowork 啟動「review last week's digest」**,Claude:
- 讀 digest + 勾選狀態
- 對 ⚠️ / ❌ 的 briefing 追問「為什麼?」
- 把答案 append 到 `engagement_log.md`
- 這個 qualitative data 餵 Mechanism A1(季度健檢)+ A2(source 增刪)

時間成本:5~10 min/週。**非強制**,但連續 4 週跳過,Layer 1 訊號量不足以做決策,系統會主動 nudge。

### Layer 3 — Downstream Citation Tracking(Cowork 自動捕捉,consumer 零負擔)

**設計原則**:Layer 3 訊號(downstream usage)有價值但要求 consumer 手動打 tag = friction-heavy,違反「AI 服務人類」紀律。改由 Cowork(Claude)自動捕捉,consumer 完全不用記得做任何事。

**機制三條(全部 AI-mediated):**

1. **被動偵測**:Cowork session 中 consumer 提到任何近期 digest 內容(「上週 digest 那個 X」「那篇 Anthropic eval」),Claude 自動 grep 最近 4 期 digest 推測指向哪一篇 briefing,silently append 到 `engagement_log.md`
2. **月度 recall check**:每月第一次 Cowork session,Claude 主動問「過去 4 期哪幾篇你實際用到客戶對話 / wiki / deck?口頭報即可」。Consumer 30 秒回答,Claude 登錄
3. **Wiki backlink auto-propose**:Consumer 在 Cowork 寫 / 更新 wiki 頁時,Claude 自動掃內容看有沒有源自最近 digest,主動 propose「這段加 `source: digests/2026-W19` link 嗎?」,consumer 一句 yes/no

**Consumer 端動作**:零。繼續正常用 Cowork 即可。**所有 tag 由 Claude 在背後維護**。

**Citation log 格式**(Claude 維護):
```markdown
# engagement_log.md
2026-W19#briefing-3 (Karpathy nanoGPT update) → cited 2026-05-12 (wiki update on harness-design)
2026-W20#briefing-1 (Palantir Q1 earnings) → cited 2026-05-15 (Cathay client prep)
```

### Signal Yield 公式(per source)

```
signal_yield = digest_inclusion_rate
             × avg_inline_checkbox_score
             × (1.0 + downstream_citation_bonus)
             # citation_bonus: 有 = 0.5, 無 = 0.0
             # 所以乘數最低 1.0、最高 1.5

# 4 週累積後決策
> 0.5 → 投資 adapter / 升級
0.2 ~ 0.5 → 維持現狀,觀察第 5~8 週
< 0.2 → 降權
0(0 inclusion) → 移出
```

Layer 2 qualitative data **不進公式,作為 override 使用**——Cowork 季度健檢時 consumer 跟 Claude 聊完可手動翻案。

---

## 14. MVP Mode(2026-05-04 起,4 週驗證期)

**核心紀律**:**MVP 階段只用免費 source**,證明 pipeline value 後再投資付費 channel。

### MVP-deferred(暫時關閉,不寫 code path)

- **Paywall**:Stratechery、The Information AI → 走 HITL queue,但不發 weekly notification(降為 ad-hoc 手動)
- **Twitter API**:14 個 individual influencer 不直接抓推文,**改走 echo 通道**

### Echo 通道機制(免費替代 Twitter)

Individual influencer 的重要發言通常 1~2 週內被以下 free source 引用,於是 Mechanism A3 自動捕捉:

- Latent Space(podcast + newsletter)
- Interconnects(Nathan Lambert)
- Import AI(Jack Clark)
- The Batch(吳恩達)
- Last Week in AI / Ben's Bites / TLDR AI(廣度兜底)
- arXiv 引用

**Twitter primary 改為**:
- 仍保留個人多通道資料,但 `mvp_mode: echo_only` 標籤
- 主抓改成個人擁有的免費 owned media:YouTube、GitHub、個人 blog、Substack、podcast appearances
- 例外:無自有 owned media 的 influencer(例如 Yann LeCun 主要在 X),完全靠 echo

### MVP 升級條件(轉付費的觸發)

4 週後,若以下兩條同時滿足,**才**評估 Twitter API 付費:

1. **echo 覆蓋率 < 70%**:即重要 influencer 發言**真的有 30% 漏掉**(用 Cowork 季度 review 評估)
2. **個別 influencer signal_yield > 0.5**:該 influencer 的內容真的值得直抓

否則保持 echo only。**很可能永遠不需要付 Twitter API**。

### MVP-active 設定 in sources.yaml

每筆 source 加欄位:

```yaml
mvp_active: true | false
mvp_mode: full | echo_only | hitl_adhoc
```

預設 `mvp_active: true, mvp_mode: full`。Twitter individual / paywalled 改 false / echo_only / hitl_adhoc。

---

## 15. Changelog

- **v0.1 (2026-05-03)** — Initial scope locked. 經過 Cowork 多輪對話收斂(身份模型 → 5 Pillars → Pulse+Foundation → 4 紀律 → cadence/視覺/memory/budget/eval/meta-loop)。
- **v0.2 (2026-05-03)** — Pillar 2 source 地圖擴張(MBB + AI-specialty boutique + Big Tech 顧問臂 + Big 4 + 學術 think tank);合成紀律從 4 條 → 6 條(加 URL 引用 + 雙語);Memory layer 加 L0 content cache;Mechanism A 改成三通路維護(A1 排程 / A2 Consumer flag / A3 系統自我發現)。
- **v0.3 (2026-05-04)** — 加 §13 Engagement & Eval Loop(三層 engagement:inline checkbox / Cowork review / downstream citation),補上之前 hand-wave 過去的 `livia_engagement_score` 真實機制;加 §14 MVP Mode(免費 only,paywall + Twitter API deferred,個人 influencer 走 echo 通道靠其他 free source 1~2 週延遲覆蓋);釐清「wide scan 是 source 廣度不是時間廣度」並把 incremental cursor 寫進 collector spec。
- **v0.3.1 (2026-05-04)** — Layer 3 重新設計:從「consumer 手動打 tag」改成「Cowork(Claude)自動 mediated」三條機制(被動偵測 / 月度 recall / wiki backlink auto-propose)。Consumer 端動作降到零,burden 移到 Claude。Trigger:Livia 反映 Layer 3 對她不友善——這個調整本身就是 harness eng「scaffolding 應該服務人類,不該服務 AI 自己」紀律的具體實踐。
