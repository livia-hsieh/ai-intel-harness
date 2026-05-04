# [SNAPSHOT] Frontier Vocabulary Arbitrage 七槓桿框架

> **這是 2026-05-03 凍結快照,不再修訂。**
> Canonical version: `/Users/liviahsieh/Library/CloudStorage/OneDrive-IBM/AI 知識庫/wiki/perspectives/frontier-vocabulary-arbitrage-7-levers.md`
> 任何後續修訂請改 canonical 版本。本副本存在的目的:讓本專案資料夾保持自洽完整紀錄,任何人讀本專案不需翻閱 AI 知識庫即能理解 Session 1 產出。

---

## 一、核心主張(Meta-Insight)

### 「Frontier Vocabulary Arbitrage」

買家透過 newsletter / X / Bloomberg / a16z 等通路接觸到 frontier lab(Anthropic、OpenAI、Palantir、Google DeepMind)生產的新詞彙,但他自己的 IT 團隊 / 顧問來源 / 內部 RFP 模板還在用 18~24 個月前的詞彙(數據治理、AI 平台、轉型藍圖、CoE)。**這 18~24 個月就是套利空間**——你用 frontier 的詞彙說同一件事,買家會把 frontier 公司的可信度自動轉嫁到你身上。

底層真理(capability stack)其實沒有變,但交付給買家的「敘事原子」可以也應該換掉。舊框架(IBM 6 大 AI 營運核心能力)的問題不是錯,是包裝層 audience-mismatched:對 IT 落地團隊有用(合規檢核表),對讀 frontier 的 CEO/CDO 是反向訊號。

### 觀察觸發點

Livia 同儕將 IBM 6 大能力重組為「Agent Engineering 藍圖」三原子:

| 原子 | 對應的買家心結 | 借用的 frontier 公司品牌 |
|------|--------------|------------------------|
| **Agent marketplace** | 「未來能不能自建?」(vendor lock-in 焦慮) | Google Gemini Enterprise、Oracle AI Agent Marketplace、Salesforce AgentExchange |
| **Ontology** | 「我的非結構化資料是死資產嗎?」 | Palantir Foundry Ontology(2026-02 GA + AIP Document Intelligence) |
| **Harness** | 「能 fast 又 safe 嗎?」(治理+HITL 的新包裝) | Anthropic agent harness 定義 |

對 CTBC 中信網銀/行銀單位,進一步把藍圖橫向展開為 MVP/Y1/Y2/Y3 時間軸,內涵替換為「網銀/行銀殺手級應用」「行銀轉型三階段」等。

---

## 二、七個槓桿

**槓桿一:Frontier 詞彙套利** — 用 frontier lab 每 12~18 個月生產的新詞彙說同一件事,把 frontier 公司的可信度自動轉嫁過來。舊框架借的是 IBM/麥肯錫顧問可信度,在 2026 年是負債而非資產(對 frontier-aware 買家)。

**槓桿二:Capability Slab → Atom Kit** — 舊框架是整板,少一塊就破。新框架是原子套件,每個原子可獨立、可重組。對 CTBC 行銀抽出 Agent marketplace、對風控長重押 Harness、對資料長重押 Ontology——同樣三原子,三種講法。

**槓桿三:每個原子對應一個買家心結** — 舊框架對所有焦慮平鋪解答(menu),新原子是每個焦慮給一個利器(prescription)。買家想要的是「你聽懂我了」不是「你包山包海」。設計新原子前自問:這在哪個買家心裡會 click?

**槓桿四:Engineering-Coded 語言取代 Transformation-Coded** — 「Agent Engineering 藍圖」這個標題暗示我們會 ship 系統不是賣 ppt。Transformation / blueprint / operating model 在 2026 年的銀行 CTO 耳裡是顧問鬼話。動詞改名詞,是把賣方從「顧問」重新定位成「工程團隊」,連鎖影響 SOW、人月、交付節奏。

**槓桿五:時間軸取代組織軸** — 舊框架橫軸是組織(前台/中台/後台),對 IT 有用,對 CEO 是反向訊號。新框架橫軸是時間(MVP/Y1/Y2/Y3),天然帶有「進步、壓力、節奏」的隱喻。

**槓桿六:借用 Frontier 公司品牌信用,但限縮承諾** — 不是「我們是 Palantir」,而是「我們用同一套思維」。距離很重要:讓買家有對標 + 給賣方差異化。

**槓桿七:讓買家自己投射** — 不寫死 KPI,讓買家自己投射「我家的 Ontology 應該長什麼樣」。投射的東西買家會更愛護(IKEA 效應)。

---

## 三、四個失效條件(冷水)

1. **詞彙套利會貶值** — 2027~2028 這些詞會被 IBM/Accenture 收割成顧問詞彙再變回負債。真正肌肉是「持續刷新詞彙」這個元能力,不是這三個字。
2. **包裝拉高了實質期待** — 打 Ontology 牌就要答得出「跟 Palantir Foundry 比怎樣」。借來的信用是有條件的:條件是你真的在這個語言系統裡面活著。
3. **極度仰賴買家 sophistication** — CTBC 行銀吃這套(讀 frontier),區域銀行徵授信主管不一定吃。**不是新框架取代舊框架,而是必須兩套並存,瞬間判斷端哪一套**。
4. **不要貶低舊圖** — 舊 6 大能力對 IT 落地團隊、PMO、稽核仍有用。問題是用錯場合。內部要有「分層敘事庫」:同方案 × 多 persona。

---

## 四、實作 Routine(每週 30 分鐘)

| 步驟 | 內容 | 輸出 |
|------|------|------|
| 1. 收詞 | 從 Anthropic / OpenAI / Palantir / a16z / Google DeepMind 各挑一篇,每週收集 3 個新詞 | 詞彙帳本兩欄:(a) frontier 公司用此詞解什麼?(b) 我的方案哪一塊在解類似問題? |
| 2. 翻譯練習 | 挑一張舊版簡報,用本週新詞重組一頁 | 重組簡報頁(把 capability 拆成原子,每原子對應一個買家心結) |
| 3. 轉軸練習 | 同一原子套件對 CEO / CTO / 稽核長三人各講一遍 | 三版口條(原子相同,故事不同) |
| 4. 壓力測試 | 找扎實同事(或 LLM)扮挑剔買家,問「你的 X 跟 Palantir 的差在哪?」 | 標準答案表 |

---

## 五、跟既有概念的連結

- **[[digital-transformation-framework]]**(concepts):七槓桿是 digital transformation 框架的「對話腳本」延伸層;該頁的三層次模型(L1/L2/L3)是原子重組的座標
- **[[e2e-playbook-v2]]**(concepts):「atom kit vs. slab」與 V2 漸進漏斗設計哲學相通

## 六、待驗證

⚠️ 萃取自第三方觀察(Livia 同儕對 CTBC 的 reframe)+ 對話分析,**Livia 尚未在自己客戶專案實戰驗證**。建議下一個合適銀行案做第一次實戰,反饋回填 canonical 頁的「使用紀錄」(尚未建立的區塊)。

## 七、未解問題

- 「持續刷新詞彙」除了每週看 frontier blog,有無更高槓桿訓練方式
- 在更保守(政府)或更 sophisticated(半導體 R&D)產業,原子組合是否需不同設計
- 此方法論於 Livia 自身求職場景(harness engineer)的應用,可能是反向:對潛在雇主套用 engineering-coded 語言 + atom kit
- 「分層敘事庫」(同方案 × 多 persona)的工程實作 still open
