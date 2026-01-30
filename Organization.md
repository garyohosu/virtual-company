# Organization.md - スケールフリー・ネットワーク構造

## 🏛️ 会社の組織図（相似構造）

```
┌────────────────────────────────────────────────────┐
│              CEO（社長）                            │
│   CEO-Skills.md  CEO-Memory.md  CEO-Reports/     │
└──────────────────┬─────────────────────────────────┘
                   │
         ┌─────────┴─────────┐
         ↓                   ↓
    ┌─────────┐          ┌─────────┐
    │ 部長A   │          │ 部長B   │
    │ Dir-    │          │ Dir-    │
    │ Skills  │          │ Skills  │
    │ Dir-    │          │ Dir-    │
    │ Memory  │          │ Memory  │
    └────┬────┘          └────┬────┘
         │                    │
      ┌──┴──┐             ┌──┴──┐
      ↓     ↓             ↓     ↓
    課長  課長          課長  課長
    A1    A2           B1    B2
    │     │            │     │
  係係  係係          係係  係係
  1 2  3 4          5 6  7 8
```

---

## 📊 各層の役割とメモリ管理

### 層と責任

| 層 | 役割 | メモリ範囲 | 親への報告 |
|-----|------|----------|----------|
| **CEO** | 全体統括 | 部長からの報告のみ | なし |
| **部長** | 複数部門管理 | 課長からの報告のみ | 月次レポート |
| **課長** | 複数チーム管理 | 係からの報告のみ | 週次レポート |
| **係** | 実務実行 | 自分の仕事のみ | 日次レポート |

### 相似性（スケールフリー）

各層は **全く同じアーキテクチャ** を持つ：

```
CEO層:
├─ CEO-Skills.md
│  └─ Error Pattern: CEO がしてはいけない判断ミス
├─ CEO-Memory.md
│  └─ 月度: 部長からの報告内容、判断
└─ CEO-Reports/
   └─ director_A_report.md
   └─ director_B_report.md

部長層:
├─ Director-Skills.md
│  └─ Error Pattern: 部長がしてはいけない判断ミス
├─ Director-Memory.md
│  └─ 週度: 課長からの報告内容、判断
└─ Director-Reports/
   └─ manager_A1_report.md
   └─ manager_A2_report.md

課長層（相似）:
├─ Manager-Skills.md
├─ Manager-Memory.md
└─ Manager-Reports/

係層（相似）:
├─ Employee-Skills.md
├─ Employee-Memory.md
└─ Employee-Reports/
```

---

## 🧠 メモリとスキルの流れ

### 係が失敗 → スキルが生まれる

```
係が「このエラー見たことある」
  ↓
係-Skills.md で解決方法を見つける
  ↓
解決して報告
  ↓
課長に報告書で知らせる

課長は係の詳細は知らない。
課長は「係が報告書を提出した」ことだけ知る。
```

### 課長が判断ミス → その層のスキルになる

```
課長が判断ミスをした
  ↓
Manager-Skills.md に「課長が陥りやすいパターン」を記録
  ↓
部長に「判断ミスがありました」と報告
  ↓
部長は詳細は知らない。
部長は「課長が報告書を修正提出した」ことだけ知る。
```

### CEO は何も覚えていない

```
CEO-Memory.md には：
- 部長Aが好調
- 部長Bが要監視
- 月度目標達成状況

CEO は係のことは知らない。
部長が報告書だけを持ってくる。
```

---

## 📂 ファイル構造

```
virtual-company/
├── Organization.md             ← この構造図
├── README.md
│
├── Organization/
│   │
│   ├── ceo/
│   │   ├── Skills.md           # CEO-level failures
│   │   ├── Memory.md           # CEO 進捗記録
│   │   ├── Reports/
│   │   │   ├── director_a_report.md
│   │   │   └── director_b_report.md
│   │   └── order_ceo_yoro.md   # CEO への指示
│   │
│   ├── director_a/
│   │   ├── Skills.md           # 部長A-level failures
│   │   ├── Memory.md           # 部長A 進捗記録
│   │   ├── Reports/
│   │   │   ├── manager_a1_report.md
│   │   │   └── manager_a2_report.md
│   │   └── order_director_yoro.md
│   │
│   ├── manager_a1/
│   │   ├── Skills.md           # 課長A1-level failures
│   │   ├── Memory.md           # 課長A1 進捗記録
│   │   ├── Reports/
│   │   │   ├── employee_1_report.md
│   │   │   └── employee_2_report.md
│   │   └── order_manager_yoro.md
│   │
│   └── employee_1/
│       ├── Skills.md           # 係-level failures
│       ├── Memory.md           # 係 進捗記録
│       └── order_employee_yoro.md
```

---

## 🎯 スケールフリー・ネットワークの特性

### 1. 相似性（Self-similarity）

```
CEO の order_ceo_yoro.md:
「部長から報告を受け取れ。判断を下せ。」

部長 の order_director_yoro.md:
「課長から報告を受け取れ。判断を下せ。」

課長 の order_manager_yoro.md:
「係から報告を受け取れ。判断を下せ。」

係 の order_employee_yoro.md:
「タスクを実行せよ。完了を報告せよ。」
```

### 2. ハブ構造（Hub-based）

```
CEO（強いハブ）
  └─ 部長（中程度のハブ）
      └─ 課長（弱いハブ）
          └─ 係（末端ノード）

CEO は 2 つの部長にしか接続しない
部長は 2 つの課長にしか接続しない
課長は複数の係に接続

ネットワークが爆発的に成長しない ✅
```

### 3. 距離（Distance）

