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

### Session 2 後段：v0.2 → v0.3 大修訂

Livia 提供 AI 治理 ASSET MAP（看 / 建 / 用 + 配套，M1-M12），並指出我 #5 拆 5a/5b/5c 完全不對。同時指出我把 Playbook、四階文件、Agent 控制項表錯放在「建置才完整」。

**v0.3 主要變動：**
1. **#5 全重寫按 Livia ASSET MAP 12 模組**（M1 成熟度 / M2-M5 建底盤 / M6-M7 跨階段 / M8-M9 場景循環 / M10-M12 配套）
2. **#3 重排順序**（業務 → 雙軌盤點 → Ontology 業務語意 → 架構 → 選型分階段）
3. **#4 去 watsonx 偏好**，加架構現況訪談、成熟度診斷、藍圖驅動需求拆解、best practice gap analysis、明確選型 framework、釐清「資料/系統層安全」vs「AI 模型/應用層治理工具」邊界
4. **顧問交付物完整版回歸顧問階段**——Playbook、四階文件（含完整評估表體系）、Agent 控制項表

**新存記憶：** `feedback_use_user_existing_structure.md`——用戶已有結構就用，不要自己發明

### Session 2 末段：v0.3 → v0.4

Livia 指出工作項太破碎，需要往上收一層成「銷售可講的模組」（仿 #5 ASSET MAP M1-M12 的粒度）。

**v0.4 變動：**
- 每個元件加「模組層」（3-7 個模組）
- 工作項變成模組底下細項
- 共 55 個模組（33 顧問 + 23 建置 - 1 重複 = 55）
- #5 ASSET MAP 不動（已是模組層）

### Session 2 後段：方法論矯正 + Phase 4 v0.1

Livia 點破我繞圈：「我目前認知就在這裡，你不要再從我身上挖」——指明應該是：**接受她認知為基底，Claude 帶外部視角擴張、補洞、挑戰**。

不再做 interview-style 的 bottom-up，改為：
- 直接從 Livia 兩段認知（光譜兩端 + 三條剛性需求路徑）擴張成 v0.1 賣法 Playbook
- 落檔 `SALES_PLAYBOOK.md`

⚠️ **關鍵記憶教訓**：Livia 已給的認知（哪怕不完整）是 base，不要反覆問她「你覺得呢」想挖更多。我的工作是 import 外部視角擴張，她挑刺。

### Session 2 末段：v0.1 → v0.2 結構重整

Livia 指示兩階段結構：
1. 切出幾種「可以賣的結果」+ 決策樹判斷客戶偏好指向某個結果
2. 根據客戶 文化/風格/驅動點/窗口 → 改變溝通和包裝

→ Claude v0.2 推進為三層 outcome catalog（15 個）/ 決策樹 / 包裝層——但 outcome 過度發明。

### Session 2 後段：v0.2 → v0.3 按 Livia 直接 named outcome 收斂

Livia 給兩個 anchor 訊息：
1. AI at Scale 4 種賣法（口述）：先場景後診斷 / 純顧問 / 顧問+場景+落地 / 純場景
2. AI Governance 5 客群套餐（截圖「支柱一·對外 GTM」）：A 補強升級 / B 內規重構 / C 全套新建 / D 工具棧 / E 一次性技術檢測

→ v0.3 按 Livia named outcome 收斂：
- **Part A**：9 個 outcome（AS 4 + GV 5），命名照 Livia
- **Part B**：進案路徑獨立成層（v0.2 把這個跟 outcome 混在 GV-1~8 裡是錯的）
- **Part C**：兩個決策樹（AS / GV 各一）
- **Part D**：包裝層（4 維度 / 5 archetype / 分層敘事庫）

⚠️ Livia 截圖標題「支柱一」implicit 還有支柱二、三 hook（待 Livia reveal）

已知 v0.3 問題：
- AS-1 先場景後診斷 vs AS-4 純場景 要不要合？
- GV-A 客戶 anchor 不確定是誰
- AS 進案路徑（B1 5 條）是 Claude 推
- 包裝 archetype 5 個是 Claude 推

### Session 2 末段：v0.3 → v0.4 按 Livia 4 段 pipeline 重整

Livia 給更精準工作流：
```
進案路徑（觸發點 + 窗口/有決策權的人）
  → 依客戶 profile 走決策樹
  → outcome
  → 依客戶 profile 走決策樹決定包裝
    （緣起痛點 → 用啥方式賣 → 整體語氣 style）
```

