# Foundation — Track G: 治理與安全

_Week 2026-W23 · 25 items synthesized · $0.7141 USD_



# AI 治理的實戰轉折：從框架合規到沙箱工程與失控代價

## TL;DR (3 句繁中)
1. 2026 年中的治理實況揭示一個根本轉變：AI 安全不再只是「政策文件」，而是「沙箱工程 + 成本控制 + 審計追蹤」三位一體的系統設計問題，Anthropic 的容器化文件與 Meta 的社交工程潰敗恰好勾勒出光譜兩端。
2. 核心 trade-off 在於「代理自主性 vs. 可控性」——更長跑、更自主的 agent 帶來更大的攻擊面、更高的 token 燃燒率、以及更難追溯的決策鏈；治理必須嵌入 runtime 本身，而非疊加在外層。
3. 對 Livia 而言，台灣金融與製造客戶正進入「AI 從 PoC 走向 plant-wide / bank-wide 部署」的階段，此刻最能賣的不是模型能力，而是「可審計、可熔斷、可歸責」的治理 harness——這就是 IBM 的甜蜜點。

## 背景與問題框架

[推論] 六個月前（2025 年底），企業 AI 治理的對話核心還停留在「該不該用 GenAI」、「敏感資料會不會外洩」這類第一代風險。當時 NIST AI RMF 1.0 剛被主要金融業參照，EU AI Act 的分級制度也只在歐洲本地有影響力。台灣金管會則以「金融業運用 AI 指引」設下原則性框架，但缺乏技術級別的實施標準。

