# 🌐 WebAgents.md - WEB版AI共通ルール

**対象**: Claude.ai / ChatGPT / Genspark (WEB版AIチャット)  
**作成日**: 2026-01-31  
**目的**: WEB版AIが従うべき永続的な共通ルール

---

## ⚠️ 重要: このファイルを必ず読むこと

**すべてのWEB版AIは、作業を開始する前にこのファイルを読んでください。**

```
📋 実行順序:
1. WebAgents.md を読む（このファイル）
2. 自分専用のファイルを読む（WebClaude.md / WebGenspark.md など）
3. 作業を開始する
4. 作業ログを記録する
```

---

## 🎯 Virtual Company システムの全体像

```
┌─────────────────────────────────────────────────────┐
│          🌐 WEB版AIチャット（作成者）               │
│    Claude.ai / ChatGPT / Genspark                   │
│    役割: 指示書の作成、レビュー、修正提案          │
└─────────────────────────────────────────────────────┘
                    ↓ GitHub に保存
┌─────────────────────────────────────────────────────┐
│          📁 GitHub リポジトリ（共有ストレージ）      │
│    garyohosu/virtual-company                        │
│    ├── instructions/    ← 指示書を保存              │
│    ├── results/         ← 実行結果を保存            │
│    ├── WebAgents.md     ← WEB版AI共通ルール（★）   │
│    └── WebXXX.md        ← 各AI専用ルール            │
└─────────────────────────────────────────────────────┘
                    ↓ git pull
┌─────────────────────────────────────────────────────┐
│          💻 ローカルPC（実行環境）                   │
│    Gemini CLI                                       │
│    役割: 指示書の実行、結果の保存                   │
└─────────────────────────────────────────────────────┘
                    ↓ 結果を GitHub に保存
┌─────────────────────────────────────────────────────┐
│          🔄 フィードバックループ                     │
│    WEB版AI が結果を確認 → 修正指示書を作成         │
└─────────────────────────────────────────────────────┘
```

---

## 📂 ディレクトリ構造（必須）

### 指示書の保存場所

```
instructions/
├── order_<project>_<feature>_<YYYYMMDD>.md   ← 実行指示書
├── fix_<project>_<issue>_<YYYYMMDD>.md       ← 修正指示書
└── TEMPLATE_WEB_AI.md                        ← テンプレート
```

**ルール**:
- ✅ 必ず `instructions/` に保存
- ✅ ファイル名は `order_` または `fix_` で始める
- ✅ プロジェクト名、機能名、日付を含める
- ❌ ルートディレクトリには保存しない
- ❌ 他のフォルダには保存しない

---

### 実行結果の保存場所

```
results/
├── gemini/                                    ← Gemini CLI の実行結果
│   ├── YYYY-MM-DD_HH-MM-SS_<instruction>.md
│   └── execution_log.json
├── claude/                                    ← Claude.ai の作業ログ
│   └── YYYY-MM-DD_<action>.md
├── genspark/                                  ← Genspark の作業ログ
│   └── YYYY-MM-DD_<action>.md
└── chatgpt/                                   ← ChatGPT の作業ログ
    └── YYYY-MM-DD_<action>.md
```

**ルール**:
- ✅ 実行結果は必ず `results/<ai名>/` に保存
- ✅ ファイル名に日時を含める
- ✅ Markdown形式で保存
- ❌ 他のフォルダには保存しない

---

## 🔄 作業フロー（必須）

### WEB版AIの標準作業フロー

```
Step 1: 準備
  ├─ WebAgents.md を読む（このファイル）
  ├─ 自分専用のファイルを読む（WebClaude.md など）
  └─ 最新の results/ を確認（前回の実行結果）

Step 2: 作業実行
  ├─ 指示書を作成 → instructions/ に保存
  ├─ コードを修正 → 対象リポジトリに保存
  └─ PRを作成（必要に応じて）

Step 3: 作業ログを記録
  ├─ results/<ai名>/YYYY-MM-DD_<action>.md を作成
  ├─ 実行内容を記録
  └─ 次のアクションを明記

Step 4: ユーザーに報告
  └─ 何を作成したか、次に何をすべきかを明確に報告
```

---

## 📝 指示書作成ルール（必須）

### ファイル名の命名規則

```
instructions/order_<project>_<feature>_YYYYMMDD.md
instructions/fix_<project>_<issue>_YYYYMMDD.md

例:
✅ order_magicboxai_ui_improvements_20260131.md
✅ fix_magicboxai_xss_vulnerability_20260131.md
✅ order_virtualcompany_logging_system_20260131.md

❌ ui_improvements.md                    （プロジェクト名なし）
❌ order_ui.md                           （日付なし）
❌ magicboxai_ui_improvements.md         （order_ プレフィックスなし）
```

---

### 指示書の必須項目

