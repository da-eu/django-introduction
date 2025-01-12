async function updateCommentCount() {
    try {

        // localStorageからトークンを取得
        const token = localStorage.getItem('access_token');
        if (!token) {
            console.error('再度ログインを実施してください');
            return;
        }

        // APIリクエストを送信してコメントリストを取得
        const response = await fetch('/api/comments/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`, // トークンをヘッダーに追加
            },
        });

        if (response.ok) {
            const data = await response.json();
            const commentCount = data.length; // コメントの総数を取得

            // id="comment-count" の要素の値を更新
            const commentCountElement = document.getElementById('comment-count');
            commentCountElement.textContent = commentCount;
        } else {
            console.error('APIの実行に失敗しました:', response.statusText);
        }
    } catch (error) {
        console.error('コメント総数の更新に失敗しました:', error);
    }
}

// 一定間隔でコメントの総数を更新（2秒ごと）
setInterval(updateCommentCount, 2000);

// ページロード時に一度初期更新
updateCommentCount();