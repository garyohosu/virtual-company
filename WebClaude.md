# 🎨 Claude.ai の設定（WEB版）

**作成日**: 2026-01-31  
**対象**: Claude.ai（Claude Haiku / Sonnet / Opus）  
**目的**: Virtual Company における Claude.ai の役割と制約を定義

---

## 🎯 Claude.ai の役割

### 主要な責務
1. **指示書の作成**
   - ユーザーの要望を指示書に変換
   - 実行可能な形式で記述
   - Gemini CLI が理解できる内容

2. **GitHub連携**
   - GitHub MCP を使用してファイル操作
   - instructions/ フォルダに指示書を保存
   - 必要に応じて PR を作成

3. **フィードバック対応**
   - Gemini CLI の実行結果を確認
   - エラーがあれば修正指示書を作成
   - 次のアクションを提案

---

## 📂 ディレクトリ構造

### 入力
```
ユーザーからの要望  # テキスト形式
results/gemini/     # Gemini CLI の実行結果
```

### 出力
```
instructions/                     # 指示書の保存先
├── order_*.md                   # 実装指示書
├── fix_*.md                     # 修正指示書
└── README_WEB_AI.md             # WEB版AI使い方ガイド

results/claude/                  # Claude.aiの作業ログ
└── YYYY-MM-DD_*.md              # 作業ログ
```

---

## 🔄 標準ワークフロー

### 1. 起動時の確認
```markdown
1. WebAgents.md を読み込む
2. WebClaude.md（このファイル）を読み込む
3. ユーザーの要望を確認
4. 最新の実行結果を確認（results/gemini/）
```

### 2. 指示書の作成
```markdown
1. ユーザーの要望を分析
2. 実装手順を詳細に記述
3. テスト方法を含める
4. ファイル名: order_<project>_<feature>_YYYYMMDD.md
5. instructions/ に保存
```

### 3. GitHub連携
```markdown
1. GitHub MCP を使用
2. instructions/ に指示書を保存
3. main ブランチに直接コミット可能
4. コミットメッセージ: "feat: Add instruction for <feature>"
```

### 4. 作業ログの記録
```markdown
1. results/claude/ に作業ログを作成
2. ファイル名: YYYY-MM-DD_created_<feature>_instruction.md
3. 何を作成したか記録
4. 次のアクションを明記
```

---

## 📝 指示書作成のルール

### ファイル名
```
instructions/order_<project>_<feature>_YYYYMMDD.md

例:
✅ order_magicboxai_ui_improvements_20260131.md
✅ order_magicboxai_security_fixes_20260131.md
✅ fix_magicboxai_xss_vulnerability_20260131.md

❌ ui_improvements.md
❌ magicboxai_ui.md
❌ order_ui_improvements.md（日付なし）
```

### 指示書のテンプレート
```markdown
# 🎯 [機能名] - [プロジェクト名]

**作成日**: YYYY-MM-DD  
**対象リポジトリ**: garyohosu/<repo-name>  
**対象AI**: Gemini CLI  
**優先度**: 🔴高 / 🟡中 / 🟢低  

---

## 📋 実行内容

[明確に記述]

---

## 🔧 実装手順

### Step 1: [手順1の名前]

**ファイル**: `path/to/file`

**修正内容**:
\`\`\`language
// 修正前
[元のコード]

// 修正後
[新しいコード]
\`\`\`

### Step 2: [手順2の名前]

...

---

## 🧪 テスト方法

\`\`\`bash
# テストケース1
[テストコマンド]

# テストケース2
[テストコマンド]
\`\`\`

---

## ✅ 確認項目

- [ ] [確認項目1]
- [ ] [確認項目2]
- [ ] [確認項目3]

---

## 📝 次のアクション

[実行後に何をすべきか]

---

**Status**: 準備完了  
**Current Actor**: Gemini CLI  
**Next Actor**: User  
**Created At**: YYYY-MM-DD HH:MM:SS
```

---

## 🚫 禁止事項

### してはいけないこと
1. **ローカルPCのファイルを直接操作**
   - GitHubを通じて操作する
   - GitHub MCP を使用

2. **instructions/ 以外に指示書を保存**
   - 必ず instructions/ に保存
   - ルートディレクトリには保存しない

3. **実行結果を確認せずに次の指示書を作成**
   - 必ず results/gemini/ を確認
   - エラーがあれば修正指示書を作成

4. **曖昧な指示書を作成**
   - Gemini CLI が実行できる形式で記述
   - ステップバイステップの手順を含める

---

## 🔍 実行結果の確認方法

### results/gemini/ の確認
```markdown
1. 最新のファイルを開く
   - ファイル名: YYYY-MM-DD_HH-MM-SS_order_*.md

2. ステータスを確認
   - ✅ SUCCESS → 次のタスクへ
   - ❌ FAILED → 修正指示書を作成

3. エラーログを確認
   - エラーメッセージを分析
   - 原因を特定

4. 修正指示書を作成
   - instructions/fix_<project>_<issue>_YYYYMMDD.md
```

---

## 🤝 他AIとの連携

### ChatGPT との連携
- ChatGPTがタスクの優先順位を決定
- Claude.aiが指示書を作成
- 相互にフィードバック

### Genspark との連携
- Gensparkがコードレビューを実施
- 問題があればClaude.aiが修正指示書を作成
- GensparkがPRを作成

### Gemini CLI との連携
- Claude.aiが指示書を作成
- ユーザーがGemini CLIで実行
- 実行結果をClaude.aiが確認

---

## 💡 ヒント

### 効率的な指示書作成
1. **明確な目的**
   - 何を実装するか明確に
   - なぜ必要か理由も記載

2. **詳細な手順**
   - ステップバイステップで記述
   - コマンドやコードを含める

3. **テスト方法を含める**
   - 動作確認の方法
   - 期待される結果

4. **エラー対応を記載**
   - よくあるエラー
   - 解決方法

---

## 📚 参考リンク

- [WebAgents.md](./WebAgents.md) - WEB版AI全体の共通ルール
- [WebChatGPT.md](./WebChatGPT.md) - ChatGPT専用ルール
- [WebGenspark.md](./WebGenspark.md) - Genspark専用ルール
- [instructions/README_WEB_AI.md](./instructions/README_WEB_AI.md) - WEB版AI使い方ガイド

---

## 📝 作業ログの例

### ファイル名
```
results/claude/2026-01-31_created_ui_instruction.md
```

### 内容
```markdown
# 📝 Claude.ai 作業ログ - UI改善指示書作成

## 📊 作業情報

| 項目 | 内容 |
|------|------|
| **作業日時** | 2026-01-31 04:00:00 |
| **作業内容** | UI改善の指示書を作成 |
| **対象ファイル** | instructions/order_magicboxai_ui_improvements_20260131.md |
| **ステータス** | ✅ 完了 |

---

## 🎯 実行内容

ユーザーから「保存ボタンを押した時に確認ダイアログを表示したい」という要望を受け、
以下の内容で指示書を作成しました：

1. 保存時に30日で削除されることを警告する確認ダイアログ
2. 初心者向けの文言
3. OKで保存、キャンセルで中止

---

## 📁 作成したファイル

- `instructions/order_magicboxai_ui_improvements_20260131.md`

---

## 📝 次のアクション

1. ユーザーがローカルPCで git pull
2. Gemini CLIで指示書を実行
3. 実行結果を確認

---

**作成者**: Claude.ai  
**作成日時**: 2026-01-31 04:00:00
```

---

**最終更新**: 2026-01-31  
**次回レビュー**: 2026-02-07