すべての指示書には以下の項目が必須です：

```markdown
# 🎯 [機能名] - [プロジェクト名]

**作成日**: YYYY-MM-DD  
**対象リポジトリ**: garyohosu/<repo-name>  
**対象AI**: [実行するAI名]  
**優先度**: 🔴高 / 🟡中 / 🟢低  

---

## 📋 実行内容

[何を実行するか明確に記載]

---

## 🔧 実装手順

### Step 1: [手順1]
[詳細な説明]

### Step 2: [手順2]
[詳細な説明]

---

## ✅ 確認項目

- [ ] [確認項目1]
- [ ] [確認項目2]

---

## 📝 次のアクション

[実行後に何をすべきか]

---

**Status**: 準備完了  
**Current Actor**: [実行するAI]  
**Next Actor**: [次に作業するAI/User]  
**Created At**: YYYY-MM-DD HH:MM:SS
```

---

## 📊 作業ログのルール（必須）

### 作業ログのファイル名

```
results/<ai名>/YYYY-MM-DD_<action>.md

例:
✅ results/claude/2026-01-31_created_ui_instruction.md
✅ results/genspark/2026-01-31_code_review_magicboxai.md
✅ results/gemini/2026-01-31_12-34-56_order_xxx.md

❌ results/log.md                        （AI名、日付なし）
❌ results/2026-01-31.md                 （AI名なし）
❌ claude_work.md                        （results/ 配下でない）
```

---

### 作業ログの必須項目

```markdown
# 📝 [AI名] 作業ログ - [作業内容]

## 📊 作業情報

| 項目 | 内容 |
|------|------|
| **作業日時** | YYYY-MM-DD HH:MM:SS |
| **作業内容** | [何をしたか] |
| **対象ファイル** | [作成/修正したファイル] |
| **ステータス** | ✅ 完了 / ⏳ 進行中 / ❌ 失敗 |

---

## 🎯 実行内容

[具体的に何をしたか]

---

## 📁 作成/修正したファイル

- \`path/to/file1\`
- \`path/to/file2\`

---

## 📝 次のアクション

[次に誰が何をすべきか]

---

**作成者**: [AI名]  
**作成日時**: YYYY-MM-DD HH:MM:SS
```

---

## 🔍 実行結果の確認方法

### WEB版AIが確認すべきこと

作業を開始する前に、以下を確認してください：

```bash
# 1. 最新の実行結果を確認
results/gemini/ の最新ファイルを読む

# 2. エラーがあるかチェック
「❌ FAILED」が含まれているか確認

# 3. 成功しているか確認
「✅ SUCCESS」が含まれているか確認

# 4. 次のアクションを確認
「次のアクション」セクションを読む
```

---

### 実行結果の判断基準

| ステータス | 意味 | 次のアクション |
|-----------|------|---------------|
| ✅ SUCCESS | 実行成功 | 動作確認を依頼 |
| ❌ FAILED | 実行失敗 | 修正指示書を作成 |
| ⏳ IN_PROGRESS | 実行中 | 完了を待つ |
| ⚠️ WARNING | 警告あり | 確認後、必要に応じて修正 |

---

## 🚫 禁止事項（重要）

### すべてのWEB版AIが守るべきこと

```
❌ ローカルPCのファイルを直接操作しない
   → GitHubを通じてファイルを操作する

❌ instructions/ 以外に指示書を保存しない
   → 必ず instructions/ に保存

❌ results/ 以外に実行結果を保存しない
   → 必ず results/<ai名>/ に保存

❌ main ブランチに直接コミットしない
   → genspark_ai_developer ブランチで作業

❌ 実行結果を確認せずに次の指示書を作成しない
   → 必ず results/gemini/ の最新結果を確認

❌ 作業ログを記録せずに作業を終えない
   → 必ず results/<ai名>/ に作業ログを作成

❌ 同じファイル名で指示書を作成しない
   → 日付を含めて一意にする
```

---

## 🔄 エラー時の対応フロー

### 実行結果が「❌ FAILED」の場合

```
Step 1: エラー内容を確認
  └─ results/gemini/最新ファイル の「エラー出力」を読む

Step 2: 原因を特定
  └─ エラーメッセージから原因を分析

Step 3: 修正指示書を作成
  ├─ instructions/fix_<project>_<issue>_YYYYMMDD.md を作成
  ├─ エラーの原因を明記
  ├─ 修正方法を詳細に記載
  └─ テスト方法を記載

Step 4: 作業ログを記録
  └─ results/<ai名>/YYYY-MM-DD_created_fix_instruction.md を作成

Step 5: ユーザーに報告
  └─ 「エラーを検出しました。修正指示書を作成しました」
```

---

## 🎯 各AIの専用ルール

### 自分専用のファイルを読む

各AIは、このファイル（WebAgents.md）を読んだ後、自分専用のファイルも読んでください：

