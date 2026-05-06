// AI Governance 賣法 config - 改這裡的字串就能更新展示，不用動 index.html
// 來源：SALES_AI_GOVERNANCE.md v1.6

const govConfig = {
  meta: {
    title: "AI Governance 賣法",
    version: "v1.6",
    core_one_liner: "治理本身不直接賺錢——所以賣治理 = 找剛性需求附身。",
    summary: "7 條進案路徑 → Frame 與套餐獨立決定：客戶嘴上說的決定 Frame（怎麼包裝），治理成熟度決定套餐（實際範圍）。",
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
      scale: "50-150 人月 / 3-9 個月",
      anchors: [], // 待 Livia 補
    },
    {
      id: "GV-B",
      name: "內規重構 + 落地包",
      maturity: "mid",
      maturity_label: "中成熟",
      client_state: "零散內規寫不好",
      key_modules: "基於 M4 既有內規 + M1-M9",
      scale: "200-500 人月 / 9-18 個月",
      anchors: [],
    },
    {
      id: "GV-C",
      name: "全套新建 + 落地包",
      maturity: "low",
      maturity_label: "低成熟",
      client_state: "沒內規從零開始",
      key_modules: "M1-M9 全",
      scale: "300-800 人月 / 12-24 個月",
      anchors: [],
    },
    {
      id: "GV-D",
      name: "治理工具棧",
      maturity: "tool",
      maturity_label: "工具型",
      client_state: "真的真的只想買工具（罕見）",
      key_modules: "M5 為主",
      scale: "50-150 人月 / 3-6 個月",
      warning: "純工具對 IBM Consulting 沒大贏面——是 fallback 不是 default。客戶說「要工具」時應該抽絲剝繭主動往上推",
      anchors: [],
    },
    {
      id: "GV-E",
      name: "一次性技術檢測",
      maturity: "single",
      maturity_label: "單案型",
      client_state: "只想針對某專案表現驗證",
      key_modules: "M8-M9 技術控制項",
      scale: "30-80 人月 / 1-3 個月",
      warning: "若客戶內規不清 → 等同沒內規 → 回到 GV-B 或 GV-C",
      anchors: [],
    },
  ],

  // ====== 7 條進案路徑（A/B/C 三組） ======
  entry_paths: [
    {
      group_id: "A",
      group_name: "與 IBM 既有關係結合",
      group_desc: "IBM 主動帶。已有 default 套餐，5 訊號用來「判斷是否升級」。",
      paths: [
        {
          id: "A1",
          name: "IBM 內部 AI 工具品質保證",
          window: "CIO / IT 主管",
          frame_id: "tool_provider",
          default_outcome: "看 5 訊號",
          opening_hook: "IBM 顧問用 AI 工具效果未知，所以 IBM 內部都需要治理保證",
        },
        {
          id: "A2",
          name: "IBM AI 專案結合（要工具）",
          window: "CIO",
          frame_id: "tool_provider",
          default_outcome: "看 5 訊號",
          opening_hook: "您的 AI 案 / watsonx 順勢加治理",
        },
        {
          id: "A3",
          name: "IBM AI 專案結合（要藍圖）",
          window: "CDO / 董事會",
          frame_id: "operating_model",
          default_outcome: "看 5 訊號（偏中-低成熟）",
          opening_hook: "治理是規模化的前提，3 年走完才能跨場景 reuse",
        },
        {
          id: "A4",
          name: "三朵雲合作",
          window: "CIO + 雲商",
          frame_id: "tool_provider",
          default_outcome: "看 5 訊號",
          opening_hook: "補雲商不擅長的合規 mapping",
        },
      ],
    },
    {
      group_id: "B",
      group_name: "客戶端剛性需求",
      group_desc: "客戶情境驅動。從 0 用 5 訊號決策樹一跑套餐。",
      paths: [
        {
          id: "B1",
          name: "法規驅動",
          window: "CRO / 法遵長",
          frame_id: "compliance_partner",
          default_outcome: "看 5 訊號",
          opening_hook: "金管會 / EU AI Act / ISO 42001...",
        },
        {
          id: "B2",
          name: "危機事件後",
          window: "CEO 直線",
          frame_id: "compliance_partner",
          default_outcome: "補強升級 / 內規重構",
          opening_hook: "您看 X 公司上週 AI 出事...",
        },
        {
          id: "B3",
          name: "M&A 集團整合",
          window: "集團 CEO / CFO",
          frame_id: "group_integrator",
          default_outcome: "內規重構 / 全套新建",
          opening_hook: "併購後 12 個 BU 各做各的...",
        },
        {
          id: "B4",
          name: "認證取證",
          window: "CMO / CEO",
          frame_id: "compliance_partner",
          default_outcome: "內規重構 / 全套新建",
          opening_hook: "ISO 42001 是您出海前必拿的...",
        },
      ],
    },
    {
      group_id: "C",
      group_name: "技術前沿驅動",
      group_desc: "新技術出現觸發客戶來問怎麼治理。窗口通常是技術主管。",
      paths: [
        {
          id: "C1",
          name: "新技術觸發（multiagent / Claude Code 等）",
          window: "CTO / CDO / RAI",
          frame_id: "tool_provider", // 或 operating_model
          default_outcome: "補強升級 / 一次性檢測",
          opening_hook: "您要落地 X 新技術，治理還沒跟上...",
        },
      ],
    },
  ],

  // ====== Frame 鋪陳內涵 ======
  frames: [
    {
      id: "tool_provider",
      name: "工具供應商",
      core_story: "客戶腦袋簡化版：買工具 + IBM 教用 + 技術移轉 + 客戶的人會用了。**IBM 內部其實導入完整 operating model**——但不在客戶語言中說，客戶最終一樣得到完整治理",
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
      name: "法遵伴侶（常態 + 危機加速版）",
      core_story: "監理機關視角。法規 mapping → 落差 → 控制項 → 三道防線 → 取證 milestone。**速度可調**：常態走慢、危機走快。危機時加上「止血→根因→經驗轉化內規」",
      client_concern: "常態：我會被罰嗎？認證能拿到嗎？／ 危機：能多快止血？怎麼證明對外處理好了？",
      is_special: false,
    },
    {
      id: "group_integrator",
      name: "集團統合者",
      core_story: "集團一致性 + 風險集中 + 子公司散→拉齊。**講政治可行性 + 中立第三方**",
      client_concern: "子公司會配合嗎？怎麼讓他們不抵抗？",
      is_special: false,
    },
    {
      id: "ai_lab_partner",
      name: "AI Lab Partner",
      core_story: "Frontier-aligned。跟 Anthropic / Palantir 對標。Capability bet。Agent / Ontology / Harness / Evals。研發共創",
      client_concern: "我們是不是站在 frontier？跟同業比領先嗎？",
      is_special: true,
      special_note: "99% 案不適用。只在 tier 1 客戶（CTBC / 玉山 / Wistron 等）主動提出新治理觀念時才走",
    },
  ],

  // ====== 5 訊號（決策樹一） ======
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

  // ====== 訊號 → 套餐映射規則 ======
  signal_to_outcome: {
    rule_description: "5 個訊號中多數落哪欄就推那個套餐。打平時按 mid 偏低處理。",
    mappings: {
      low: "GV-C", // 全套新建
      mid: "GV-B", // 內規重構
      high: "GV-A", // 補強升級
    },
    quick_branches: [
      {
        condition: "客戶嘴上說「我要工具」+ 抽絲剝繭都答得出來",
        outcome: "GV-D",
        note: "罕見，等於 GV-A 退化版",
      },
      {
        condition: "客戶嘴上說「單案驗證」+ 內規清楚",
        outcome: "GV-E",
        note: "若內規不清 → 回 5 訊號決策",
      },
    ],
  },

  // ====== 抽絲剝繭問句 ======
  drill_down_questions: [
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
      label: "中(需要橋接)",
      packaging: "用比喻 + 簡化術語",
      example: "治理是您 AI 工廠的鋼筋，3 年讓多個 BU 在同一張藍圖上跑",
      detection: "聽得懂 frontier 詞彙但不主動用",
    },
    {
      id: "low",
      label: "低(要 educate)",
      packaging: "從基礎觀念講起 + step-by-step + 案例",
      example: "您聽過 ChatGPT 嗎？AI 治理是讓您的 ChatGPT 不出錯的整套機制",
      detection: "完全沒聽過 frontier 詞彙 / 把 GenAI 等同 Chatbot",
    },
  ],

  // ====== 同套餐對不同客戶範例 ======
  outcome_examples: [
    {
      outcome_id: "GV-C",
      examples: [
        {
          client: "玉山",
          client_says: "金管會檢查",
          frame_id: "compliance_partner",
          sophistication: "mid",
          opening_storyline: "「金管會 AI 治理檢查週期...」+ 法規 mapping → 三道防線 → 取證 milestone",
        },
        {
          client: "YAGEO",
          client_says: "集團要統一",
          frame_id: "group_integrator",
          sophistication: "mid",
          opening_storyline: "「併購後 12 個 BU 各做各的...」+ 集團一致性 → 子公司拉齊",
        },
        {
          client: "大型製造業",
          client_says: "我要藍圖",
          frame_id: "operating_model",
          sophistication: "mid_high",
          opening_storyline: "「3 年讓您的 AI 工廠跑起來」+ Operating Model 全景 + roadmap",
        },
        {
          client: "中型銀行",
          client_says: "我要工具",
          frame_id: "tool_provider",
          sophistication: "low",
          opening_storyline: "「您的 watsonx 順勢加治理」+ 買工具 + IBM 教用 + 技術移轉（用比喻）。IBM 內部仍跑完整 M1-M9",
        },
      ],
    },
  ],
};

if (typeof module !== 'undefined') {
  module.exports = govConfig;
}
