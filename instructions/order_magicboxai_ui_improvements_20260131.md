# 🎯 MagicBoxAI UI 改善指示書

**作成日**: 2026-01-31  
**対象**: magic-box-ai リポジトリ（Sakuraレンタルサーバー）  
**実行方法**: `gemini --yolo instructions/order_magicboxai_ui_improvements_20260131.md`

---

## 📋 改善内容

### ① 保存時の確認ダイアログ追加
**目的**: 30日で自動削除されることをユーザーに明確に伝え、クレーム防止

**実装**:
- 「保存」ボタンクリック時に確認ダイアログを表示
- 初心者向けのわかりやすい文言
- 「OK」で保存実行、「キャンセル」で中止

**文言例**:
```
⚠️ 保存する前に確認してください

保存したファイルは30日後に自動的に削除されます。
長期間保存したい場合は、ご自身のPCにダウンロードしてください。

このまま保存してもよろしいですか？

[キャンセル]  [保存する]
```

---

### ② URLコピー＆開くボタン追加
**目的**: 保存後のURL操作を簡単にする

**実装**:
- 保存完了後のURLセクションに2つのボタンを追加
  1. **「コピー」ボタン**: URLをクリップボードにコピー
  2. **「開く」ボタン**: 新しいタブでURLを開く

**配置イメージ**:
```
✅ 保存完了！
このURLを共有してください：
[https://garyo.sakura.ne.jp/magicboxai/view/xxxxx]
[コピー] [開く]

30日後に自動削除されます
```

---

### ③ ZIPダウンロード機能追加
**目的**: ユーザーが作成したHTMLファイルをローカルに保存できるようにする

**実装**:
- 保存完了後に「ZIPで渡す」ボタンを追加
- クリックすると `index.html` を含むZIPファイルをダウンロード
- ZIPファイル名: `magicboxai-{token}.zip`

**配置イメージ**:
```
✅ 保存完了！
このURLを共有してください：
[https://garyo.sakura.ne.jp/magicboxai/view/xxxxx]
[コピー] [開く] [ZIPで渡す]
```

---

### ④ サンプル例文とデモの追加
**目的**: 初心者がすぐに試せるように、具体例を提供

**実装**:
- トップページのテキストエリアの上に「使い方ガイド」セクションを追加
- クリック1つでサンプルコードをコピーできる

**サンプル例文**:

#### サンプル1: ボタンクリックでコピー機能
```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>テキストコピーツール</title>
    <script src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
    <style>
        body { font-family: sans-serif; padding: 20px; background: #f0f0f0; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }
        input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; }
        button { background: #667eea; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #764ba2; }
        .success { color: green; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="container" x-data="{ text: 'こんにちは！コピーしてみてください', copied: false }">
        <h1>📋 テキストコピーツール</h1>
        <input type="text" x-model="text" placeholder="コピーしたいテキストを入力">
        <button @click="navigator.clipboard.writeText(text); copied = true; setTimeout(() => copied = false, 2000)">
            📄 コピー
        </button>
        <p x-show="copied" class="success">✅ コピーしました！</p>
    </div>
</body>
</html>
```
**説明**: ボタンを押すとテキストがコピーされる簡単なツール

---

#### サンプル2: カウンターアプリ
```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>カウンターアプリ</title>
    <script src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
    <style>
        body { font-family: sans-serif; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
        .container { background: white; padding: 40px; border-radius: 12px; text-align: center; box-shadow: 0 10px 40px rgba(0,0,0,0.2); }
        .counter { font-size: 72px; font-weight: bold; color: #667eea; margin: 20px 0; }
        button { background: #667eea; color: white; padding: 15px 30px; margin: 5px; border: none; border-radius: 8px; cursor: pointer; font-size: 18px; }
        button:hover { background: #764ba2; }
        .reset { background: #e74c3c; }
        .reset:hover { background: #c0392b; }
    </style>
</head>
<body>
    <div class="container" x-data="{ count: 0 }">
        <h1>🔢 カウンターアプリ</h1>
        <div class="counter" x-text="count"></div>
        <button @click="count++">➕ 増やす</button>
        <button @click="count--">➖ 減らす</button>
        <button class="reset" @click="count = 0">🔄 リセット</button>
    </div>
</body>
</html>
```
**説明**: ボタンで数字を増減できるカウンター

---

#### サンプル3: ToDoリスト
```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>ToDoリスト</title>
    <script src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
    <style>
        body { font-family: sans-serif; padding: 20px; background: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 16px rgba(0,0,0,0.1); }
        input { width: 70%; padding: 12px; border: 1px solid #ccc; border-radius: 4px; font-size: 16px; }
        button { padding: 12px 24px; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer; margin-left: 10px; }
        button:hover { background: #764ba2; }
        ul { list-style: none; padding: 0; margin-top: 20px; }
        li { padding: 15px; background: #f9f9f9; margin: 10px 0; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; }
        .done { text-decoration: line-through; color: #999; }
        .delete-btn { background: #e74c3c; padding: 8px 16px; font-size: 14px; }
        .delete-btn:hover { background: #c0392b; }
    </style>
</head>
<body>
    <div class="container" x-data="{ todos: [], newTodo: '', addTodo() { if(this.newTodo.trim()) { this.todos.push({text: this.newTodo, done: false}); this.newTodo = ''; } }, toggleDone(index) { this.todos[index].done = !this.todos[index].done; }, deleteTodo(index) { this.todos.splice(index, 1); } }">
        <h1>📝 ToDoリスト</h1>
        <div>
            <input type="text" x-model="newTodo" @keyup.enter="addTodo()" placeholder="新しいタスクを入力...">
            <button @click="addTodo()">追加</button>
        </div>
        <ul>
            <template x-for="(todo, index) in todos" :key="index">
                <li>
                    <span :class="{ 'done': todo.done }" @click="toggleDone(index)" style="cursor: pointer; flex: 1;" x-text="todo.text"></span>
                    <button class="delete-btn" @click="deleteTodo(index)">削除</button>
                </li>
            </template>
        </ul>
        <p x-show="todos.length === 0" style="text-align: center; color: #999; margin-top: 20px;">タスクがありません</p>
    </div>
</body>
</html>
```
**説明**: タスクを追加・完了・削除できるToDoリスト