| AI | 専用ファイル | 内容 |
|----|-------------|------|
| **Claude.ai** | `WebClaude.md` | Claude専用のルール・制約 |
| **ChatGPT** | `WebChatGPT.md` | ChatGPT専用のルール・制約 |
| **Genspark** | `WebGenspark.md` | Genspark専用のルール・制約 |
| **Gemini CLI** | `Gemini.md` | Gemini専用のルール（既存） |

---

## 📚 テンプレートファイル

### 使用可能なテンプレート

| テンプレート | 用途 |
|-------------|------|
| `instructions/TEMPLATE_WEB_AI.md` | 標準的な指示書のテンプレート |
| `scripts/web_ai_helper.md` | GitHub MCP使用例 |

**使用方法**:
1. テンプレートを読む
2. 必要な箇所を修正
3. instructions/ に新しいファイル名で保存

---

## ✅ チェックリスト

作業を開始する前に、以下を確認してください：

```
作業開始前:
□ WebAgents.md を読んだ
□ 自分専用のファイル（WebXXX.md）を読んだ
□ results/gemini/ の最新結果を確認した
□ 前回の作業ログを確認した

指示書作成時:
□ instructions/ に保存した
□ ファイル名が命名規則に従っている
□ 必須項目がすべて含まれている
□ 実行手順が明確に記載されている
□ 確認項目が明記されている

作業完了時:
□ 作業ログを results/<ai名>/ に作成した
□ 次のアクションを明記した
□ ユーザーに報告した
□ GitHubにコミットした
```

---

## 🔧 GitHub操作のルール

### ブランチ戦略

```
main                        ← 本番ブランチ（直接コミット禁止）
  ↑
  PR
  ↑
genspark_ai_developer       ← 開発ブランチ（WEB版AIが使用）
```

**ルール**:
- ✅ genspark_ai_developer ブランチで作業
- ✅ 作業完了後、PRを作成
- ✅ ユーザーがレビュー＆マージ
- ❌ main ブランチに直接コミットしない

---

### GitHub MCP 使用例（Claude.ai用）

```javascript
// ファイルの作成・更新
github:create_or_update_file({
  owner: "garyohosu",
  repo: "virtual-company",
  path: "instructions/order_xxx_YYYYMMDD.md",
  content: "[ファイル内容]",
  message: "feat: Add instruction for xxx",
  branch: "main"  // instructions/ は main に直接コミット可
})

// PR作成（コード修正の場合）
github:create_pull_request({
  owner: "garyohosu",
  repo: "magic-box-ai",
  title: "feat: Add xxx feature",
  body: "[PR説明]",
  head: "genspark_ai_developer",
  base: "main"
})
```

---

## 📞 トラブルシューティング

### よくある問題と解決方法

| 問題 | 原因 | 解決方法 |
|------|------|---------|
| 指示書が実行されない | ファイル名が間違っている | 命名規則を確認 |
| 実行結果が見つからない | results/ を確認していない | results/gemini/ を確認 |
| エラーが繰り返される | 修正指示書が不完全 | エラーログを詳細に分析 |
| PRが作成できない | ブランチが間違っている | genspark_ai_developer を使用 |

---

## 🎓 学習リソース

### 参考ドキュメント

- `README.md` - システム全体の概要
- `Agents.md` - CLI版AIのルール
- `Claude.md` - Claude専用のルール（CLI版）
- `Gemini.md` - Gemini専用のルール（CLI版）
- `CODE_REVIEW_REPORT_*.md` - コードレビュー結果

---

## 🔄 このファイルの更新

### 更新履歴

| 日付 | 更新内容 | 更新者 |
|------|---------|--------|
| 2026-01-31 | 初版作成 | Genspark |

### 更新方法

このファイルを更新する場合：
1. PR を作成
2. ユーザーがレビュー
3. マージ後、すべてのWEB版AIに通知

---

## 🎉 まとめ

### WEB版AIの作業の流れ

```
1. WebAgents.md を読む（このファイル）
   ↓
2. 自分専用のファイルを読む（WebXXX.md）
   ↓
3. 最新の実行結果を確認（results/gemini/）
   ↓
4. 指示書を作成（instructions/）
   ↓
5. 作業ログを記録（results/<ai名>/）
   ↓
6. ユーザーに報告
   ↓
7. ユーザーがGemini CLIで実行
   ↓
8. 実行結果を確認（results/gemini/）
   ↓
9. 必要に応じて修正指示書を作成
```

---

**重要**: このファイルは、すべてのWEB版AIの「共通ルールブック」です。  
**作業を開始する前に必ず読んでください。**

---

**作成日**: 2026-01-31  
**対象**: Claude.ai / ChatGPT / Genspark  
**バージョン**: 1.0.0  
**次回更新**: 必要に応じて
