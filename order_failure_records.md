# Order - 失敗記録・解決策のドキュメント化（note 記事用）

**Status**: ⏳ 失敗記録の整理待ち
**Current Actor**: Codex（ドキュメンテーション）
**Next Actor**: CEO（note 記事執筆）

---

## 🎯 ミッション

Virtual Company / MagicBoxAI 構築過程での失敗・解決策を整理し、
note の有料記事のネタとして記録します。

---

## 📋 失敗記録：実装順序別

### 失敗 1: Linux 向け Order を FreeBSD に直接適用

**発生時期**: Sakura デプロイ初期

**失敗内容**:
```
order_deploy_sakura.md は Linux 向けのみ
- apt-get コマンド（Debian/Ubuntu）
- systemd サービス（Linux）
- certbot の Linux 向け設定

Sakura は FreeBSD → 全部使えない ❌
```

**原因分析**:
- リサーチ不足：Sakura のOS を事前確認しなかった
- 設計ミス：Linux を前提に order を書いた

**解決策**:
```
✅ uname -a で OS 確認
✅ FreeBSD 専用 order を作成
✅ apt-get → pkg
✅ systemd → rc.d
✅ crontab は両 OS 共通
```

**学んだこと**:
```
「仮定するな、確認せよ」
ターゲット環境を明確にしてから order を書く
```

**note 記事での使い方**:
```
セクション: 「AI エージェントの落とし穴」
内容: クラウドサーバーの OS を確認せずに失敗した話
      → 再現可能な解決方法
```

---

### 失敗 2: pydantic-core が Rust コンパイラを要求

**発生時期**: Sakura 依存関係インストール時

**失敗内容**:
```
pip install -r requirements.txt でエラー

error: Microsoft Visual C++ 14.0 or greater is required.
  → Rust コンパイラがない
  → pydantic-core のビルドに失敗
```

**原因分析**:
- pydantic==2.5.0 → pydantic-core==2.14.0 に依存
- pydantic-core はソースコードからビルド必要
- Sakura FreeBSD に Rust がない

**失敗の過程**:
```
1. そのまま pip install → Rust エラー
2. Rust インストール試行 → ファイルサイズ大・時間かかる
3. wheel 版を探す → ❌ 該当バージョンなし
4. 古いバージョンに下げる → ✅ 成功
```

**解決策**:
```
✅ pip --only-binary :all: を使用
✅ または古いバージョン（Python 3.8 互換）を指定
```

**学んだこと**:
```
「新しいバージョンが常に最良ではない」
レンタルサーバーは古い環境 → 互換性が重要
```

**note 記事での使い方**:
```
セクション: 「レンタルサーバーと最新フレームワークの相性」
内容: FastAPI + Pydantic のバージョン互換性問題
      → 古いバージョンで動く理由
      → 依存関係チェーンの重要性
```

---

### 失敗 3: Python 3.8 に pydantic-core 2.14.0 wheel がない

**発生時期**: 2 回目のセットアップ試行時

**失敗内容**:
```
Sakura は Python 3.8 のまま
pydantic-core==2.14.0 は Python 3.9+ 向け
wheel がない → インストール失敗
```

**失敗の過程**:
```
1. pip install --only-binary で同じエラー
2. 「最新 pydantic は 3.8 未対応」に気付く
3. 古いバージョンを探す
4. fastapi==0.100.0 + pydantic==2.0.0 に変更
5. ✅ 成功
```

**解決策**:
```
✅ Python バージョンを先に確認
✅ 古いバージョンの互換マトリックスを作成
✅ 依存関係の下位互換性を確保
```

**学んだこと**:
```
「Python バージョンと依存関係は必ず確認」
3.8 → 3.9 のアップグレードより、古いバージョン使用が現実的
```

**note 記事での使い方**:
```
セクション: 「古いサーバー環境との付き合い方」
内容: Python 3.8 はもう古い？
      → でも世界中の本番サーバーはまだ 3.8
      → 互換性を保つ設計の重要性
```

---

### 失敗 4: SSH 並行実行による git 競合リスク

**発生時期**: 自動化設計時

**失敗内容**:
```
4 つの Codex を同時実行
→ 同時に git add & push
→ 競合の可能性（実際には起こらず）
```

**失敗を避けた方法**:
```
❌ 同時実行（4 つの DOS 窓）
✅ 順序付き実行（1 つずつ）
✅ ブランチ分離（並行 OK）
```

**学んだこと**:
```
「自動化でも git の競合管理は必須」
CI/CD での branch strategy が重要
```

**note 記事での使い方**:
```
セクション: 「マルチエージェント × Git の課題」
内容: AI 複数体が同時に GitHub を操作する時の競合戦略
      → ブランチ戦略の実装
      → 自動マージのルール
```

---

### 失敗 5: 依存関係バージョンチェーン

**発生時期**: 複数回の修正試行時

**失敗内容**:
```
fastapi のバージョン変更
  → uvicorn のバージョン確認忘れ
  → pydantic のバージョン確認忘れ
  → pytest の互換性確認忘れ

すべてがチェーンでつながっている
```

**失敗の過程**:
```
1. fastapi==0.104.1 を指定
2. uvicorn==0.24.0 は OK か？未確認
3. pydantic==2.5.0 は？
4. pytest は動く？
5. すべてをテストして初めて気付く
```

**解決策**:
```
✅ 依存関係マトリックスを事前に作成
✅ 各バージョン組み合わせをテスト
✅ requirements.txt を「動作確認済み」として保管
```

**学んだこと**:
```
「1 つのバージョンが全部に影響」
依存関係管理は自動化より手動確認が重要
```

**note 記事での使い方**:
```
セクション: 「依存関係地獄を解く」
内容: requirements.txt は「記録」ではなく「契約書」
      → テスト済みバージョン組み合わせの保持
      → lock ファイルの重要性
```

---

## 📝 出力ファイル

Codex が以下を作成：

```
results/failure_records/
├── FAILURE_RECORD_001_linux_to_freebsd.md
├── FAILURE_RECORD_002_pydantic_rust.md
├── FAILURE_RECORD_003_python38_wheel.md
├── FAILURE_RECORD_004_git_concurrency.md
├── FAILURE_RECORD_005_dependency_chain.md
├── FAILURE_SUMMARY.md（全失敗の総括）
└── NOTE_ARTICLE_IDEAS.md（note 記事案）
```

---

## 💡 note 記事の構成案

### 記事タイトル（失敗ドキュメント活用）

```
「AI エージェントで起業した。
  失敗してわかった『本番環境の現実』」

セクション：
1. 失敗 1: Linux と FreeBSD の違い
   → 環境確認の重要性

2. 失敗 2: 最新フレームワークと古いサーバー
   → バージョン互換性の問題

3. 失敗 3: Python 3.8 はまだ現役
   → 本番環境は進化が遅い

4. 失敗 4: マルチエージェント × Git
   → 自動化の落とし穴

5. 失敗 5: 依存関係地獄
   → lock ファイルが必要な理由

6. 解決策すべて
   → 再現可能な手順
   → 他の人が使える order ファイル
```

---

## ✅ 成功基準

以下がすべて完成すること：

- ✅ 失敗 1-5 の詳細ドキュメント作成
- ✅ 各失敗の原因分析
- ✅ 解決策の記述
- ✅ note 記事案の作成
- ✅ GitHub に push

---

**Status**: 失敗記録のドキュメント化準備完了
**価値**: 本番環境での課題を解決した実例
**販売価値**: ⭐⭐⭐⭐⭐ 高（他人の失敗は学習価値大）
