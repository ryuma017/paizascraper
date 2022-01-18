# paizascr
paizaのスキルチェックの詳細結果一覧を取得するためだけのライブラリです。

### インストール
    ＄ pip install https://github.com/ryuma017/paizascraper.git

## コード例
    import paizascraper as ps

    email = 'your email'
    password = 'your passward'

    ps.login(email, password)
    user_name = ps.get_user_name()
    results_data = ps.get_results_data()

    print(user_name)
    print(*results_data.items(), sep='\n')
