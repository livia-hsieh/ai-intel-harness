# 賣法 Playbook 互動式 View

對人類友善 + 互動 + 配置與展示分離的呈現層。

---

## 怎麼用

1. **開啟頁面**：雙擊 `index.html`，或在 Finder 點 [open](computer:///Users/liviahsieh/Documents/Claude/Projects/推廣 AI at Scale Solution/view/index.html) 在瀏覽器打開
2. **切 tab**：上方 nav 切「AI Governance」/「AI at Scale」
3. **互動**：「決策樹一」section 點 5 訊號的「低 / 中 / 高」按鈕，下方推薦套餐會即時更新 + 上方對應卡片高亮
4. **看範例**：「同套餐對不同客戶」section 用 dropdown 切套餐看不同客戶範例

---

## 怎麼改內容（不用動 HTML）

所有內容在兩個 config 檔：

- `config_governance.js`（AI Governance）
- `config_at_scale.js`（AI at Scale）

打開檔案，直接改 string 內容、加減 row、改 metadata。儲存後重新整理 browser 就更新。

### 結構速查

| 資料區塊 | config 欄位 | 改什麼 |
|---|---|---|
| 核心一句話 | `meta.core_one_liner` | 標題下方 hero 文字 |
| 5 套餐卡片 | `outcomes[]` | 套餐名、客戶現況、模組、規模 |
| 進案路徑 | `entry_paths[]` | 觸發點、窗口、Frame、開場 hook |
| Frame 鋪陳 | `frames[]` | Frame 名、core_story、客戶關切 |
| 決策樹訊號 | `decision_signals[]` | 5 訊號名、low/mid/high 標籤、訪談問句 |
| 客戶程度 | `sophistication_levels[]` | 高 / 中 / 低 包裝方式 |
| 範例對照 | `outcome_examples[]` | 同套餐對不同客戶範例 |
| 抽絲剝繭問句 | `drill_down_questions[]` | GV-D 警告問句 |

### 加新套餐

在 `outcomes[]` 加新 object，譬如：

```javascript
{
  id: "GV-F",
  name: "新套餐",
  maturity: "tool",            // 對應 signal_to_outcome.mappings 的 key
  maturity_label: "新型",
  client_state: "客戶現況描述",
  key_modules: "M1+M2",
  scale: "100 人月",
  warning: "可選的警告文字",    // 紅色 callout
  anchors: [],
}
```

### 加新進案路徑

在 `entry_paths[]` 找對應 group，在 `paths[]` 加：

```javascript
{
  id: "B5",
  name: "新進案路徑",
  window: "CEO",
  frame_id: "compliance_partner",  // 必須對應 frames[] 中的 id
  default_outcome: "看 5 訊號",
  opening_hook: "您看 X 公司...",
}
```

### 加客戶 anchor

每個套餐的 `anchors` 目前是空 array `[]`。改成：

```javascript
anchors: [
  { client: "玉山", year: "2025", note: "已交付" },
  { client: "中信", year: "2026", note: "進行中" },
]
```

（注意：HTML 目前沒 render anchors，要加 render 邏輯需改 `index.html` 的 `renderOutcomes`）

---

## 設計理念

**底層 raw data ≠ 展示層**。

- `config_*.js` = 純資料（改字串就更新）
- `index.html` = template + 互動 JS（一次寫好幾乎不動）

→ 修改內容不燒 token 改 HTML，只改 config 的 string

---

## 已知限制

- HTML 目前不 render `anchors` 欄位（要加需改 template）
- 決策樹一只看 5 訊號的眾數推套餐——快速分支（GV-D / GV-E）目前是文字顯示，沒做互動分支
- 包裝建議（Frame × 套餐 × 程度 → 完整推薦）目前只有「範例對照」section，沒做完整互動推薦工具
- AI at Scale config 還沒到 governance v1.6 的精修程度

未來如要強化互動（譬如完整推薦工具），改 `index.html` 加 render function。
