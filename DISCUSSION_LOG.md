# 推廣 AI at Scale & AI Governance Solution — 討論進度日誌

> Session 間的進度交接檔，用來避免 Claude 失憶。
> **不是 wiki 內容**——最終 wiki 沉澱在 `/AI 知識庫/wiki/perspectives/`。
> 本檔只記「目前談到哪、下一步要做什麼、有什麼開放問題」。

---

## Session 1 — 2026-05-04

### 任務本質

Livia 在台灣市場推廣 AI at Scale & AI Governance solution，遇到三類阻礙：(1) 客戶成熟度不一，(2) MBB 競爭，(3) Governance 不直接盈利難賣。

希望規劃以下，3,4,5 收斂為決策樹：
1. AI at Scale 賣法（光譜兩端客戶接受度不同）
2. AI Governance 賣法（包進剛性需求）
3. 怎麼判斷大型機構需求
4. 怎麼判斷可接受的 sales 包裝/Style
5. 怎麼判斷可接受的切入點/專案大小

### 用戶澄清（AskUserQuestion 收齊）

| 項目 | 選擇 |
|---|---|
| 輸出形式 | 先口頭辯論再決定形式 |
| 解決方案理解管道 | 連 AI 知識庫，材料現成 |
| 客戶分級框架 | 從頭建立 |
| MBB 痛點 | 高層關係、frontier 故事、商業策略思考。**未選**「落地交付 IBM 較強」（後續澄清為「不確定，待驗證」） |

### 重大發現：wiki 已有大量基礎，不要重做

Livia 的 AI 知識庫是 Karpathy LLM Wiki 模式 Obsidian vault，三層分明（概念/觀點/經驗）。已有相關觀點頁：

| 觀點頁 | 與本任務關係 |
|---|---|
| [[banking-ai-maturity-t1t5-llm-thesis]] | **應用成熟度** BFSI 完整 |
| [[manufacturing-ai-maturity-m1m5-llm-thesis]] | **應用成熟度** 製造業完整 |
| [[frontier-vocabulary-arbitrage-7-levers]] | **MBB defense 七槓桿**（Livia 自己尚未實戰驗證，待推進）|
| [[data-strategy-顧問方法論]] | NSL 萃取的 6 步驟，≈ Livia 7 元件早期版本 |
| [[ai-governance-methodology-hub]] | Governance 方法論導航樞紐（114 行，未讀完）|
| 多個 governance perspectives | unified-control / project-admission / agent-control-extension / governance-level-split 等 |

客戶實戰（projects 層）：NSL、ESUN AI Governance、Wistron AI Governance/Data/Ontology、CTBC、HNCB、TCB eLoan、AUO、YAGEO（最新 2026-04-28 起案）、WNC、Heineken。

### 缺的觀點層 = 本任務真正目標

1. **「組織採購成熟度」軸**——與「應用成熟度」正交。應用成熟度看 CTO；組織採購成熟度看 sales。雙軸交叉才是賣法決策樹。
2. **應用成熟度 × 組織採購成熟度 → 賣法決策樹**（用戶 3,4,5 的收斂答案）
3. **AI Governance 包裝策略**（剛性需求綁附 = IBM 內部專案夾賣 / AI 場景擴大補強 / 三朵雲合作）
4. **既有 frontier-vocab-arbitrage 七槓桿從「觀察萃取」升級到「Livia 自己實戰」**——`open question 4` 的「分層敘事庫」工程設計，正好就是本任務要解的同一件事

### 已建辯論點（待持續推進）

- 不選「落地交付 IBM 較強」的可能解釋：(A)在台灣市場已死 (B)Livia 不想被定位成 implementer (C)Livia 不確認 IBM 真的更強 → Livia 確認是 (B)+ 部分 (C)，**保留為待驗證**
- 「成熟度」單軸 → 拆成多維（決策路徑 / 痛點壓力源 / 風險胃口）的提案，待用戶回應
- AI at Scale 本質 = 能力複利；AI Governance 本質 = 基礎設施稅 + 規模化權利金 → 分級維度應該不同（已被用戶確認）

### 任務狀態（見 TaskList）

#1 釐清 IBM solution 7 元件 → in_progress（已讀 4 個關鍵 perspectives，發現 7 元件 ≈ NSL 萃取的六步驟 + AI Governance 增量）
#2~7 → pending

### 下一步候選（待用戶選）

- **A.** 讀完 ai-governance-methodology-hub + 1 篇 governance projects → 寫 governance 賣法 perspective 草稿
- **B.** 直接寫「組織採購成熟度」perspective 草稿（不分 AI at Scale / Governance），後續再分裂
- **C.** 並行：兩個 perspective 同時開
- **D.** 先把賣法決策樹（問題 3/4/5 收斂）骨架做出來，當作後續基礎
- **E.** Livia 自己提想法

### 開放問題

- AI at Scale 賣法 perspective 與 AI Governance 賣法 perspective 要分頁還是合頁？（傾向分，本質不同）
- 「組織採購成熟度」維度初稿（決策路徑 / 痛點壓力源 / 風險胃口）夠不夠？
- 落地交付 IBM vs MBB「待驗證」——要不要在 wiki 開 Open Question 頁追蹤？
- frontier-vocab-arbitrage 第 138 行已連結 `Documents/Claude/Projects/推廣 AI at Scale Solution/frontier_vocabulary_arbitrage_7_levers_snapshot.md` 凍結快照——要不要查看？

---

## Session 2 — 2026-05-04（同日續）

### 進度推進

- 與 Livia 對齊 5 階段路徑（產品先 → 客群 → 賣法），選 Path A
- 完成 Q1（策略藍圖內涵）+ Q2（CoE 設計）兩個反問
- Livia 給 5 個結構性修正（藍圖、#1 vs #6、Ontology 融入 #3、#4 是傘含 ops/治理工具、#5 是平行可拆三子分類）
- 確認 AI Governance = AI at Scale 之 1，但很獨立可拆
- 提出 7 元件 × 顧問案 × 建置案 大表 v0.1
- Livia 要求自我挑刺 → 完成 14 條，呈現 7 條 critical + 7 條 backlog
- **v0.1 已落檔** → `SOLUTION_MAP.md`（之前漏落檔被 Livia 點出）

### Livia 給的關鍵指示

1. 藍圖 = 完整施工圖，「現在 AI at scale 框架有什麼，藍圖上就該出現什麼」
2. 組織人才 track 還有更多沒探討（含 CoE 設計責任，但不只 CoE）
3. 大表要先自我挑刺

### Open questions 給 Livia（待回）

見 `SOLUTION_MAP.md` 末尾「Open questions」區。

### Session 2 末尾額外修正

- Livia 點出 v0.1 表格用頓號破壞順序、不易閱讀 → v0.2 改分節編號清單格式
- 已知工作交付物落檔不能只放 chat，已存 feedback memory

### 下次 session 開頭該讀

1. 本檔（DISCUSSION_LOG.md）
2. SOLUTION_MAP.md（解決方案大表 v0.2）
3. AI 知識庫 CLAUDE.md（如要寫 wiki）

---

## 跨 session 約定

- 本日誌每次討論結束更新一次「Session N」段落
- **任何工作交付物（表格、清單、設計）一定要落成檔案在 project folder**，不只放在 chat 裡（Livia 點出過一次）
- wiki 沉澱（perspectives 頁）只在共識成形後寫，不要邊辯論邊寫 wiki
- 寫 wiki 前再次確認用戶對核心主張的同意度（Livia 在 CLAUDE.md 強調：不要把使用者經驗寫成業界通則）