```
CEO-報告書 の距離: 1層上（部長経由）
CEO-課長 の距離: 2層上（部長経由）
CEO-係 の距離: 3層上（部長→課長経由）

CEO は係の詳細を見ない。
見るのは「月度報告」だけ。
```

---

## 📝 各層のメモリ形式

### CEO-Memory.md

```markdown
## 月度進捗

**2025年1月**

### 部長A の報告
- 課題: 課長A1が判断ミス
- 対応: 課長A1が修正提出（Skills に記録済み）
- 評価: 対応良好

### 部長B の報告
- 課題: 特になし
- 評価: 順調

### CEO が覚えていること
- 部長A は対応力がある
- 部長B は安定している
- 来月は部長A に追加予算配分
```

CEO は係の失敗を知らない。部長経由で「対応済み」として報告されるだけ。

### 部長-Memory.md

```markdown
## 週度進捗

**2025年1月 Week1**

### 課長A1 の報告
- 係1: GitHubエラーで詰まった（Skills で解決）
- 係2: 正常実行
- 評価: 対応良好

### 課長A2 の報告
- 係3,4: 正常実行
- 評価: 順調

### 部長が覚えていること
- 課長A1 の係1 が成長している
- 課長A2 は安定している
- CEO には「課長A1 が判断ミスをしたが自己修正」と報告
```

部長は係の個別タスクを知らない。課長経由で「対応済み」として報告されるだけ。

---

## 🔄 情報フロー

### ボトムアップ（報告）

```
係がタスク完了
  ↓
係-Memory.md に記録
  ↓
Employee-Report.md を課長に提出
  ↓
課長が確認・判断
  ↓
課長-Memory.md に記録
  ↓
Manager-Report.md を部長に提出
  ↓
部長が確認・判断
  ↓
部長-Memory.md に記録
  ↓
Director-Report.md を CEO に提出
```

### トップダウン（指示）

```
CEO が「重要度UP」と決定
  ↓
CEO-order.md を更新
  ↓
部長が read → order_director.md を更新
  ↓
課長が read → order_manager.md を更新
  ↓
係が read → order_employee.md を更新
  ↓
係が実行
```

---

## 💾 スケーラビリティの計算

### 従来型（全員が全員を覚える）

```
10人で 100 の作業
全員が全員を覚える
= 各エージェント 900 の記憶量
= 合計 9000 の記憶消費

破綻 ❌
```

### スケールフリー型（相似構造）

```
CEO（部長2人の報告のみ）: 2 の記憶
部長A（課長2人の報告のみ）: 2 の記憶
部長B（課長2人の報告のみ）: 2 の記憶
課長A1（係2人の報告のみ）: 2 の記憶
...
係（自分の作業のみ）: 10 の記憶

各層: ~2 の記憶
合計: ~2 × 5層 × 2 × 2 × ... = O(log n)

スケール ✅
```

---

## 🎯 失敗学習の循環

### 係が失敗

```
係が「このエラー見たことある」
  ↓
係-Skills.md で解決
  ↓
解決内容を Employee-Report.md に書く
  ↓
課長が確認 → 「係が成長した」と記録
  ↓
課長-Memory.md に「係1 は成長している」と記録
  ↓
次の課長判断に活かされる
```

### 課長が判断ミス

```
課長が判断ミスをした
  ↓
Manager-Skills.md に「課長が避けるべき判断パターン」を記録
  ↓
Manager-Report.md に「判断ミスがありました」と書く
  ↓
部長が確認 → 「課長は修正できる」と評価
  ↓
部長-Memory.md に「課長は判断ミスから学んでいる」と記録
  ↓
CEO には「対応済み」として報告
```

**CEO は失敗の詳細を知らない。** でも、全体の信頼度は上がる。

---

## 🚀 実装ロードマップ

### Phase 1: CEO 層実装
- [ ] Organization/ceo/ ディレクトリ作成
- [ ] CEO-Skills.md, CEO-Memory.md, order_ceo_yoro.md
- [ ] 部長への指示書フォーマット作成

### Phase 2: 部長層実装
- [ ] Organization/director_a/, director_b/ ディレクトリ
- [ ] 各層で相似的な構造を実装

### Phase 3: 課長層実装
- [ ] Organization/manager_a1/, manager_a2/ ディレクトリ

### Phase 4: 係層実装
- [ ] Organization/employee_1/, employee_2/ ディレクトリ

### Phase 5: 統合テスト
- [ ] CEO が指示 → 係が実行 の全フロー
- [ ] 報告書が正しく上がってくるか確認
- [ ] メモリ消費量が O(log n) か検証

---

## 💡 神回：CEO が何も知らない事件

```
CEO: 「月度報告をくれ」

部長A: 「係1がGitHubエラーで詰まりましたが、
        課長A1が修正対応させました。
        係は成長しています。」

CEO: 「ほーん。対応できてるんだな。」

CEO は係の存在を知らない。
部長と課長からの報告だけで判断している。

CEO-Memory.md には：
「部長A の係配下が成長している」

だけ。

これが スケールフリー・ネットワーク の本質。
```

---

## 📊 スケール検証

| 人数 | 従来型メモリ | スケールフリー型 | 削減率 |
|-----|-----------|--------------|-------|
| 10 | 900 | 20 | 97.8% ↓ |
| 100 | 99,000 | 60 | 99.9% ↓ |
| 1,000 | 9,990,000 | 100 | 99.99% ↓ |

---

**Status**: Ready to implement  
**Version**: 1.0  
**Pattern**: Scale-free Network with Self-similarity