關鍵新概念「**售賣 Frame**」（Livia 例：「都是賣治理全套，工具思維 vs 顧問思維」）：
- Frame = IBM 在案子裡是誰（工具供應商 / 顧問 / 法遵伴侶 / AI Lab Partner / 集團統合者 / 危機戰友 ...）
- Frame 跟 Style（語氣風格）不同
- Frame 跟 outcome（範圍）也不同
- 同一 outcome 可走不同 Frame，由窗口 + 文化 + 驅動點決定

v0.4 變動：
- **Part B**：進案路徑加窗口維度（10 個窗口 W1-W10），組合出 12 條 archetype（R1-R12）
- **Part C**：加客戶 profile 概念層（10 維），決策樹輸入是 profile 而非單點訊號
- **Part D**：拆三件事 D1 緣起痛點 / D2 **售賣 Frame（9 個 F1-F9，新增層）**/ D3 語氣 Style（5 個 P1-P5，沿用）
- **Part E**：5 個 Step 完整工作流圖

⚠️ 已知 v0.4 問題：
- 進案路徑 R1-R12 是 Claude 推
- Frame 9 個可能過度發明（F1 工具 vs F3 標準服務 可能合）
- 客戶 profile 10 維可能太多
- D4 persona 對照表只示範一個組合（30+ 主要組合工程量大）

### Session 2 末段：v0.4 → v1.0 拆兩份 + 對人類友善

Livia 點出兩個錯：
1. AI at Scale & AI Governance 應該是兩份獨立檔案（她講過很多次）
2. v0.4 巨型 MD（800+ 行 + 14 條挑刺 + 12 個 questions）難讀

→ v1.0 拆成兩份精簡檔案（每份 < 200 行）：
- `SALES_AI_AT_SCALE.md`（4 種可賣結果 + 進案路徑 + 決策樹 + 包裝三件事）
- `SALES_AI_GOVERNANCE.md`（5 套餐 + 8 條進案路徑 + 決策樹 + 包裝三件事）

格式改善：
- 短段落，不是巨型表格
- mermaid 視覺化決策樹 / 工作流
- 重點放前（核心一句話 + 套餐表 → 細節）
- 移除「自我挑刺」「Open Questions」「變更紀錄」這些 meta 區塊（移到本 DISCUSSION_LOG）
- Frame 從 9 個收斂為 5-6 個

舊 SALES_PLAYBOOK.md 已 rename 為 `SALES_PLAYBOOK_v0.4_archive.md` 保留。

### v1.0 待 Livia 補的東西（兩份檔案末尾）

1. 每個結果 / 套餐的客戶 anchor
2. 進案路徑你親身打過哪幾條？死區哪幾條？
3. Frame 數量對嗎？
4. 「支柱二、三」是什麼？

### Session 2 末段：SALES_AI_GOVERNANCE.md v1.0 → v1.1

Livia 對 governance 進案路徑做修正：
1. **8 條 → 6 條（去冗餘）**：合併法規 + 危機；砍掉 Claude 推的「場景案前置」
2. **第 1 條重新理解**：不是「IBM 大案 piggyback」，而是「**IBM 顧問用 AI 工具效果未知 → 治理機制保證**」（proof point + 內建品質保證）
3. **分兩組**：A 組「與 IBM 既有關係結合」（IBM 主動帶）+ B 組「客戶端剛性需求」（客戶情境驅動）
4. **強調 4 段 pipeline 兩個決策樹**：推套餐 + 推包裝（v1.0 只有第一個，v1.1 補第二個）

v1.1 新增：
- 決策樹二（推包裝）：依觸發點 → 緣起 / 依窗口 → Frame / 依文化 → Style
- 範例：同 GV-C 全套新建對玉山 / YAGEO / CTBC / 中型銀行 4 種完全不同的講法

### Session 2 末段：v1.1 → v1.2 大重構（Frame / Style 結構修正）

Livia 給三個結構性批評：

**1. 觸發點與 Frame 重複** —「直接綁定」
→ 廢掉決策樹二，把 Frame 合進進案路徑表（觸發點 + 窗口 → 自動推 Frame + 開場）

**2. Style 內涵錯亂** —「工具供應商 / 顧問藍圖為何擺一起？」
→ 工具供應商 vs 顧問藍圖**鋪陳內涵完全不同**：
  - 工具供應商：built-in 思維、技術細節、production-ready
  - 顧問藍圖：3 年願景、roadmap、AI at Scale 未來想像
→ Style archetype 廢除，Style 變成 Frame 的內建屬性（鋪陳內涵）

