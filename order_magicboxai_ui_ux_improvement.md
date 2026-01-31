# Order - MagicBoxAI UI/UX 改善（初心者向け）

**Status**: ⏳ UX 改善実装待ち
**Current Actor**: Gemini CLI
**Goal**: 初心者ユーザーが安心して使える UI に改善
**Output**: 修正済みの index.php と pages/home.php を Sakura にデプロイ

---

## 🎯 ミッション

初心者ユーザーが「データが消えて困った」という苦情を避けるために、UI/UX を改善する

---

## 📋 改善内容

### 改善 1: 「30日で消えます」を目立つようにする

**現在**:
```
小さな灰色テキスト
「30日で消えます」
```

**改善後**:
```
📢 大きな赤い警告ボックス

⚠️ 重要なお知らせ

このページは **30日後に自動で削除** されます。

大切なファイルは保存し直してください。
```

### 改善 2: 保存ボタン押下時に確認ダイアログ

**現在**:
```
[保存] ボタン → すぐに保存
```

**改善後**:
```
[保存] ボタン
  ↓
ダイアログ表示:
"このファイルはこのページから 30日後に自動削除されます。
 大切な場合は別途保存してください。

 本当に保存してよろしいですか？"

[はい、保存します] [キャンセル]
```

### 改善 3: 保存後、URL 共有方法を大きく表示

**現在**:
```
小さなテキスト + 小さなコピーボタン
```

**改善後**:
```
📋 あなたの保存ファイル

共有用 URL:
┌─────────────────────────┐
│ https://garyo.sakura... │
└─────────────────────────┘

[コピー] [開く]

⏰ このリンクは 30日で自動削除されます
```

### 改善 4: 初心者向けのメッセージ追加

**トップに追加**:
```
👋 初めての方へ

1. HTML コードを左の枠に貼り付け
2. [プレビュー] で確認
3. [保存] で URL を生成
4. URL を友達に共有

💡 ファイルは 30日で自動削除されます
```

---

## 🔧 実装内容

### pages/home.php の改善

```php
<!-- 1. ヘッダーにわかりやすいタイトル -->
<div class="hero-section">
  <h1>🎮 MagicBoxAI</h1>
  <p>HTML コードを貼り付けたら、すぐに動作確認</p>
  <p class="subtitle">Powered by PHP + CGI (Sakura 最適化版)</p>
</div>

<!-- 2. 初心者向けガイド（目立つボックス） -->
<div class="beginner-guide">
  <h2>👋 初めての方へ</h2>
  <ol>
    <li>左の枠に HTML コードを貼り付け</li>
    <li><button>プレビュー</button> で確認</li>
    <li><button>保存</button> で共有用 URL を生成</li>
    <li>URL を友達に共有</li>
  </ol>
</div>

<!-- 3. 警告ボックスを大きく表示 -->
<div class="warning-box">
  <h3>⚠️ 重要なお知らせ</h3>
  <p class="large-text">
    このページは <strong>30日後に自動で削除</strong> されます。
  </p>
  <p>大切なファイルは、パソコンに別途保存してください。</p>
</div>
```

### JavaScript: 確認ダイアログ

```javascript
// 保存ボタンをクリックしたときのダイアログ
document.getElementById('saveButton').addEventListener('click', function() {
  const confirmed = confirm(
    '⏰ 注意！\n\n' +
    'このファイルは 30日後に自動で削除されます。\n' +
    '大切な場合は、パソコンに別途保存してください。\n\n' +
    '本当に保存してよろしいですか？'
  );
  
  if (confirmed) {
    // 保存処理を実行
    saveFile();
  }
});

// 保存後、URL 表示時のダイアログ
function showSaveSuccess(token) {
  const url = `${window.location.origin}/magicboxai/view/${token}`;
  
  const html = `
    <div class="success-dialog">
      <h2>✅ 保存しました！</h2>
      <p>以下の URL を友達と共有できます：</p>
      
      <div class="url-box">
        <input type="text" value="${url}" readonly>
        <button onclick="copyToClipboard('${url}')">📋 コピー</button>
        <button onclick="window.open('${url}', '_blank')">🔗 開く</button>
      </div>
      
      <p class="warning">⏰ このリンクは 30日で自動削除されます</p>
      
      <button onclick="closeDialog()">閉じる</button>
    </div>
  `;
  
  showModal(html);
}

// クリップボードにコピー
function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    alert('URL をコピーしました！');
  });
}
```

### CSS: スタイル改善

```css
/* ヘッダー */
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 40px;
  text-align: center;
  border-radius: 10px;
  margin-bottom: 30px;
}

.hero-section h1 {
  font-size: 48px;
  margin: 0;
}

/* ガイドボックス */
.beginner-guide {
  background: #f0f4ff;
  border-left: 5px solid #667eea;
  padding: 20px;
  margin-bottom: 30px;
  border-radius: 5px;
}

.beginner-guide ol {
  font-size: 18px;
  line-height: 2;
}

/* 警告ボックス */
.warning-box {
  background: #fff3cd;
  border: 3px solid #ff6b6b;
  padding: 30px;
  margin-bottom: 30px;
  border-radius: 10px;
  text-align: center;
}

.warning-box h3 {
  font-size: 28px;
  margin: 0 0 15px 0;
}

.warning-box .large-text {
  font-size: 22px;
  font-weight: bold;
  color: #d63031;
  margin: 10px 0;
}

.warning-box p {
  font-size: 16px;
  margin: 10px 0;
}

/* URL 表示ボックス */
.url-box {
  background: white;
  border: 2px solid #667eea;
  padding: 15px;
  margin: 20px 0;
  border-radius: 5px;
  display: flex;
  gap: 10px;
}

.url-box input {
  flex: 1;
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 3px;
}

.url-box button {
  padding: 10px 20px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  font-weight: bold;
}

.url-box button:hover {
  background: #5568d3;
}

/* 成功ダイアログ */
.success-dialog {
  background: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
  text-align: center;
}

.success-dialog h2 {
  font-size: 28px;
  color: #28a745;
  margin: 0 0 20px 0;
}

.success-dialog .warning {
  background: #fff3cd;
  border: 1px solid #ffc107;
  padding: 15px;
  border-radius: 5px;
  margin: 20px 0;
  font-weight: bold;
  font-size: 16px;
}
```

---

## ✅ 成功基準

- ✅ 「30日で消えます」が目立つ（大きさ・色・位置）
- ✅ 保存ボタン押下時に確認ダイアログが表示される
- ✅ URL 共有方法が目立つ
- ✅ 初心者向けガイドが表示される
- ✅ すべてのメッセージが日本語でわかりやすい
- ✅ 修正版が Sakura にデプロイされている

---

## 🚀 実装方法

Gemini が実行すること：

1. pages/home.php を修正（HTML + 警告ボックス拡大）
2. JavaScript を追加（確認ダイアログ）
3. CSS を更新（大きな警告・ガイド表示）
4. 修正ファイルを Sakura に scp で転送
5. ブラウザで動作確認

---

**Status**: UX 改善実装待ち

初心者ユーザーが「データが消えて困った」と言わないようなシステムを作ります。
