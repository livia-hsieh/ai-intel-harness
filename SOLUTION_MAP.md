# 解決方案大表 — 7 元件 × 顧問案 × 建置案

> **版本**：v0.2（2026-05-04，從 v0.1 重寫——格式改為分節編號清單，保留順序）
> **目的**：把 Livia 的 IBM AI at Scale solution 7 元件，依「顧問規劃案 vs 建置案」拆解關鍵工作項目與產出。每項按時間 / 邏輯順序編號。
> **狀態**：Phase 2 工作文件，待 Livia 糾正。穩定後沉澱 wiki/perspectives/。
> **下一步**：Livia 挑刺 v0.2 → Claude 改 v0.3 → 凍結 → 進 Phase 3。

---

## 已知 7 條 Critical 自我挑刺（修 v0.2 前先看）

詳見最末「自我挑刺」區。簡述：
1. **顧問 vs 建置二元太粗**——實務 5 類（純顧問 / 顧問+試點 / 純建置 / BOT / 長期 advisory）
2. **#1 建置 N/A 寫錯**——應是「指揮/監督/整合」
3. **#5b 必 piggyback 在 #6**——無獨立建置案
4. **NSL 殘影 vs 2026 新東西沒區分**
5. **缺「典型專案規模/人月/工期」欄**
6. **缺「IBM 內部 owner」欄**
7. **表的目的不明**——catalog / process / training？

→ v0.2 已部分處理 1, 2, 3；其他待 Livia 裁決後修。

---

# #1 策略藍圖

> 性質：總指揮元件。顧問案是主軸，「建置案」其實是「方案分發到 #2~#7 + 跨元件 PMO + 長期 advisory」。

## 顧問案

### 典型工作項目（按順序）

1. 立案：與 CXO 對齊範圍 / 預算 / 時程 / 期望
2. 高階訪談：董事長 / CEO / CXO 群分別訪談（戰略意圖 + 痛點 + 期望）
3. 戰略文件分析：年報 / 法說 / 內部策略 deck → 萃取明示與隱含戰略
4. 產業對標：選 3-5 家標竿（國內 + 國際）做 frontier 對齊度比對
5. 場景訪談：BU 層級訪談 + 問卷，蒐集場景需求
6. 能力 gap 評估：用應用成熟度（T1-T5 / M1-M5）+ 7 元件成熟度評估
7. 方案彙整：所有可能方案整理成方案卡（含 #2~#7 各元件方案）
8. 方案排序：按效益 × 可行性 × 戰略對齊 × 依賴關係 × 預算
9. 三期 timeline 編排：MVP / Y1 / Y2 / Y3 切分
10. 元件 To-Be 整合：每元件的 To-Be 設計概要納入藍圖
11. Dependency graph 繪製
12. CXO 共識營：高階確認藍圖
13. 預算估算 + 風險清單

### 典型產出（按邏輯順序）

1. 訪談摘要 + 痛點地圖
2. 戰略對齊判讀
3. 能力 gap 雷達圖（按 7 元件）
4. 方案卡集（依元件分類）
5. 方案優先序排序矩陣
6. 三期施工藍圖（含 dependency graph、應用成熟度路徑、frontier 對齊）
7. 預算表 / 資源強度表
8. 風險清單與 mitigation
9. CXO 共識備忘錄
10. 企業級 AI 戰略書（彙整以上）

## 建置案（修挑刺 2：不是 N/A，是「指揮 / 監督 / 整合」）

### 典型工作項目

1. PMO 設置 / 跨元件依賴管理
2. Quarter review 機制
3. 預算追蹤
4. 元件案進度整合
5. 滾動修訂藍圖（年度更新）

### 典型產出

1. 季度滾動報告
2. 跨元件 dependency 異動紀錄
3. 年度修訂藍圖

---

# #2 組織人才

## 顧問案

### 典型工作項目（按順序）

1. 現況組織盤點（既有 IT / Data / AI 相關角色與 reporting line）
2. 高階意圖訪談（CDO / CAIO / CRO / CIO / CTO 對 AI 組織的設想）
3. 標竿對標（7+ 同業 / 跨業）
4. AI 高階組織架構設計（C-suite 角色、治理委員會）
5. CoE 型態選擇（central / federated / hub-and-spoke）
6. CoE 職能設計（治理 / 平台 / AI 工程 / 教育 / use case incubation）
7. CoE 與 BU / IT / Data / Risk 的 RACI 介面設計
8. 預算所有權設計（CoE 中央 vs BU 分攤）
9. AI 角色職涯體系設計（既有升級 + 新角色 + 等級認證）
10. 薪酬設計建議（市場行情比對 + 留才 incentive）
11. AI 教育體系設計（分層學習路徑 + 認證）
12. 文化與變革管理計畫（思維轉型 + 宣導 + 抗拒處理）
13. 績效設計（新角色 KPI + 跨部門合作 KPI）
14. 法規 / 工會應對策略
15. 與 #5 治理介面釐清（RAI / Ethics board 歸屬）