**3. 缺客戶 sophistication 維度** — 同樣內涵不同程度客戶要不同包裝
→ 加客戶程度維度（高 / 中 / 低）→ 決定 frontier shorthand vs 比喻 vs 教育型

v1.2 新結構：
```
[1] 進案路徑表（觸發點 + 窗口 + Frame + 開場 一表搞定）
[2] 客戶 profile → 套餐（決策樹一）
[3] Frame 自帶鋪陳內涵（不是用詞，是核心故事）
[4] 客戶程度 → 包裝深淺
```

⚠️ **重要學習**：「Style 不是獨立 archetype，Style 是 Frame 的鋪陳內涵屬性」——這個 insight 應該也適用 AI at Scale 那份的修正

### Session 2 末段：v1.2 → v1.3 決策樹一反向設計

Livia 點出實務問題：v1.2 決策樹一全要客戶自答（要不要整體治理 / 成熟度 / 內規清不清），但**客戶自己根本不知道**。

→ v1.3 改為「用 IBM 銷售可外部觀察的訊號反推」：

5 個側寫訊號：
1. AI 應用面積（無/中/多）
2. AI 治理組織（無/散落/RAI office）
3. 內規狀態（沒/patchy/完整）
4. 客戶詞彙（保守/中/激進 frontier）
5. 採購行為（整體 RFP/單案/工具/法規驅動）

→ 5 訊號多數落哪欄就推哪個套餐
→ 加快速分支：採購意圖明確「要工具」直接走治理工具棧；明確「單案 validate」直接走一次性檢測

⚠️ **重要學習**：「決策樹輸入應該是 IBM 可觀察的客戶側寫訊號，不是客戶自答」——同樣的 insight 應該也適用 AI at Scale 那份的修正

### Session 2 末段：v1.3 → v1.4 Frame 對齊 + 進案路徑釐清

Livia 給 4 修正：

**1. Frame 對齊**：
- 工具供應商：補 Livia 解讀（客戶腦袋簡化版「買工具+IBM 教」，但 IBM 實際還是導入完整 operating model）
- 顧問藍圖 → **Operating Model 導入夥伴**（強調 operating model 概念）
- **AI Lab Partner 通常不存在**——砍。特殊情況保留（tier 1 客戶主動提新治理觀念）
- **危機戰友合進法遵伴侶**（內涵重疊，差別只在節奏：常態版 vs 加速版）

**2. 加 C 組進案路徑「技術前沿驅動」**：
- 客戶因 multiagent / 龍蝦 / Claude Code 等新技術出現來問怎麼治理
- 窗口：CTO / CDO / RAI

**3. 進案路徑與決策樹一的關係釐清**（v1.3 UX 失敗）：
- A 組（IBM 主動帶）：已有 default 套餐，5 訊號只用來「判斷是否升級」
- B 組（客戶剛性需求）：5 訊號從 0 跑決策樹
- C 組（技術前沿）：default 偏補強或檢測，5 訊號微調

**4. 進案路徑表加「默認套餐」欄**：A/C 組已有 default，B 組要 lookup

⚠️ **重要學習**：「不同進案路徑的決策樹用法不同——A 組用 default + 微調，B 組從 0 跑」——這個區分可能也適用 AI at Scale 那份

### Session 2 末段：v1.4 → v1.5 Frame vs 套餐分開決定

Livia 點出 v1.4 第 1 步犯大錯：客戶嘴上說「我要工具」**不直接 = GV-D 治理工具棧**。客戶心智模型（簡化版）≠ 實際需求。

→ 修正：**Frame 跟套餐獨立決定**
- 客戶採購意圖訊號（嘴上說的）= **Frame 訊號（怎麼包裝）**
- 客戶側寫 5 訊號（治理成熟度）= **套餐訊號（實際範圍）**
- 兩者正交、分開決定

→ GV-D 治理工具棧套餐**只在罕見真小案存在**——多數「要工具」客戶實際是 GV-A/B/C 用工具供應商 Frame 包裝

→ 範例：中型銀行嘴上說「我要工具」、但 5 訊號是低成熟 → 套餐 GV-C 全套新建 + 工具供應商 Frame 包裝（買工具+IBM 教用+技術移轉，IBM 內部仍跑完整 M1-M9）

⚠️ **重要學習**：「採購意圖訊號 ≠ 套餐訊號。客戶心智模型可能 ≠ 實際需求。Frame 跟套餐永遠分開決定。」——這個 insight 應該也適用 AI at Scale 那份的修正

