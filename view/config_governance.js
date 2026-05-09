// AI Governance 賣法 config - 改這裡的字串就能更新展示

const govConfig = {
  meta: {
    title: "AI Governance 賣法",
    version: "v2.0",
    core_one_liner: "治理本身不直接賺錢——所以賣治理 = 找剛性需求附身。",
    summary: "進案路徑 → IBM 角色 + 套餐推薦樹獨立決定 → 依客戶程度調整包裝深淺。",
  },

  // ====== 5 種可賣套餐 ======
  outcomes: [
    {
      id: "GV-A",
      name: "補強升級包",
      maturity: "high",
      maturity_label: "高成熟",
      client_state: "已有完整 AI 內規、已實施",
      key_modules: "M3 機制補強 + M5 工具升級",
      anchors: [],
    },
    {
      id: "GV-B",
      name: "內規重構 + 落地包",
      maturity: "mid",
      maturity_label: "中成熟",
      client_state: "零散內規寫不好",
      key_modules: "基於 M4 既有內規 + M1-M9",
      anchors: [],
    },
    {
      id: "GV-C",
      name: "全套新建 + 落地包",
      maturity: "low",
      maturity_label: "低成熟",
      client_state: "沒內規從零開始",
      key_modules: "M1-M9 全",
      anchors: [],
    },
    {
      id: "GV-D",
      name: "治理工具棧",
      maturity: "tool",
      maturity_label: "工具型",
      client_state: "真的真的只想買工具（罕見）",
      key_modules: "M5 為主",
      warning: "純工具買賣 IBM 顧問賺不到顧問費——客戶說「要工具」時應該主動追問，多半其實該升級到 GV-A/B/C",
      anchors: [],
    },
    {
      id: "GV-E",
      name: "一次性技術檢測",
      maturity: "single",
      maturity_label: "單案型",
      client_state: "只想針對某專案表現驗證",
      key_modules: "M8-M9 技術控制項",
      warning: "若客戶內規不清 → 等同沒內規 → 回到 GV-B 或 GV-C",
      anchors: [],
    },
  ],

  // ====== 進案路徑 ======
  entry_paths: [
    {
      group_id: "A",
      group_name: "IBM 內部賦能",
      group_desc: "純內部議題：建立方法確保 IBM 顧問用 AI 工具做客戶案的品質。沒有對外窗口、沒對外角色、沒對外開場白。",
      paths: [
        {
          id: "A1",
          name: "IBM 內部專案 AI 工具品質保證",
          window: "—",
          frame_id: null,
          default_outcome: "IBM 內部使用，不對外賣",
          opening_hook: "—",
          internal_note: "建立內規與工具品質檢核機制，確保 IBM 顧問用 AI 工具開發給客戶的東西品質有保證",
        },
      ],
    },
    {
      group_id: "B",
      group_name: "客戶端需求",
      group_desc: "客戶情境驅動。從 0 走套餐推薦樹判斷套餐。",
      paths: [
        {
          id: "B1",
          name: "法規驅動",
          window: "CRO / 法遵長",
          frame_id: "compliance_partner",
          default_outcome: "走套餐推薦樹",
          opening_hook: "金管會 / EU AI Act / ISO 42001...",
        },
        {
          id: "B2",
          name: "危機事件後",
          window: "CEO 直線",
          frame_id: "compliance_partner",
          default_outcome: "GV-A 補強 / GV-B 內規重構",
          opening_hook: "您看 X 公司上週 AI 出事...",
        },
        {
          id: "B3",
          name: "M&A 集團整合",
          window: "集團 CEO / CFO",
          frame_id: "group_integrator",
          default_outcome: "GV-B 內規重構 / GV-C 全套新建",
          opening_hook: "併購後 12 個 BU 各做各的...",
        },
        {
          id: "B4",
          name: "認證取證",
          window: "CMO / CEO",
          frame_id: "compliance_partner",
          default_outcome: "GV-B 內規重構 / GV-C 全套新建",
          opening_hook: "ISO 42001 是您出海前必拿的...",
        },
        {
          id: "B5",
          name: "IBM AI 轉型 / 場景案內含治理",
          window: "依客戶角色（CDO / CIO / CRO）",
          frame_id: "compliance_partner",
          default_outcome: "走套餐推薦樹",
          opening_hook: "您買的 IBM AI 案中有一塊是治理...",
        },
      ],
    },
    {
      group_id: "C",
      group_name: "技術前沿驅動",
      group_desc: "新技術出現觸發客戶問怎麼治理。窗口通常是技術主管。",
      paths: [
        {
          id: "C1",
          name: "新技術觸發（multiagent / Claude Code 等）",
          window: "CTO / CDO / RAI",
          frame_id: "tool_provider",
          default_outcome: "GV-A 補強 / GV-E 一次性檢測",
          opening_hook: "您要落地 X 新技術，治理還沒跟上...",
        },
      ],
    },
    {
      group_id: "D",
      group_name: "合作夥伴 Partnership（三朵雲）",
      group_desc: "與雲廠商談合作關係——不是直接客戶路徑，是 IBM 與雲商共同 Go-to-Market。重點談：(1) 與雲商產品/服務整合方式 (2) 雙方利益分配 (3) 共同 GTM。",
      paths: [
        {
          id: "D1",
          name: "三朵雲合作（AWS / Azure / GCP）",
          window: "雲商 BD + 雙方 partnership team",
          frame_id: "tool_provider",
          default_outcome: "GV-D 工具棧（嵌進雲商產品）",
          opening_hook: "與您（雲商）的 X 產品 / 服務結合，補強雲商不擅長的合規 mapping",
        },
      ],
    },
  ],

  // ====== IBM 角色（前 = Frame） ======
  frames: [
    {
      id: "tool_provider",
      name: "工具供應商",
      core_story: "客戶腦袋簡化版：買工具 + IBM 教用 + 技術移轉，客戶的人就會用了。其實 IBM 內部還是要花時間導入完整方法和 operating model——只是不用客戶聽不懂的話講。客戶最終一樣得到完整治理",
      client_concern: "我買的工具夠用嗎？怎麼整合？我的人能不能上手？",
      is_special: false,
    },
    {
      id: "operating_model",
      name: "Operating Model 導入夥伴",
      core_story: "客戶懂 operating model 重要性。表裡一致：客戶語言 = IBM 語言。3 年願景 + AI at Scale 全景 + 治理是規模化前提",
      client_concern: "3 年後我長什麼樣？這個 operating model 對嗎？",
      is_special: false,
    },
    {
      id: "compliance_partner",
      name: "法遵伴侶",
      core_story: "監理機關視角。法規 mapping → 落差 → 控制項 → 三道防線 → 取證 milestone。速度可調：常態走慢、危機走快加上止血→根因→經驗轉化內規",
      client_concern: "常態：我會被罰嗎？認證能拿到嗎？／ 危機：能多快止血？怎麼證明對外處理好了？",
      is_special: false,
    },
    {
      id: "group_integrator",
      name: "集團統合者",
      core_story: "集團一致性 + 風險集中 + 子公司散→拉齊。重點：政治可行性 + 中立第三方",
      client_concern: "子公司會配合嗎？怎麼讓他們不抵抗？",
      is_special: false,
    },
    {
      id: "ai_lab_partner",
      name: "AI Lab Partner（特殊）",
      core_story: "Frontier-aligned。跟 Anthropic / Palantir 對標。Capability bet。Agent / Ontology / Harness / Evals。研發共創",
      client_concern: "我們是不是站在 frontier？跟同業比領先嗎？",
      is_special: true,
      special_note: "99% 案不適用。只在 tier 1 客戶（CTBC / 玉山 / Wistron 等）主動提出新治理觀念時才走",
    },
  ],

  // ====== 套餐推薦樹（即原決策樹一） ======
  decision_tree: {
    name: "套餐推薦樹",
    description: "起點是進案路徑分組（多元入口）→ 客戶採購意圖 → 治理成熟度判斷。內規判斷只在一處：治理成熟度的 5 訊號之一。",
    flat_mermaid: `flowchart TD
    Start[客戶來] --> Path{進案路徑分組}
    Path -->|A 組: IBM 內部賦能| AInt[IBM 內部用<br/>不對外賣]
    Path -->|D 組: 三朵雲合作| DPart[嵌進雲商產品<br/>= GV-D 治理工具棧]
    Path -->|B 組: 客戶端需求<br/>法規/危機/M&A/認證/<br/>IBM AI 案內含治理| Intent
    Path -->|C 組: 技術前沿驅動<br/>multiagent/Claude Code| Intent

    Intent{客戶採購意圖?}
    Intent -->|要工具| ToolDrill{抽絲剝繭追問<br/>有專責角色/SOP/委員會嗎?}
    ToolDrill -->|全部答得出| GVD[GV-D 治理工具棧<br/>罕見]
    ToolDrill -->|答不出| Maturity
    Intent -->|單案技術驗證| Single{內規清楚<br/>可依循?}
    Single -->|清楚| GVE[GV-E 一次性技術檢測]
    Single -->|不清楚| Upgrade[⚠️ 等同沒內規<br/>升級到 GV-B 或 GV-C]
    Intent -->|整體治理 / 要藍圖 /<br/>要顧問 / 模糊| Maturity

    Maturity{治理成熟度判斷<br/>看 5 訊號:<br/>AI 應用面積 / 治理組織 /<br/>內規狀態 / 客戶詞彙 / 採購行為}
    Maturity -->|多數訊號 高| GVA[GV-A 補強升級包]
    Maturity -->|多數訊號 中| GVB[GV-B 內規重構+落地包]
    Maturity -->|多數訊號 低| GVC[GV-C 全套新建+落地包]

    style AInt fill:#e5e7eb,stroke:#6b7280
    style DPart fill:#fef3c7,stroke:#d97706
    style GVD fill:#fef3c7,stroke:#d97706
    style GVE fill:#d1fae5,stroke:#059669
    style GVA fill:#dbeafe,stroke:#1d4ed8
    style GVB fill:#dbeafe,stroke:#1d4ed8
    style GVC fill:#dbeafe,stroke:#1d4ed8
    style Upgrade fill:#fee2e2,stroke:#dc2626`,
  },

  decision_signals: [
    {
      id: "ai_app_scope",
      name: "AI 應用面積",
      values: {
        low: "無 / 少 PoC",
        mid: "中（5-10 production）",
        high: "多（跨多 BU production）",
      },
      interview_question: "您 AI 應用上線幾個？跨幾個業務單位？",
    },
    {
      id: "governance_org",
      name: "AI 治理組織",
      values: {
        low: "無 / 散落 IT/Risk",
        mid: "有專責角色但無組織",
        high: "RAI office / 治理委員會在運作",
      },
      interview_question: "貴公司 AI 治理由哪個單位主責？有沒有專責角色？",
    },
    {
      id: "policy_state",
      name: "內規 / 政策狀態",
      values: {
        low: "沒 / ML 老政策硬套",
        mid: "patchy 寫不好 / 各 BU 各做各的",
        high: "完整 AI Playbook + SOP 在執行",
      },
      interview_question: "能不能分享您現有的 AI 政策 / SOP 文件？",
    },
    {
      id: "vocab",
      name: "客戶詞彙",
      values: {
        low: "「合規」「風險」「審計」",
        mid: "「治理」「PDCA」「Playbook」「藍圖」",
        high: "「frontier」「Agent」「Capability bet」「Ontology」",
      },
      interview_question: "訪談中觀察客戶用什麼詞？引用哪些 reference？",
    },
    {
      id: "buying_behavior",
      name: "採購行為",
      values: {
        low: "法規 RFP / 市場對標壓力",
        mid: "主動問治理 / RFP 列治理 requirement",
        high: "升級 / frontier 對齊",
      },
      interview_question: "RFP 列了什麼 requirement？客戶主動問什麼問題？",
    },
  ],

  signal_to_outcome: {
    rule_description: "5 個訊號中多數落哪欄就推那個套餐。",
    mappings: {
      low: "GV-C",
      mid: "GV-B",
      high: "GV-A",
    },
  },

  // ====== 抽絲剝繭問句（GV-D 警告） ======
  drill_down: {
    warning: "純工具買賣 IBM 顧問賺不到顧問費——是備案不是首選方案。客戶說「要工具」時應該主動追問，看是不是其實該升級到完整治理（GV-A/B/C）。",
    questions: [
      {
        question: "工具上線後誰負責讓它跑起來？",
        answerable: "有專責 / RAI office",
        unanswerable: "沒人 → 升級 GV-A/B/C",
      },
      {
        question: "您的內規 / SOP 寫了 AI 治理流程嗎？",
        answerable: "完整 SOP 在執行",
        unanswerable: "沒 SOP → 升級 GV-A/B/C",
      },
      {
        question: "AI 應用上線決策由誰拍板？",
        answerable: "有治理委員會",
        unanswerable: "沒人 → 升級 GV-A/B/C",
      },
      {
        question: "工具監控的指標誰看？看了會做什麼？",
        answerable: "明確的責任鏈",
        unanswerable: "沒人看 → 升級 GV-A/B/C",
      },
    ],
  },

  // ====== 客戶程度（包裝深淺） ======
  sophistication_levels: [
    {
      id: "high",
      label: "高（讀 frontier）",
      packaging: "直接 frontier shorthand、跳過教育",
      example: "我們和您共建 Operating Model + Ontology + Harness，跟 Anthropic 同思維",
      detection: "CEO/CDO 自己讀 Anthropic blog / X / 主動引用 frontier 詞彙",
    },
    {
      id: "mid",
      label: "中（需要橋接）",
      packaging: "用比喻 + 簡化術語",
      example: "治理是您 AI 工廠的鋼筋，3 年讓多個 BU 在同一張藍圖上跑",
      detection: "聽得懂 frontier 詞彙但不主動用",
    },
    {
      id: "low",
      label: "低（要 educate）",
      packaging: "從基礎觀念講起 + step-by-step + 案例",
      example: "您聽過 ChatGPT 嗎？AI 治理是讓您的 ChatGPT 不出錯的整套機制",
      detection: "完全沒聽過 frontier 詞彙 / 把 GenAI 等同 Chatbot",
    },
  ],
};

if (typeof module !== 'undefined') {
  module.exports = govConfig;
}