### 典型產出（按邏輯順序）

1. 現況組織圖 + reporting line 盤點報告
2. 標竿對標分析
3. To-Be AI 高階組織架構圖
4. CoE 設計書（型態 + 職能 + RACI + 預算）
5. AI 角色職涯路徑（含等級 × 認證矩陣）
6. 薪酬建議書
7. AI 教育體系設計
8. 變革管理計畫
9. 績效設計建議
10. 員額配置表
11. 招聘 / 留才策略
12. 工會 / 法規應對備忘錄

## 建置案

### 典型工作項目（按順序）

1. 教育訓練實際開課（分層）
2. CoE 招募
3. CoE 站立首季 coach
4. 認證制度上線
5. 文化宣導活動執行
6. 績效制度落地

### 典型產出

1. 訓練完成證書 / 出席紀錄
2. CoE 運作起來（首批人員到位）
3. 已通過認證的人員清單
4. 變革滿意度調查
5. AI 文化指標（員工 AI 工具使用度、bottom-up innovation 件數）

---

# #3 AI Ready Data（含 Ontology）

## 顧問案

### 典型工作項目（按順序）

1. 業務目標與場景對焦（與 #1 / #6 對齊）
2. 既有資料盤點（資料源 / 系統 / 格式 / 量級）
3. Data Asset Catalog 設計
4. Metadata 標準設計
5. 資料品質現況評估（事前 / 事中 / 事後）
6. 非結構化資料盤點（文件 / 影像 / 錄音 / 對話 log）
7. Ontology 設計（Object Type / Property / Link Type / Action Type）
8. 雲地混合架構建議
9. Data Mesh vs 中台 vs 混合策略選擇
10. Vector DB 戰略設計
11. 資料治理組織與流程建議（與 #5 介接）
12. 技術選型建議（IBM / 開源 / 三朵雲）
13. 預算 / 資源強度估算

### 典型產出（按邏輯順序）

1. 資料源盤點報告
2. Data Asset Catalog 草版
3. Metadata 標準
4. 資料品質報告（事前 / 事中 / 事後 缺口）
5. Ontology Schema 草版
6. To-Be 資料架構圖
7. 雲地混合策略
8. Vector DB 戰略
9. 技術選型報告
10. 治理流程建議
11. 預算

## 建置案

### 典型工作項目（按順序）

1. Ontology 平台選型 + 部署
2. Data Pipeline 建置（ELT / 流式）
3. Metadata 平台部署
4. Data Quality 工具部署 + rules 設定
5. Vector DB 建置 + Embedding pipeline
6. 資料治理流程上線（搭 #5）
7. 監控 + 警報配套
8. 試點業務場景驗證

### 典型產出

1. Working Ontology
2. 自動化 pipeline
3. Metadata 平台
4. 品質監控儀表板
5. Vector DB 上線
6. 治理流程運作中

---

# #4 Data & AI 平台工具（傘）

> 性質：傘元件。涵蓋全企業 data / ML / LLM / Agent / Ops / Governance 所有工具。設計時要先聽其他元件需求，再做選型整合。

## 顧問案

### 典型工作項目（按順序）

1. 與 #1 / #2 / #3 / #5 / #7 對齊（傘元件先聽需求）
2. 既有工具盤點（含影子 IT）
3. 需求 vs 工具能力差距分析
4. 工具分類設計：
   1. Data 工具
   2. ML 工具
   3. LLM 工具
   4. Agent 工具
   5. Ops 工具
   6. Governance 工具
5. 選型評估（IBM watsonx + 開源 + 三朵雲 整合策略）
6. 整合架構設計
7. 權限 / 安全 / 隱私規劃
8. 成本分析 / TCO 估算
9. 整合 roadmap

### 典型產出（按邏輯順序）

1. 既有工具盤點報告
2. 需求 vs 能力 gap 分析
3. 平台架構圖（按 6 類工具分區）
4. 選型報告
5. 整合架構設計書
6. 權限 / 安全設計
7. TCO 報告
8. 整合 roadmap
9. 預算

## 建置案

### 典型工作項目（按順序）

1. 平台部署（依 roadmap，分批）
2. 工具整合驗證
3. 權限 / 安全配置
4. 監控配套部署
5. 跨工具編排（如 watsonx + Snowflake + Databricks）
6. 試點驗收

### 典型產出

1. 上線平台（分階段）
2. API gateway / 整合層
3. 權限 / 監控配套
4. 工具編排 workflow

---

# #5a AI 治理 — 基礎建設