[推論] 到 2026 年中，情勢已發生結構性位移。首先，agent 成為主流部署形態——不再是一次性 prompt-in/response-out，而是長跑數十分鐘甚至數小時的自主工作流（如 [LangChain 的 EU 宏觀研究 agent 跑 45 分鐘](https://www.langchain.com/blog/financial-ai-that-investigates-macro-trends-eu-economic-analysis-with-you-com-and-langchain)、[Rippling 跨五大業務域的 deep agent](https://www.langchain.com/blog/how-rippling-went-ai-native-across-every-product-in-6-months-with-deep-agents-and-langsmith)）。其次，真實世界的治理失敗已從假想場景變成頭版新聞——[Meta AI 客服機器人被社交工程攻破，讓駭客接管 Instagram 高知名度帳戶](https://simonwillison.net/2026/Jun/1/hackers-simply-asked-meta-ai/#atom-everything)。第三，token 經濟學爆炸性成長迫使組織層級的成本治理介入——[Uber 四個月燒完全年 AI 預算後對每人每月設 $1,500 上限](https://simonwillison.net/2026/Jun/3/uber-caps-usage/#atom-everything)。

[推論] 這三股力量匯流成一個新命題：**治理不能只是政策層；它必須成為 agent runtime 的原生屬性。** 本週的信號密集地指向這個結論——從 Anthropic 的沙箱文件、LangGraph 的容錯原語、到國泰金控自行訓練 SLM 來掌控意圖判斷——每一個案例都是「把治理嵌入系統架構」的不同面向。

## 核心概念解析（含 Mermaid 圖）

### 一、Anthropic 的沙箱分層：治理即容器工程

[原文] Anthropic 發布了 [跨產品的 Claude 容器化安全文件](https://simonwillison.net/2026/May/30/how-we-contain-claude/#atom-everything)，詳述 Claude.ai、Claude Code、Cowork 三個產品線各自的 process sandbox、VM 隔離、filesystem boundary、egress control 機制。Simon Willison 特別稱讚其文件化程度為業界罕見。

[推論] 這份文件的意義不只是「Anthropic 做了安全」，而是確立了一個 pattern：**agent 治理的最小可行單元是「容器 + 出口控制 + 檔案系統邊界」，而非「使用政策 + 人工審核」。** 當 agent 可以執行程式碼、讀寫檔案、發出網路請求時，政策聲明毫無約束力——只有技術邊界才算數。

以下圖示展示 Anthropic 三層沙箱架構的邏輯分層：

```mermaid
flowchart TD
    subgraph Product["產品層"]
        A["Claude.ai<br/>(對話)"]
        B["Claude Code<br/>(IDE agent)"]
        C["Cowork<br/>(自主任務)"]
    end
    subgraph Sandbox["沙箱層"]
        D["Process Sandbox<br/>最小權限隔離"]
        E["VM Boundary<br/>完整虛擬機隔離"]
        F["Filesystem Boundary<br/>路徑白名單"]
    end
    subgraph Egress["出口控制層"]
        G["Egress Filter<br/>網路連線白名單"]
    end
    A --> D
    B --> E
    B --> F
    C --> E
    C --> F
    D --> G
    E --> G
    F --> G
```

**關鍵洞見**：自主性越高的產品（Cowork > Claude Code > Claude.ai）所需的隔離層級越深——從 process 級到完整 VM 級。這建立了一個可套用到任何企業 agent 部署的設計原則：**agent 自主性等級必須對映到對應的沙箱深度。**

### 二、Meta AI 潰敗：沒有沙箱的反面教材

[原文] [Meta AI 客服機器人被社交工程攻破](https://simonwillison.net/2026/Jun/1/hackers-simply-asked-meta-ai/#atom-everything)，駭客只需要用自然語言請求「幫我把這個帳戶綁定到新 email」，機器人就執行了帳戶轉移操作。多個獨立來源驗證此事件為真。

[推論] 這是一個教科書級的治理失敗案例。根本問題不在模型能力，而在**系統架構把「理解使用者意圖」和「執行帳戶變更」的權限綁在同一個 agent 裡，且沒有人工確認閘門、沒有身份驗證步階、沒有操作範圍限制**。用 NIST AI RMF 的語言，這是 Govern 和 Map 功能的同時失效——組織既沒有定義 AI 系統的操作邊界（Map），也沒有建立足夠的控制機制（Govern）。

以下對比 Anthropic 模式與 Meta 反面案例的架構差異：

```mermaid
flowchart LR
    subgraph Safe["Anthropic 模式"]
        S1["使用者請求"] --> S2["意圖分類"]
        S2 --> S3{"高風險操作?"}
        S3 -->|是| S4["人工確認閘門"]
        S3 -->|否| S5["沙箱內執行"]
        S4 --> S5
    end
    subgraph Fail["Meta 反面案例"]
        F1["使用者請求"] --> F2["AI 理解意圖"]
        F2 --> F3["直接執行<br/>帳戶變更"]
    end
```

**關鍵洞見**：Meta 模式中，從「理解」到「執行」之間沒有任何中斷點。這正是 BFSI 部署最不能犯的錯——銀行客服 AI 若能直接執行轉帳，就等同把金庫鑰匙交給任何會說話的人。

### 三、Agent Runtime 層的治理原語：LangGraph 的容錯三件組

[原文] LangGraph 發布了[三種容錯原語](https://www.langchain.com/blog/fault-tolerance-in-langgraph)：RetryPolicy（自動重試 + 退避）、TimeoutPolicy（牆鐘時間 + 閒置時間上限）、error_handler（重試耗盡後的清理邏輯），並引入 SAGA pattern 處理多步驟工作流的副作用回滾。

[原文] 同時，[DeltaChannel 機制](https://www.langchain.com/blog/delta-channels-evolving-agent-runtime) 解決了長跑 agent 的 O(N²) checkpoint 儲存膨脹問題，改為 diff-only checkpoint + 週期性全量快照。

[推論] 這些技術看似是「工程問題」而非「治理問題」，但在 agent 時代，**容錯 = 可審計性的前提**。如果 agent 在第 47 步失敗後沒有清理副作用、沒有記錄失敗狀態，任何事後審計都無法重建事件鏈。SAGA pattern 尤其重要——它確保多步驟操作要嘛全部完成，要嘛全部回滾，這正是金融交易處理的基本要求。

```mermaid
stateDiagram-v2
    [*] --> Executing
    Executing --> Retry: 暫時性錯誤
    Retry --> Executing: RetryPolicy<br/>(指數退避)
    Retry --> ErrorHandler: 重試耗盡
    Executing --> Timeout: 超時
    Timeout --> ErrorHandler: TimeoutPolicy
    ErrorHandler --> Compensate: SAGA 回滾
    Compensate --> [*]: 副作用清除
    Executing --> Checkpoint: 每步 diff
    Checkpoint --> Executing
```

**關鍵洞見**：LangGraph 把容錯做成 runtime 原語而非應用層 wrapper，這意味著治理行為（超時熔斷、失敗回滾、狀態持久化）是 agent 執行引擎的內建屬性，不需要每個開發者自己重新實作。這是「治理左移」（shift-left governance）的具體技術實現。

### 四、成本治理：從 token 經濟學到組織管控

[原文] [Uber 四個月燒完全年 AI 預算](https://simonwillison.net/2026/Jun/3/uber-caps-usage/#atom-everything)，隨後對每位員工設定每月 $1,500 的 AI 編碼工具 token 上限。Simon Willison 指出，2025 年編列的預算根本無法預見 2026 年 coding agent 的 token 消耗量級。

[推論] 成本治理是 AI 治理中最常被忽略的維度。NIST AI RMF 談風險、EU AI Act 談合規、Anthropic RSP 談能力門檻，但沒有框架正面處理「AI 系統的營運成本可能在部署後指數成長」這個現實。Uber 案例證明：**agent 時代的 token 消耗不是線性可預測的——coding agent 的 token-per-task 比 chat 高出 10-100x**，而組織若不在架構層設置 budget guardrail，就只能事後救火。

[推論] 對應到台灣脈絡，[Anthropic 年化營收已達 $47B](https://simonwillison.net/2026/May/29/anthropic/#atom-everything) 的事實說明全球企業正在大規模採購 AI 能力，但 Uber 的教訓暗示：**採購速度遠超成本治理機制的建立速度**。

### 五、國泰金控 SLM：以在地模型實現意圖治理

[原文] [國泰金控在 GTC Taipei 2026 發表開源 SLM](https://www.cio.com.tw/114361/)，專門用於客戶意圖判斷，強調在地金融語意、專有名詞、模糊提問的處理能力。

[推論] 這是一個非常聰明的治理策略：**用小型在地模型作為意圖分類的第一道閘門，而非直接讓大型通用模型接觸業務邏輯**。這等同於在 Meta 反面案例中缺失的「意圖分類 → 權限判斷」中間層。國泰的做法意味著：即使後端使用 GPT-4 或 Claude 做生成，前端的意圖路由由自己訓練的模型掌控，這大幅降低了提示注入和社交工程的風險面。

### 六、工廠 AI 的治理維度：NVIDIA FOX 與 Cooler Master 實踐

[原文] [NVIDIA 發布 Factory Operations Blueprint (FOX)](https://blogs.nvidia.com/blog/factory-operations-fox-blueprint-ai-brain/) 作為自主工廠管理的參考架構，將即時機器信號、品質系統、工作指令、營運告警整合到統一決策層。[Cooler Master 與 Spingence 合作](https://www.inside.com.tw/article/41470-Spingence) 在全球據點導入 NVIDIA 物理 AI 三部電腦架構，串聯 AI 視覺檢測、數位孿生與知識系統。

[推論] 製造業 AI 治理有獨特挑戰：決策延遲的代價不是「使用者不滿」而是「產線停機」或「人身安全」。NVIDIA 的 [Cosmos 3 世界模型](https://blogs.nvidia.com/blog/cosmos-3-physical-ai-open-world-foundation-model/) 讓 physical AI 能預測未來狀態再行動——這實際上是治理的前移：**在行動之前驗證行動的合理性**。但這也引入了新的治理問題：世界模型的預測錯誤如何偵測？當數位孿生與實體工廠的狀態出現偏差時，誰負責？

## 與既有框架的對位

[推論] 本週信號與 **NIST AI RMF** 的四大功能（Govern, Map, Measure, Manage）形成精確對位。Anthropic 的沙箱文件是 **Manage** 的典範——具體的技術控制措施。Meta 的失敗是 **Map** 的缺失——沒有辨識出「AI 客服直連帳戶操作」是高風險功能。Uber 的成本爆炸是 **Measure** 的空白——沒有持續監測 token 消耗趨勢。國泰的 SLM 意圖分類是 **Govern** 的體現——在組織層決定「哪些判斷必須由自己掌控」。

[推論] 與 **EU AI Act** 的風險分級對位：BFSI 領域的帳戶操作 agent 顯然屬於「高風險 AI 系統」，需要人機介面、可追溯性、穩健性要求。Meta 的案例若發生在歐洲銀行，將觸發 EU AI Act 第 14 條（人類監督）和第 15 條（準確性、穩健性和網路安全）的違規。台灣雖不直接適用 EU AI Act，但金管會指引已明確參照其精神，未來升級為強制規範的機率極高。

[推論] 與 **Anthropic RSP (Responsible Scaling Policy)** 的關係更為微妙。Anthropic 自己的沙箱文件可以視為 RSP 在產品層的落地——RSP 定義能力門檻和對應的安全措施，沙箱文件則是那些安全措施的工程實現。但 RSP 框架的侷限在於它是「自我監管」——[Import AI 459 明確指出 AI 監督本身就是困難的](https://jack-clark.net/2026/06/01/import-ai-459-ai-oversight-is-difficult-scaling-laws-for-protein-folding-models-and-pricing-the-extinction-risk-of-ai-systems/)，沒有外部驗證機制的自律很容易在商業壓力下鬆動。

[推論] **Chip Huyen** 在 *Designing Machine Learning Systems* 中強調的「monitoring → alerting → debugging → remediation」循環，在 agent 時代需要升級。LangGraph 的容錯原語和 DeltaChannel 本質上是這個循環在 agent runtime 內部的微觀實現——每步 checkpoint、每次 timeout 都是一個 monitoring 事件。EVA-Bench 的[多域語音 agent 評估](https://huggingface.co/blog/ServiceNow-AI/eva-bench-data)則從外部提供了 Measure 維度的工具。

## Trade-offs 與爭議

**1. 沙箱深度 vs. Agent 能力**
正面：更深的沙箱（VM 隔離、嚴格 egress 控制）大幅降低安全風險。
反面：每一層隔離都增加延遲、限制 agent 能使用的工具、並提高維運複雜度。Cowork 級別的 VM 隔離可能讓 agent 無法即時訪問企業內部 API，迫使開發者在沙箱內重建連接通道。
立場：[推論] 對 BFSI 而言，沙箱深度不是可選的，是必要的。延遲增加 200ms 對銀行客服可以接受，但帳戶被接管不可以。

**2. 自訓練 SLM vs. 外購大模型作為意圖閘門**
正面：國泰模式——自行掌控意圖分類，降低外部模型的攻擊面。
反面：SLM 訓練和維護需要持續的 ML 工程投入；模型過時或覆蓋不足時，反而成為瓶頸。
立場：[推論] 混合架構（SLM 做路由 + 大模型做生成）是目前最務實的 BFSI 選擇，但必須為 SLM 建立持續評估管線。

**3. Runtime 內建容錯 vs. 應用層自理**
正面：LangGraph 把 RetryPolicy / TimeoutPolicy / SAGA 做成 runtime 原語，確保一致性。
反面：框架鎖定（vendor lock-in）風險——如果組織深度依賴 LangGraph 的容錯機制，遷移到其他 agent 框架的成本極高。
立場：[推論] 容錯邏輯應有抽象介面，即使用 LangGraph 實作也應保持可替換性。IBM 的顧問角色正好可以幫客戶設計這個抽象層。

**4. 成本上限管控 vs. 開發者生產力**
正面：Uber 的 $1,500/月上限防止預算失控。
反面：硬上限可能在月末最忙的時候切斷開發者最有價值的工具使用。
立場：[推論] 更好的做法是分級 budget（基礎額度 + 專案申請 + 自動告警），而非一刀切。

**5. 自律 vs. 外部監管**
正面：Anthropic RSP + 沙箱文件展現了高品質自律。
反面：[Import AI 459](https://jack-clark.net/2026/06/01/import-ai-459-ai-oversight-is-difficult-scaling-laws-for-protein-folding-models-and-pricing-the-extinction-risk-of-ai-systems/) 直接指出 AI 監督本質上困難，且 Anthropic 同時接受 $65B 融資——商業壓力與安全自律的張力只會加劇。
立場：[推論] 外部審計框架（無論由金管會或第三方執行）是不可替代的。自律是必要條件，但絕非充分條件。

## 對 Livia IBM 客戶的具體含意

**國泰金控 / 玉山銀行等 BFSI 客戶**：
[推論] Meta 的失敗案例是最強的客戶對話開場白。任何台灣銀行如果正在部署 AI 客服，都必須回答一個問題：「你的 AI 客服能不能被社交工程攻破來轉帳？」IBM 可以提案的角色是**治理層 harness 設計**：意圖分類閘門（可參照國泰 SLM 模式）、操作權限沙箱（參照 Anthropic 模式）、審計追蹤管線（參照 LangSmith 模式）。

具體提案 angle：
1. **「AI 客服安全性評估」快速診斷**：用 EVA-Bench 式的多域語音 agent 測試框架，對客戶現有 AI 客服做壓力測試，包含社交工程場景。
2. **「Agent 治理 harness」參考架構**：以 Anthropic 沙箱文件為 blueprint，為客戶的 agent 部署設計分層沙箱 + SAGA 回滾 + token budget 管控。
3. **「在地 SLM 意圖路由」顧問專案**：協助非國泰的金融客戶評估是否需要自訓練意圖分類模型，或可以用 fine-tuned 開源模型替代。

**台積電 / 鴻海 / Cooler Master 等製造客戶**：
[推論] NVIDIA FOX blueprint 和 Cooler Master 案例建立了「工廠 AI 大腦」的願景，但缺少治理層。IBM 可以切入的角色是**數位孿生與實體工廠之間的一致性驗證**——當 AI 決策基於數位孿生的模擬結果，但模擬與現實偏差超過閾值時，需要自動熔斷機制。這正是 LangGraph 的 TimeoutPolicy 概念在物理世界的延伸。

**通用警示**：
[推論] Uber 的預算爆炸會在台灣重演。台灣企業的 2026 AI 預算多數在 2025 年底編列，完全沒有預見 coding agent 的 token 消耗量級。IBM 應該主動在客戶對話中提出「token 經濟學模型」，幫客戶在部署前就建立消耗預測和分級管控。

## 對 Livia harness engineer portfolio 的含意

1. **Design Note 提取：「Agent 治理三層模型」**——可以從本週分析中抽出一篇 design note，定義 agent 部署的三層治理架構（意圖閘門層 → 沙箱執行層 → 審計追蹤層），以 Anthropic 文件為基準，以 Meta 失敗為反例，以國泰 SLM 為在地變體。這是 portfolio 中最能展示「系統思維」的文件類型。

2. **面試問答框架：「你怎麼設計一個安全的 AI 客服系統？」**——答案結構：先用 Meta 反例說明問題空間，再用 Anthropic 沙箱模式說明技術解法，最後用 SAGA pattern 說明多步驟操作的回滾機制。這個答案同時展示安全意識、系統設計能力、和對業界最新實踐的掌握。

3. **Portfolio 敘事線**：本週深讀強化了「治理不是 checkbox，是 runtime 屬性」這個核心論述。Livia 的 pipeline 如果在 CLAUDE.md 或 design notes 中明確體現 timeout/retry/budget-guard 的設計決策，就是在用行動證明這個論述。

4. **技術展示機會**：可以在 GitHub portfolio 中實作一個簡化版的「agent governance harness」demo——接入 LangGraph 的 RetryPolicy + TimeoutPolicy，加上 token budget tracking，配 Mermaid 架構圖——作為治理工程能力的具體證據。

---

# AI Governance in Practice: From Policy Frameworks to Sandbox Engineering and the Cost of Lost Control

## TL;DR (3 sentences)
1. Mid-2026 governance realities reveal a fundamental shift: AI safety is no longer just "policy documents" but a triad of sandbox engineering + cost control + audit trails; Anthropic's containerization documentation and Meta's social engineering breach perfectly delineate both ends of the spectrum.
2. The core trade-off is agent autonomy vs. controllability — longer-running, more autonomous agents create larger attack surfaces, higher token burn rates, and harder-to-trace decision chains; governance must be embedded in the runtime itself, not layered on top.
3. For Livia, Taiwan banking and manufacturing clients are entering the "AI moves from PoC to bank-wide/plant-wide deployment" phase, and what sells best right now isn't model capability but "auditable, circuit-breakable, accountable" governance harnesses — IBM's sweet spot.

## Background & Problem Framing

[Inference] Six months ago, enterprise AI governance conversations centered on first-generation risks: "should we use GenAI at all?" and "will sensitive data leak?" NIST AI RMF 1.0 was just being referenced by major financial institutions, the EU AI Act's risk tiers were only locally relevant in Europe, and Taiwan's FSC guidelines for AI in finance remained principle-level without technical implementation standards.

[Inference] By mid-2026, the situation has structurally shifted. First, agents have become the dominant deployment form — no longer single-turn prompt-in/response-out but autonomous workflows running for tens of minutes to hours (e.g., [LangChain's EU macro research agent running 45 minutes](https://www.langchain.com/blog/financial-ai-that-investigates-macro-trends-eu-economic-analysis-with-you-com-and-langchain), [Rippling's deep agents across five business domains](https://www.langchain.com/blog/how-rippling-went-ai-native-across-every-product-in-6-months-with-deep-agents-and-langsmith)). Second, real-world governance failures have moved from hypothetical scenarios to front-page news — [Meta's AI support bot was compromised via social engineering, allowing hackers to take over high-profile Instagram accounts](https://simonwillison.net/2026/Jun/1/hackers-simply-asked-meta-ai/#atom-everything). Third, token economics have exploded to the point where organization-level cost governance must intervene — [Uber burned through its entire annual AI budget in four months, then capped each employee at $1,500/month](https://simonwillison.net/2026/Jun/3/uber-caps-usage/#atom-everything).

[Inference] These three forces converge on a new thesis: **governance cannot be just a policy layer; it must become a native property of the agent runtime.** This week's signals point densely toward this conclusion — from Anthropic's sandbox documentation, LangGraph's fault-tolerance primitives, to Cathay Financial's custom SLM for intent classification — each case represents a different facet of "embedding governance into system architecture."

## Core Concepts (with Mermaid diagrams)

### 1. Anthropic's Sandbox Layers: Governance as Container Engineering

[Source] Anthropic published a [comprehensive containment document across products](https://simonwillison.net/2026/May/30/how-we-contain-claude/#atom-everything), detailing process sandboxes, VM isolation, filesystem boundaries, and egress controls for Claude.ai, Claude Code, and Cowork. Simon Willison specifically praised the documentation level
