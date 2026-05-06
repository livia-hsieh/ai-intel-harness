// AI at Scale 賣法 config - 改這裡的字串就能更新展示
// 來源：SALES_AI_AT_SCALE.md v1.0（注意：這份還未經 governance 等級的多次迭代精修）

const scaleConfig = {
  meta: {
    title: "AI at Scale 賣法",
    version: "v1.0",
    core_one_liner: "成熟度低的客戶聽不下完整藍圖，成熟度高的客戶要 frontier 對齊全景。所以同一套 7 元件 solution 要切成 4 種「可賣結果」，光譜兩端配不同包裝。",
    summary: "4 種可賣結果 + 進案路徑 + 決策樹 + 包裝三件事",
    note: "本份文件還未對齊 governance 那份的精修程度（決策樹反向設計、Frame 內涵化、客戶程度維度、Frame vs 套餐分開等）。",
  },

  // ====== 4 種可賣結果 ======
  outcomes: [
    {
      id: "AS-1",
      name: "先場景後診斷",
      sub_label: "今年場景 + 明年顧問藍圖",
      key_modules: "#6 ×1-2 + #3 D2 minimal + 後續 #1 hooks",
      scale: "今年 50-150 人月 / 6-12 個月",
      sales_motion: "兩段 play（小 → 擴大）",
      anchors: [],
    },
    {
      id: "AS-2",
      name: "純顧問藍圖",
      sub_label: "完整顧問，不直接落地",
      key_modules: "#1 B1-B5 完整 + 部分 #2 + #5 M1 + #4 T1-T2",
      scale: "100-400 人月 / 6-12 個月",
      sales_motion: "純顧問交付",
      anchors: [],
    },
    {
      id: "AS-3",
      name: "顧問 + 場景 + 落地一案到底",
      sub_label: "完整顧問 + 同案內挑場景 + 落地",
      key_modules: "#1 + #6 ×N + #3 + 部分 #4 + 部分 #5 + 部分 #2 + 部分 #7",
      scale: "500-1500 人月 / 12-24 個月",
      sales_motion: "旗艦級",
      anchors: [],
    },
    {
      id: "AS-4",
      name: "純場景",
      sub_label: "1-N 個場景，無顧問",
      key_modules: "#6 ×1-3 + #3 D2 minimal + #4 T1 minimal",
      scale: "30-200 人月 / 3-12 個月",
      sales_motion: "直接進場景案",
      anchors: [],
    },
  ],

  // ====== 進案路徑（從 Livia 訪談中抓到的觸發點） ======
  entry_paths: [
    {
      group_id: "main",
      group_name: "常見進案觸發點",
      group_desc: "AI at Scale 還沒對齊 governance 的精細路徑分組——這層待重構",
      paths: [
        {
          id: "M1",
          name: "高層自發轉型",
          window: "CEO / CDO / 董事會",
          opening_hook: "3 年後您想跟 frontier 對齊嗎？",
        },
        {
          id: "M2",
          name: "競爭驅動",
          window: "CEO / CDO",
          opening_hook: "您的競爭對手 X 已經做了 Y...",
        },
        {
          id: "M3",
          name: "IBM 既有大案延伸",
          window: "CDO / CIO",
          opening_hook: "您現在的 IBM 案能延伸到 ...",
        },
        {
          id: "M4",
          name: "集團 / M&A 重整",
          window: "集團 CEO / CFO",
          opening_hook: "集團併購後要統一...",
        },
        {
          id: "M5",
          name: "業務 BU 痛點",
          window: "業務 BU 主管",
          opening_hook: "您客服 AI 命中率還停在 40% 嗎？",
        },
        {
          id: "M6",
          name: "IT 預算主動立案",
          window: "CIO",
          opening_hook: "您 IT 預算 30% 花在重複資料整備嗎？",
        },
      ],
    },
  ],

  // ====== Frame ======
  frames: [
    {
      id: "consultant_blueprint",
      name: "顧問藍圖",
      core_story: "戰略清晰 + 第三方 validate",
      client_concern: "3 年後我長什麼樣？這個 roadmap 對嗎？",
      is_special: false,
    },
    {
      id: "transformation_partner",
      name: "轉型陪跑夥伴",
      core_story: "長期 partner + 知識轉移 + 共同成長",
      client_concern: "我能不能跟得上？",
      is_special: false,
    },
    {
      id: "ai_lab_partner",
      name: "AI Lab Partner",
      core_story: "frontier 認知 + 研發共創",
      client_concern: "我們是不是站在 frontier？",
      is_special: true,
      special_note: "tier 1 客戶 + 主動提新觀念才適用",
    },
    {
      id: "group_integrator",
      name: "集團統合者",
      core_story: "集團一致性 + 政治可行性",
      client_concern: "子公司會配合嗎？",
      is_special: false,
    },
    {
      id: "platform_advisor",
      name: "平台選型專家",
      core_story: "中立選型 + 整合能力",
      client_concern: "我會不會被 vendor lock？",
      is_special: false,
    },
  ],

  // ====== 決策訊號（簡化版） ======
  decision_signals: [
    {
      id: "want_blueprint",
      name: "藍圖意願",
      values: {
        low: "不要藍圖",
        mid: "要藍圖但不落地",
        high: "要藍圖+要落地",
      },
      interview_question: "您要 3 年規劃還是只要解決眼前問題？",
    },
    {
      id: "want_expansion",
      name: "後續擴大意願",
      values: {
        low: "純就要場景",
        mid: "可能會擴大",
        high: "明年明確要做藍圖",
      },
      interview_question: "做完這個之後您想往哪走？",
    },
  ],

  // ====== 同 outcome 對不同客戶範例 ======
  outcome_examples: [
    {
      outcome_id: "AS-3",
      examples: [
        {
          client: "CTBC",
          client_says: "AI-native bank",
          frame_id: "ai_lab_partner",
          sophistication: "high",
          opening_storyline: "我們和您共建 AI-native 銀行，Agent + Ontology + Harness 三原子",
        },
        {
          client: "NSL（保守大型）",
          client_says: "我要 3 年規劃",
          frame_id: "transformation_partner",
          sophistication: "low",
          opening_storyline: "我們陪您 3 年做完整轉型",
        },
        {
          client: "YAGEO",
          client_says: "集團要統一",
          frame_id: "group_integrator",
          sophistication: "mid",
          opening_storyline: "我們幫您拉齊 12 個 BU",
        },
        {
          client: "中型客戶",
          client_says: "要顧問",
          frame_id: "consultant_blueprint",
          sophistication: "low",
          opening_storyline: "IBM 顧問幫您想清楚 3 年怎麼做",
        },
      ],
    },
  ],
};

if (typeof module !== 'undefined') {
  module.exports = scaleConfig;
}
