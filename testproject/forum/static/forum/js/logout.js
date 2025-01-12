async function logout() {

    // CSRFトークンを取得
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    
    // localStorage からトークンを削除
    localStorage.removeItem('access_token');
    
    try {
        // ログアウトAPIを実行
        response = await fetch('/api/logout/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken // CSRFトークンの送信
            },
        });

        // ログインページにリダイレクト
        window.location.href = '/forum/login/';
    } catch (error) {
        console.error('ログアウト中にエラーが発生しました:', error);
    }
}

function initEvent() {
    // フォームの送信イベントに対してイベントハンドラーを設定
    document.getElementById('logout-form').addEventListener('submit', function(event) {
        // ボタンクリックによるフォーム送信を無効化
        event.preventDefault();

        // ログアウトとトークンの削除を実施
        logout()
    });
}

initEvent();