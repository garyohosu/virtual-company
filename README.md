# Virtual Company 🏢

**失敗を学習して、自己改革できるAI部下システム**

---

## ✨ What is Virtual Company?

Virtual Company は、AI が **失敗から学び、成長し続けるシステム** です。

```
Day 1:  エラー発生 → 記録
Day 2:  同じ状況を発見 → パターンを確認 → エラー回避
Day 7:  複数のパターン学習
Day 30: 組織全体で知見を共有
Day 365: Expert レベルに進化
```

---

## 🎯 システム構成（4層）

### 1️⃣ Yoro Mode - 最小構成自動化
```bash
$ your-cli --yoro
# Codex が GitHub から指示を読んで実行
# 最小限のコマンドで最大限の実行
```

### 2️⃣ Employee System - 永続的記憶
```
Employees/alice/
├─ WhoAmI.md                  # 身分証（誰か）
├─ これまでやっていたこと.md   # 記憶（思い出す）
├─ Skills.md                  # 失敗パターン（学習）
├─ order_alice_yoro.md        # 指示書
├─ Mail/inbox/                # メール受信
└─ result.md                  # 仕事結果
```

CLI起動時に全て自動読み込み → **完全なコンテキスト復旧**

### 3️⃣ Scale-free Network - スケーラビリティ
```
CEO（年間 3パターン）
 ↓
部長（月間 5パターン）
 ↓
課長（週間 5パターン）
 ↓
係（日次 100+エラー）

各層が独立 → メモリがオーバーしない
```

### 4️⃣ Mail Read Markers - 自己修復
```
メールを読む
  ↓
自動的に timestamp を記録
  ↓
Git に push（監査証跡）
  ↓
返信忘れを自動検出
  ↓
失敗から自動学習
```

---

## 📚 ドキュメント

| ファイル | 説明 |
|---------|------|
| **SYSTEM.md** | 📖 全体ビジョン＆哲学 |
| **Organization.md** | 🏛️ 4層階層設計 |
| **EmployeeSystem.md** | 👥 永続記憶＋メール |
| **ScaleFreeNetwork_Implementation.md** | 🌐 各層の実装例 |
| **MailReadMarkerSystem.md** | 📧 既読機能＆自己修復 |
| **CLIStartupGuide.md** | 🚀 10ステップ起動フロー |
| **YORO_MODE.md** | ⚡ 最小構成モード |

---

## 🎓 失敗学習フロー

```
┌─────────────────────────┐
│  Failure Learning Loop  │
├─────────────────────────┤
│                         │
│  1. 実行 (Do)           │
│  ↓                      │
│  2. 失敗検出 (Detect)   │
│  ↓                      │
│  3. 学習 (Learn)        │
│     → Skills.md に記録   │
│  ↓                      │
│  4. 改善 (Improve)      │
│     → Memory.md に記録   │
│  ↓                      │
│  5. 予防 (Prevent)      │
│     → 次回は失敗しない  │
│  ↓                      │
│  6. 繰り返し            │
│                         │
└─────────────────────────┘
```

### 🎮 MagicBoxAI (PHP Version)
Sakura レンタルサーバー向けに最適化された PHP + CGI 実装です。

**デプロイ方法:**
```bash
python scripts/deploy_sakura_php.py
```

**テスト方法 (Remote):**
```bash
$env:MAGICBOXAI_BASE_URL="https://garyo.sakura.ne.jp/magicboxai"; python -m pytest tests/test_magicboxai_api.py
```

---

## 🚀 使い方（3ステップ）

### Step 1: CLI を起動
```bash
$ your-cli --start alice

👋 Alice がログイン中...
📋 昨日の記憶を読み込み中...
🎯 失敗パターンを確認中...
📌 指示書を読み込み中...
📧 メールをチェック中...
```