---

## 🎨 UI配置イメージ

### トップページ構成（改善後）

```
┌──────────────────────────────────────────────┐
│         🎮 MagicBoxAI                        │
│   HTML コードを貼り付けたら、すぐに動作確認   │
├──────────────────────────────────────────────┤
│                                              │
│ 💡 使い方ガイド                              │
│                                              │
│ JavaScriptでCDNを使ってindex.htmlの1ファイル │
│ で〇〇を作ってください。                      │
│                                              │
│ サンプル例:                                  │
│ [ボタンでコピー] [カウンター] [ToDoリスト]   │
│                                              │
├──────────────────────────────────────────────┤
│                                              │
│ 📝 HTML を貼り付け    │  🖼️ プレビュー      │
│ ┌──────────────────┐ │ ┌─────────────────┐ │
│ │ textarea         │ │ │  iframe         │ │
│ │                  │ │ │                 │ │
│ │                  │ │ │                 │ │
│ └──────────────────┘ │ └─────────────────┘ │
│ [プレビュー] [保存]   │                     │
│                      │ ✅ 保存完了！        │
│                      │ URL: [________]     │
│                      │ [コピー][開く]      │
│                      │ [ZIPで渡す]         │
│                      │ 30日後に自動削除    │
└──────────────────────────────────────────────┘
```

---

## 🔧 実装手順

### Step 1: home.php を更新

1. **確認ダイアログの追加**
   - `saveHtml()` 関数を修正
   - `confirm()` で確認メッセージを表示

2. **サンプル例セクションの追加**
   - ヘッダー下に「使い方ガイド」を追加
   - サンプルボタンをクリックでテキストエリアにコピー

3. **URLコピー＆開くボタンの追加**
   - `urlSection` に2つのボタンを追加
   - クリップボードAPI使用

4. **ZIPダウンロードボタンの追加**
   - `urlSection` にボタンを追加
   - 新しいAPI `/api/download-zip` を呼び出し

### Step 2: index.php に ZIP ダウンロード API を追加

```php
elseif (strpos($request_path, '/api/download-zip/') === 0) {
    $token = basename($request_path);
    handle_download_zip($token);
}

function handle_download_zip($token) {
    $save_dir = __DIR__ . '/data/uploads';
    $file_path = $save_dir . '/' . $token . '.html';
    
    if (!file_exists($file_path)) {
        http_response_code(404); 
        echo 'Not found'; 
        return;
    }
    
    $zip_path = $save_dir . '/' . $token . '.zip';
    $zip = new ZipArchive();
    
    if ($zip->open($zip_path, ZipArchive::CREATE | ZipArchive::OVERWRITE) === TRUE) {
        $zip->addFile($file_path, 'index.html');
        $zip->close();
        
        header('Content-Type: application/zip');
        header('Content-Disposition: attachment; filename="magicboxai-' . $token . '.zip"');
        header('Content-Length: ' . filesize($zip_path));
        readfile($zip_path);
        
        unlink($zip_path); // 一時ZIPを削除
    } else {
        http_response_code(500);
        echo 'ZIP creation failed';
    }
}
```

---

## ✅ 完成後の動作確認

1. **保存確認ダイアログ**
   - 「保存」ボタンをクリック
   - 確認メッセージが表示されることを確認
   - 「キャンセル」で中止、「保存する」で実行

2. **URLコピー機能**
   - 保存後に「コピー」ボタンをクリック
   - URLがクリップボードにコピーされることを確認

3. **URL開く機能**
   - 「開く」ボタンをクリック
   - 新しいタブで保存したページが開くことを確認

4. **ZIPダウンロード**
   - 「ZIPで渡す」ボタンをクリック
   - `magicboxai-xxxxx.zip` がダウンロードされることを確認
   - ZIPを解凍して `index.html` が含まれることを確認

5. **サンプル例**
   - 各サンプルボタンをクリック
   - テキストエリアにコードが挿入されることを確認
   - プレビューして正常に動作することを確認

---

## 📝 注意事項

- PHP環境で `ZipArchive` クラスが利用可能であること
- クリップボードAPIはHTTPS環境で動作（Sakuraサーバーは対応）
- 初心者向けの文言を重視すること
- エラーハンドリングを適切に実装すること

---

**このファイルを実行**:
```bash
cd ~/garyohosu/virtual-company
git pull origin main
gemini --yolo instructions/order_magicboxai_ui_improvements_20260131.md
```

実行後、ブラウザで `https://garyo.sakura.ne.jp/magicboxai/` にアクセスして動作確認してください。

---

**Status**: 準備完了  
**Current Actor**: Gemini  
**Next Actor**: User（動作確認）  
**Created At**: 2026-01-31