## 顧問案

### 典型工作項目（按順序）

1. 治理現況評估（既有 ML / Risk / Compliance 框架）
2. 法規 / 標準 mapping（金管會 / NIST / ISO 42001）
3. AI 應用清單盤點 + 風險分級
4. 控制項 gap 分析
5. 三道防線組織建議
6. 准入評估表（A08 等）骨架設計
7. 控制項擴充清單（含 Agent 控制項）
8. Playbook 結構設計
9. 案例說明書結構設計

### 典型產出（按邏輯順序）

1. 治理現況評估報告
2. 法規 mapping 表
3. 風險分級表
4. 控制項 gap 報告
5. 三道防線組織建議書
6. A08 准入評估表（草版）
7. 控制項擴充清單（草版）
8. Playbook 骨架
9. 案例說明書骨架
10. 治理藍圖（含三期 milestone）

## 建置案

### 典型工作項目（按順序）

1. Playbook 完整版撰寫
2. A08 表單上線（系統化）
3. Agent 控制項 Excel 完成
4. 案例說明書（首個案例）
5. 首個審核委員會運作
6. 證據留存系統建置

### 典型產出

1. 完整 Playbook
2. 運作中審核機制
3. 可被審計的證據鏈
4. 首批通過審核案例

---

# #5b AI 治理 — 專案推廣

> ⚠️ **無獨立建置案**——必 piggyback 在 #6 場景案。修挑刺 3。

## 顧問案

### 典型工作項目

1. 選 governance 試點專案（高 / 中風險各 1）
2. 設計 gate review 流程
3. 在 #6 場景案中嵌入 governance gates 的設計
4. 跨 BU 協作機制設計

### 典型產出

1. Gate review 設計書
2. 試點專案清單
3. 嵌入 #6 場景案的 governance checklist

## 建置案（piggyback 在 #6）

- **工作項**：在 #6 case 中嵌入 governance gates、跑首輪審核、迭代制度
- **產出**：已通過 gate 的案例 + 改進制度紀錄

---

# #5c AI 治理 — 技術移轉 / 學院

## 顧問案

### 典型工作項目

1. 內部教育訓練設計
2. 認證體系設計
3. 長期 advisory 計畫
4. KM 結構設計

### 典型產出

1. 訓練教材
2. 認證體系
3. Advisory 計畫書
4. KM 結構

## 建置案

### 典型工作項目

1. 開課
2. 長期 coach
3. KM 上線
4. 認證考核

### 典型產出

1. 培訓完成 / 認證人員
2. KM 運作
3. 客戶可自主迭代的能力實證

---

# #6 +AI / AI+ 場景流程再造

## 顧問案

### 典型工作項目（按順序）

1. 業務流程建模（As-Is L1-L5）
2. 痛點識別 + 機會點識別
3. 流程 redesign（To-Be）
4. 實體建模（Object / Entity，業務語意）
5. 效益估算
6. PoC 設計（範圍 / 資料 / 模型 / 評估指標）
7. HITL 設計（人介入點 / 審核 SOP）
8. Risk assessment（與 #5 對齊）

### 典型產出（按邏輯順序）

1. As-Is 流程圖（L1-L5）
2. To-Be 流程圖
3. 實體模型 / 業務 Object 字典
4. 效益估算表
5. PoC 建議書
6. HITL workflow design
7. Risk register

## 建置案

### 典型工作項目（按順序）

1. PoC 開發
2. PoC 驗證 / iterate
3. Pilot 部署
4. 上線
5. 評估 + 迭代
6. 規模化擴散

### 典型產出

1. PoC 結果報告
2. Pilot 上線
3. 正式上線場景
4. 效益實證
5. 運作中 HITL workflow

---

# #7 Ops（Data / ML / LLM / AgentOps）

## 顧問案

### 典型工作項目（按順序）

1. Ops 現況評估（人 / 流程 / 工具）
2. SOP 設計（lifecycle 各階段）
3. Roles & responsibilities 設計
4. 工具配對（與 #4 介接）
5. 治理整合點設計（與 #5 介接）
6. 評估方法論設計（含 evals harness）
7. 監控與觀測設計

### 典型產出（按邏輯順序）

1. Ops 現況評估報告
2. Ops Playbook
3. SOP 文件
4. Roles 表
5. 工具配對建議
6. 評估方法論
7. 監控架構

## 建置案

### 典型工作項目（按順序）

1. CI/CD pipeline 部署（ML / Agent）
2. 評估流水線部署
3. 觀測平台部署
4. 首批 Ops 工程師陪跑
5. 首批 ML / Agent 通過完整 lifecycle

### 典型產出

1. Ops 平台運作
2. 首批 ML / Agent 通過 lifecycle 紀錄
3. 評估報告
4. 觀測儀表板

