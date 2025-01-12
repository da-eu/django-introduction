async function login() {

    // フォームから各種データを取得
    const username = document.getElementById('id_username').value;
    const password = document.getElementById('id_password').value;
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    try {
        // APIリクエストを送信
        const response = await fetch('/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken // CSRFトークンを送信
            },
            body: JSON.stringify({ username, password }),
        });

        // レスポンスの成功判定
        if (!response.ok) {
            // 失敗した場合はエラーメッセージを返す
            const data = await response.json();
            throw new Error(data.detail || 'ログインに失敗しました');
        }

        const data = await response.json();

        // レスポンスを処理
        if (data.token) {
            // トークンを保存
            localStorage.setItem('access_token', data.token);

            // リダイレクトの処理
            const userId = data.user_id; // ユーザーIDを取得
            const redirectUrl = `/forum/user/${userId}`; // リダイレクトURLを生成
            window.location.href = redirectUrl; // 指定のURLにリダイレクト
        } else {
            throw new Error('トークンの取得に失敗しました');
        }
    } catch (error) {
        // エラーメッセージの処理
        console.error('Login failed:', error);

        const table = document.getElementById('login-table');

        // 既存のエラーメッセージ行がある場合は削除
        const existingErrorRow = table.querySelector('.error-row');
        if (existingErrorRow) {
            table.deleteRow(existingErrorRow.rowIndex);
        }

        // 新しいエラーメッセージ行を挿入
        const tr = table.insertRow(0);
        tr.classList.add('error-row'); // エラーメッセージ用のクラスを追加
        const td = tr.insertCell(0);
        td.colSpan = 2;
        td.textContent = error.message || '原因不明のエラーが発生しました';
    }
}

function initEvent() {
    // フォームの送信イベントに対するイベントハンドラーを設定
    document.getElementById('login-form').addEventListener('submit', function(event) {
        // ボタンクリックによるフォーム送信を無効化
        event.preventDefault();

        // ログインとトークンの記録を実施
        login()
    });
}

initEvent();