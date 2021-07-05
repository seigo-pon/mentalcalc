# mentalcalc
- Alexa Skill テストアプリ
- 子供の暗算問題自動生成機

## 開発環境
- Python 3.7
- ask-sdk-core
- AWS Lambda

## 使い方
1. ライブラリインストールしてコードを全てzip圧縮
1. Lambdaで「.zipファイルをアップロード」でアップロード

```
$ pip install ask-sdk-core -t skill
$ cd skill
$ cp ../calc.py .
$ cp ../mental_calc.py .
$ zip ../skill.zip . -r
```
