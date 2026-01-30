# FAILURE SUMMARY

## 目的
Virtual Company / MagicBoxAI の失敗パターンを記録し、再発防止と note 記事の素材にする。

## 収録内容
1. Linux手順をFreeBSDに適用
2. pydantic-core の Rust 依存ビルド失敗
3. Python 3.8 と pydantic-core 2.x の互換問題
4. SSH 並列作業による git 競合
5. 依存チェーンの不整合

## 共通の学び
- OS/環境の事前確認が最重要
- wheel 供給状況と Python バージョン互換を先に調べる
- 依存関係はセットで固定し、CI で検証する
- 並行作業は順序と pull/rebase を徹底

## 次のアクション
- note 記事化のためのプロット作成
- order テンプレートに「環境確認」ステップを追加
