# 🧠 Claude の永続記憶

**作成日**: 2026-01-31  
**対象**: Claude.ai（Claude Haiku）  
**目的**: 重要な設定情報と制約条件を記録

---

## 🎯 重要な制約・ルール

### ❌ ローカルPC が見えない

```
Claude からは見える：
✅ GitHub リポジトリ（GitHub MCP 経由）
✅ リモートの GitHub ファイル

Claude からは見えない：
❌ ローカルPC のファイル
❌ ローカルPC のディレクトリ構造
❌ Windows エクスプローラー
❌ ユーザーのマシンの状態
```

**覚えておくこと**: 何かローカルPCの情報が必要な場合は、**ユーザーからの報告を待つ**

---

## 📂 リポジトリ構造

### ユーザーのローカル PC

```
~/garyohosu/virtual-company/     ← ユーザーのメインリポジトリ（見えない）
├── instructions/                  ← すべての指示書がここ
│   ├── order_*.md                 （44個以上）
│   ├── CLAUDE_MEMORY.md           ← この ファイル
│   ├── MAGICBOXAI_FINAL_SETUP.md  ← Step 2-3-4 実装指示
│   ├── TEST_MAGICBOXAI_LOCAL.sh   ← ローカルテスト用
│   ├── VERIFY_MAGICBOXAI_CHROME.sh ← Chrome 検証用
│   ├── cleanup_organize_files.sh   ← ファイル整理用
│   └── ... その他指示書
├── magicboxai/
├── results/
├── scripts/
└── ... その他
```

### GitHub リポジトリ

```
garyohosu/virtual-company (GitHub)
└── instructions/
    ├── すべての指示書
    └── CLAUDE_MEMORY.md ← これを常に参照

garyohosu/magic-box-ai (GitHub)
├── src/                 (PHP ソース)
├── tests/               (テスト)
├── .github/workflows/   (CI/CD)
└── ... その他
```

---

## 📝 指示書作成ルール

### ✅ 必ず従うこと

```
1. すべての新しい指示書は以下に作成：
   https://github.com/garyohosu/virtual-company/tree/main/instructions

2. GitHub MCP を使用して作成：
   github:create_or_update_file で
   path: "instructions/FILENAME.md" または "instructions/FILENAME.sh"
   owner: "garyohosu"
   repo: "virtual-company"

3. 指示書の形式：
   - Bash スクリプト実行形式が望ましい
   - または Markdown ドキュメント形式
   - Gemini CLI で実行できるようにする

4. 指示書の先頭に以下を含める：
   - 実行方法: gemini --yolo instructions/FILENAME.md
   - 対象: (どのリポジトリか、どのディレクトリか)
   - 内容: (何をするのか)
```

---

## 🚀 新しい自動ワークフロー（最新！）

```
① Claude が GitHub に指示書を作成
   ↓
② ユーザーが git pull でローカルに取得
   ↓
③ ✨ Gemini が自動的に指示書を読んで実行 ✨
   ↓
④ garyohosu/magic-box-ai リポジトリに反映
   ↓
⑤ Gemini が自動的に git push
   ↓
⑥ ✅ 完了！
```

**重要**: Gemini は **git pull だけで** 指示書を自動読み込み → 自動実行 するようになりました！

---

## 📋 完了済みタスク

```
✅ Step 1: Python コード削除（virtual-company）
✅ Step 2-2: PHP コード同期（magic-box-ai に配置）
✅ Step 3: テスト戦略実装（PHPUnit + pytest）
✅ Step 4: CI/CD ワークフロー設定（GitHub Actions）
✅ Step X: order*.md ファイル整理（instructions/ に集約）
✅ ✅ ✅ すべての指示書は instructions/ に配置完了
✅ 永続記憶設定（CLAUDE_MEMORY.md）
✅ ローカルテスト用指示書作成
✅ Chrome 検証用指示書作成
✅ UI/UX 改良（Example Prompts + 保存確認ダイアログ）
```

**最新**: Gemini の自動実行機能が確認されました！

---

## ⏳ 次のステップ

```
1️⃣ GitHub Secrets 設定（手動）
   - SAKURA_HOST = garyo.sakura.ne.jp
   - SAKURA_USER = garyo
   - SAKURA_KEY = SSH 秘密鍵

2️⃣ git push でリモートにプッシュ
   - GitHub Actions が自動テスト実行
   - テスト成功で自動デプロイ

3️⃣ 本番環境確認
   - https://garyo.sakura.ne.jp/magicboxai/ にアクセス
   - Example Prompts が表示される
   - 保存完了画面が表示される
```

---

## 🔄 Claude の指示書作成ルール（改訂版）

### 指示書を作成する際のチェックリスト

```
□ 指示書を GitHub に作成（ローカルではなく GitHub に）
  └─ github:create_or_update_file 使用

□ パスを確認
  └─ path: "instructions/FILENAME.md"
  └─ owner: "garyohosu"
  └─ repo: "virtual-company"

□ 形式を確認
  └─ Bash スクリプト形式（*.sh）
  └─ または Markdown 形式（*.md）

□ ユーザーへの報告
  └─ 「指示書を作成しました」と報告
  └─ ユーザーが git pull すれば Gemini が自動実行

□ このファイルを参照
  └─ 忘れそうになったら CLAUDE_MEMORY.md を読む
```

---

## 🛠️ トラブルシューティング

### Q: 「どこに指示書を作成するのか忘れた」

**A**: このファイル（CLAUDE_MEMORY.md）を読む

```bash
curl https://raw.githubusercontent.com/garyohosu/virtual-company/main/instructions/CLAUDE_MEMORY.md
```

---

### Q: 「ローカルPCの状態がわからない」

**A**: ユーザーに確認する

```
「Gemini からレポートが来ましたか？」
「git pull だけで自動実行されましたか？」
```

---

### Q: 「指示書をどこに作成するのか」

**A**: 常にここ

```
https://github.com/garyohosu/virtual-company/tree/main/instructions/
```

---

## 📊 現在の状態

```
MagicBoxAI 開発状況：

✅ Phase 1: MagicBoxAI 完全実装
   ├─ PHP コード配置
   ├─ テスト環境構築
   ├─ CI/CD ワークフロー
   ├─ UI/UX 改良
   └─ 自動実行スクリプト

⏳ Phase 2: 本番デプロイ準備
   ├─ GitHub Secrets 設定（待機中）
   ├─ 自動デプロイ開始
   └─ 本番環境確認

🚀 新機能: Gemini 自動実行
   ├─ git pull だけで実行
   ├─ 指示書の自動読み込み
   └─ 自動コミット & プッシュ
```

---

## ⚠️ 注意事項

```
❌ やってはいけないこと：
   - ローカル PC のファイルを直接操作しようとする
   - GitHub 外の場所に指示書を作成する
   - 指示書を garyohosu/magic-box-ai に作成する

✅ やるべきこと：
   - すべての指示書を garyohosu/virtual-company/instructions/ に作成
   - GitHub MCP で GitHub リポジトリだけを操作
   - ユーザーからの報告を待つ
   - 不明な場合はこのファイルを参照
```

---

## 🔄 更新履歴

| 日付 | 更新内容 |
|-----|--------|
| 2026-01-31 | Claude の永続記憶ファイル作成 |
| 2026-01-31 | Gemini 自動実行機能を確認・記録 |
| 2026-01-31 | UI/UX 改良（Example Prompts + 確認ダイアログ） |
| 2026-01-31 | 新しい自動ワークフロー説明追加 |

---

**このファイルを常に参照してください！** 🧠✨