### Session 2 末段：v1.5 → v1.6 GV-D 是 fallback 不是 default

Livia 補：
1. 真小工具案還是存在（不要否認）
2. 但**純工具買賣對 IBM Consulting 沒贏面**
3. 「抽絲剝繭出來」追問才能確認

→ v1.6 修：
- GV-D 明確標 **fallback 不是 default**
- 加 4 條抽絲剝繭追問問句
- 銷售策略警告

### Session 2 末段：互動 view 落檔（config 與展示層分離）

Livia 要求：可視化 + 互動 + 保留修改彈性 + raw data 可 config 不燒 token 改 HTML。

→ 落檔 `view/` 子資料夾：
- `index.html`：template + JS + CSS（一次寫好不動）
- `config_governance.js`：AI Governance 全部資料
- `config_at_scale.js`：AI at Scale 資料（v1.0，待對齊）
- `README.md`：使用指南 + 怎麼改 config

設計理念：**raw data 在 config，展示在 HTML**——以後改內容只改 config，不燒 token 改 HTML。

### Session 2 末段：governance config v1.6 → v2.0（白話化 + 結構大改）

Livia 給多項修正：
1. **用語白話化**：fallback / default 等英文術語砍掉
2. **outcomes 砍 scale 欄位**（Claude 自己幻覺生的人月與時間）
3. **進案路徑大改**：
   - A 組改成「IBM 內部賦能」（無窗口、無角色）
   - 原 A2/A3「IBM AI 專案結合」移到 B 組「客戶端需求」
   - 三朵雲獨立成 D 組 Partnership（不是客戶路徑）
4. **進案路徑表簡化 5 欄**：路徑/窗口/角色/開場白/推什麼套餐
5. **Frame → 「IBM 角色」**（中文一眼懂）
6. **「決策樹一」→ 「套餐推薦樹」**（只一棵就直接命名）
7. **加攤平版**：mermaid flowchart 一圖看完整體決策邏輯
8. **砍同套餐對不同客戶範例**（待 Livia 看攤平版自己腦中驗）

v2.0 互動 view：
- Outcomes 不顯 scale
- 進案路徑表 5 欄（含 A 組「IBM 內部用，不對外賣」標示）
- 套餐推薦樹有兩個 tab：互動版（5 訊號點選）+ 攤平版（mermaid 視覺化）
- 警告文字白話化

⚠️ **重要學習**：「白話化是長官友善的關鍵——英文術語、冗餘代稱（5 訊號、決策樹一）都該砍」

### Session 2 末段：v2.0 → v2.1 攤平版決策樹邏輯修正

Livia 點兩個問題：
1. 起點不該是「客戶嘴上要工具/單案/整體」3 個窄選擇——應該是進案路徑多元起點
2. 「內規」判斷跑了兩次（「單案 → 內規清楚？」分支 vs「治理成熟度 → 高: 已有完整內規」訊號）邏輯衝突

→ v2.1 修：
- 起點改成**進案路徑分組**（A/B/C/D 四路）
- 採購意圖（要工具/單案/整體）放 B/C 組之下作為 sub-decision
- 內規判斷只在一處（治理成熟度的 5 訊號之一）
- 「單案 + 內規不清 → 升級 GV-B/C」是 corner case 警告分支，不再走治理成熟度判斷

⚠️ **重要學習**：「決策樹的訊號維度不該重複出現——每個維度只在一個 decision node 出現」

### 下次 session 開頭該讀

1. 本檔（DISCUSSION_LOG.md）
2. SOLUTION_MAP.md（解決方案大表 v0.4）
3. SALES_AI_AT_SCALE.md（AI at Scale 賣法 v1.0，對人類友善版）
4. SALES_AI_GOVERNANCE.md（AI Governance 賣法 v1.0，對人類友善版）
5. SALES_PLAYBOOK_v0.4_archive.md（巨型版，僅 reference）
6. AI 知識庫 CLAUDE.md（如要寫 wiki）

---

## 跨 session 約定

- 本日誌每次討論結束更新一次「Session N」段落
- **任何工作交付物（表格、清單、設計）一定要落成檔案在 project folder**，不只放在 chat 裡（Livia 點出過一次）
- wiki 沉澱（perspectives 頁）只在共識成形後寫，不要邊辯論邊寫 wiki
- 寫 wiki 前再次確認用戶對核心主張的同意度（Livia 在 CLAUDE.md 強調：不要把使用者經驗寫成業界通則）
