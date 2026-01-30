# FAILURE RECORD 002 - pydantic-core が Rust 依存でビルド失敗

## 概要
Sakura で pydantic-core をソースビルドしようとして Rust/コンパイラ不足で失敗。

## 発生状況
- `pip install` 実行時に pydantic-core のビルドで停止
- エラー例: `Rust`/`setuptools-rust`/`maturin` が必要

## 根本原因
- 共有サーバーに Rust toolchain が無い
- wheel が無い環境でソースビルドにフォールバック

## 影響
- 依存解決が止まり、FastAPI 起動/テストが失敗

## 対応
- `pip --only-binary :all:` を優先
- Pythonバージョンに合う wheel を選定

## 再発防止
- requirements を wheel 供給済みバージョンに固定
- 事前に `pip debug --verbose` で互換性確認
