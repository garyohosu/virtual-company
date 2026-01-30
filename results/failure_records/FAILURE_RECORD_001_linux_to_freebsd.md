# FAILURE RECORD 001 - Linux手順をFreeBSDに適用してしまった

## 概要
Sakura (FreeBSD) で Linux 前提の order を実行し、apt-get/systemd/certbot 前提が破綻した。

## 発生状況
- 対象: Sakura FreeBSD (shared hosting)
- 誤り: Linux向け手順 (apt-get, systemd, certbot)
- 結果: コマンドが存在しない/権限不足で停止

## 根本原因
- OS確認をせずに order を流用
- FreeBSD では pkg/rc.d が基本だが見落とし

## 影響
- 初期設定が進まず、後続作業が遅延

## 対応
- `uname -a` で OS を先に確認
- FreeBSD 専用手順に修正（pkg, rc.d, crontab）

## 再発防止
- order 冒頭に「OS確認ステップ」を追加
- Linux専用コマンドを使用する場合は明記
