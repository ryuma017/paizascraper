# paizascr
paizaのスキルチェックの詳細結果一覧を取得するためだけのunkoライブラリです。
全てのプロセスが完了するのには、数十秒から数分かかる場合があります。

## コード例
    from paizascr import PaizaAuthentication

    email = 'your email'
    password = 'your password'

    pa = PaizaAuthentication(email=email, password=password)

    pa.login()

    pa.scrape_results(rank='b', shoud_display_log=True)

    all_submmited_probs = pa.all_submmited_problems
    cleared_probs = pa.cleared_problems
    uncleared_probs = pa.uncleared_problems

    print(f'--- <提出済み問題> 合計:{len(all_submmited_probs)} ---', *all_submmited_probs, sep='\n')
    print(f'--- <100点の問題> 合計:{len(all_submmited_probs)} ---', *cleared_probs, sep='\n')
    print(f'--- <100点未満の問題> 合計:{len(all_submmited_probs)} ---', *uncleared_probs, sep='\n')

    pa.logout()