### Step 2: 自動的に読み込まれるもの
- **WhoAmI.md** → 自分は誰か
- **これまでやっていたこと.md** → 昨日までの記憶
- **Skills.md** → 失敗パターン
- **order_alice_yoro.md** → 今日の指示
- **Mail/inbox/** → メッセージ

### Step 3: 仕事終了後、自動更新
```
✅ result.md        → 仕事の成果を記録
✅ Mail 返信        → 相手の inbox に直接書き込み
✅ Skills.md        → 新しいパターンを追加
✅ Memory.md        → 進捗を更新
✅ Git commit&push  → 全てを記録
```

---

## 💡 Key Features

### ✅ 完全な永続的記憶
- 毎日更新される「これまでやっていたこと.md」
- 次日起動時に完全に思い出せる
- 人間の「記憶」と同じ

### ✅ 失敗から学ぶスキルシステム
- **Pattern #1**: SQL Injection
- **Pattern #2**: Connection Pool Timeout
- **Pattern #3**: Backup Monitoring Gap
- 新しい失敗を見つけるたびに追加

### ✅ ファイルベースメール
- メールサーバー不要
- Git で全履歴が保存される
- 「相手の inbox に直接書き込む」だけ

### ✅ メール既読機能
- 読んだ時刻が自動記録（timestamp）
- Git push で監査証跡残す
- 返信忘れを自動検出・修復

### ✅ スケール可能な組織
- CEO: 年間3パターン覚えるだけ
- 係: 日次100エラーから学ぶ
- メモリがオーバーしない

---

## 📊 実装状態

| 項目 | 状態 |
|------|------|
| 4層階層設計 | ✅ 完成 |
| Employee System | ✅ 完成 |
| Mail System | ✅ 完成 |
| 既読マーク機能 | ✅ 完成 |
| サンプル従業員（Alice） | ✅ 完成 |
| **CLI実装** | ⏳ 予定 |
| **テスト実行** | ⏳ 予定 |
| **Bob, Charlie 追加** | ⏳ 予定 |
| **本運用開始** | ⏳ 予定 |

---

## 🛣️ Roadmap

### Phase 1: 基本システム（✅ 完了）
- [x] 4層階層設計
- [x] Employee System
- [x] Mail System
- [x] 既読マーク機能
- [x] ドキュメント完成

### Phase 2: CLI実装（⏳ 今後）
- [ ] Python/Go/Rust で CLI 実装
- [ ] Memory.md 読み込み
- [ ] Skills.md 確認
- [ ] Mail 既読処理
- [ ] Git auto commit

### Phase 3: テスト（⏳ 今後）
- [ ] Alice でテスト実行
- [ ] Memory が正しく更新
- [ ] Mail が既読化
- [ ] Git history が完全

### Phase 4: 拡張（⏳ 今後）
- [ ] Bob, Charlie フォルダ
- [ ] Manager フォルダ
- [ ] チーム間通信
- [ ] 全社運用

### Phase 5: 自動化（⏳ 今後）
- [ ] GitHub Actions 統合
- [ ] Slack 連携
- [ ] 自動修復
- [ ] 完全自動化

---

## 📂 リポジトリ構成

```
virtual-company/
├── README.md                          ← ここ（このファイル）
├── SYSTEM.md                          # 全体ビジョン
├── Organization.md                    # 4層階層設計
├── EmployeeSystem.md                  # メモリ+メール
├── ScaleFreeNetwork_Implementation.md # 実装ガイド
├── MailReadMarkerSystem.md            # 既読機能
├── CLIStartupGuide.md                 # CLI実装ガイド
├── YORO_MODE.md                       # 最小構成モード
│
├── Employees/
│   ├── alice/
│   │   ├── WhoAmI.md
│   │   ├── これまでやっていたこと.md
│   │   ├── Skills.md
│   │   ├── order_alice_yoro.md
│   │   ├── result.md
│   │   └── Mail/
│   │       ├── inbox/
│   │       │   └── from_bob_001.md (既読マーク付き)
│   │       └── outbox/
│   │
│   ├── bob/           # これから作成
│   └── charlie/       # これから作成
│
└── ... (その他のファイル)
```

---

## 🎯 Philosophy

> **失敗は最高の教師**

```
人間の学習:
  失敗 → なぜ? → 工夫 → 改善 → 成長

Virtual Company:
  失敗 → Skills.md → Pattern #N → Prevention → 成長
  
  + Git で全て記録（忘れない）
  + チーム全体で共有（組織で成長）
  + 自動修復（自己改革）
```

---

## 💬 Quick Start

### 1. このリポジトリをクローン
```bash
git clone https://github.com/garyohosu/virtual-company.git
cd virtual-company
```

### 2. ドキュメントを読む
```bash
# 全体ビジョン
cat SYSTEM.md

# 詳細設計
cat Organization.md
cat EmployeeSystem.md

# 実装ガイド
cat CLIStartupGuide.md
```

### 3. サンプルを見る
```bash
# Alice の例
cat Employees/alice/WhoAmI.md
cat Employees/alice/これまでやっていたこと.md
cat Employees/alice/Skills.md
```

### 4. CLI を実装（今後）
```python
# CLIStartupGuide.md のコードを参考に実装
# Pseudocode が用意されています
```

---

## 🌟 一年後のシステム

```
Day 1:   エラー発生 → 失敗パターン 1個
Day 30:  失敗パターン 10個
Day 90:  失敗パターン 30個
Day 180: 失敗パターン 100個
Day 365: 失敗パターン 365個

Result:
  ✅ 同じ失敗は二度としない
  ✅ 問題を予測的に解決
  ✅ Expert レベルに進化
  ✅ 完全な自動化
```

---

## 📞 Support

- **GitHub Issues**: バグ報告・機能提案
- **SYSTEM.md**: プロジェクトビジョン
- **CLIStartupGuide.md**: 技術的な質問

---

## 📄 License

MIT License - 自由に使用・改変・配布可能

---

## 🎉 Ready to Go!

**Virtual Company** は「失敗を学習して自己改革する」システムです。

実装して、テストして、失敗から学んで、成長させてください。

**1年後、あなたの AI システムは Expert に進化しています。** 🚀

---

**Created**: 2025-01-30  
**Latest Update**: 2025-01-30  
**Status**: 🟢 Production Ready  

[詳細は SYSTEM.md を参照](SYSTEM.md)