---

# 自我挑刺（Critical 7）

## 結構性錯誤

### 挑刺 1：「顧問 vs 建置」二元分類太粗
實務至少 5 類：
1. 純顧問（report → walk away）
2. 顧問 + 試點（驗證後走）
3. 純建置（接 spec 蓋）
4. Build-Operate-Transfer（蓋完幫跑一段時間再轉移）
5. 長期 advisory / managed service

→ v0.3 應改成「模式光譜」，每元件標出 default 模式。

### 挑刺 2：#1 「建置 N/A」是錯的（v0.2 已修）
原寫 N/A，已修為「指揮 / 監督 / 整合」（PMO + Quarter review + dependency 管理 + 年度修訂藍圖）。

### 挑刺 3：#5b 無獨立建置案（v0.2 已修）
原寫獨立列，已改標 piggyback 在 #6。

### 挑刺 4：NSL 殘影 vs 2026 新東西沒區分
表內很多敘述（DataOps 教育訓練、中台架構）是 2022 詞彙。2026 該補但目前沒對應元件的東西：
1. Agentic Workflow 設計
2. LLM Selection 戰略
3. Vector DB 戰略
4. Evaluation framework / Evals harness
5. Prompt management
6. Agent Marketplace strategy
7. RAI SDK 整合
8. Multi-agent orchestration
9. HITL 設計
10. Agent Memory 設計
11. Tool use design
12. MCP / A2A 協定整合

→ 這些塞進哪個元件？v0.3 待 Livia 裁決。

## 缺欄位

### 挑刺 5：缺「典型專案規模 / 人月 / 工期」
影響哪元件能單賣小客戶、哪元件只能整合賣大客戶。Phase 4 賣法決策樹一定會用到。

### 挑刺 6：缺「IBM 內部 owner」
不同元件 IBM 內部 owner 不同（Consulting / Software-watsonx / Infra / IX / Research）。影響可不可同案綁賣、計費、跨 IBM 協調成本。governance 「夾賣」剛性路徑就是此欄位的應用。

## 用途不明

### 挑刺 7：表的目的不明
- catalog（給客戶看的菜單）？
- process（給銷售用的流程指南）？
- training（給 IBM 新顧問）？

三種用途欄位設計差很多。**先定用途再定欄位**。

---

# Backlog 挑刺（次要，待主軸定後處理）

1. 只 #5 拆 3 子分類其他不拆，一致性問題
2. #4 與 #7 建置案重疊嚴重（要不要明確標「必同案」）
3. #3 與 #4 Ontology 雙重歸屬未解
4. #7 Ops 顧問 vs 建置分界模糊
5. 沒體現「客戶買的順序」（藍圖第一買，然後分批）
6. 沒納入 sustainability（上線後客戶能不能繼續跑）
7. +AI vs AI+ 精確切分還沒答（Q6 未回）

---

# Open Questions 給 Livia 裁決

## 關於藍圖（Q1 follow-up）

### 藍圖深淺
- 「高層敘事 deck」還是「詳細施工 spec」？或兩種版本？
- 2026 版頁數應該是 NSL 的 1.5-2 倍合理嗎？

### 新增該出現的東西（2026 vs 2022）

1. 元件之間 dependency graph
2. 應用成熟度路徑（T1-T5 / M1-M5）
3. Frontier 對齊狀態（Agent / Ontology / RAG / Eval placement）
4. Risk register（含 model risk / agent risk / regulatory risk）
5. Capability bet vs incremental ROI 雙曲線

→ 這些對嗎？還缺什麼？

## 關於組織人才完整 track（Q2 follow-up）

我列的 9 區，請補刪：

1. AI 高階組織架構（C-suite、治理委員會、CoE vs BU 權力）
2. CoE 設計（型態 / 職能 / RACI / 預算所有權）
3. AI 角色職涯體系（既有升級、新角色、薪酬、流動）
4. AI 教育體系（分層學習、認證、Center of Education）
5. AI 文化與變革管理（思維轉型、宣導、抗拒處理）
6. AI 績效設計（新角色 KPI、AI-相關 KPI、跨部門 KPI）
7. AI 人才招聘 & 留才（招聘策略、留才、夥伴管理）
8. 法規與工會應對（取代人力、工會溝通、勞動法）
9. 與 #5 治理介面（RAI / Ethics board 屬誰）

→ 哪些對 / 漏 / 不該歸這 track？

---

# 變更紀錄

| 版本 | 日期 | 變動 |
|---|---|---|
| v0.1 | 2026-05-04 | 初稿（表格 + 頓號），含 7 critical + 7 backlog 挑刺 |
| v0.2 | 2026-05-04 | 改分節編號清單格式，保留順序；修挑刺 2、3；新增 Open Questions 區 |
