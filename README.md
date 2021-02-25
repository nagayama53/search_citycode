# search_citycode
郵便番号から市町村コードを検索する

## インストール
```
# python用行列演算ライブラリをインストール
$ pip install pandas
```

## 使い方
* data/csv/に郵便局の各県の郵便番号CSVを置く。命名規則は「都道府県コード.csv」。現在格納されているファイルは2021/2/24時点の最新版
* make_city_code.pyを使用して郵便番号データをJSONに整形する
  - 実行前にsettings.pyのROOT_DIRを変更すること
  ```
  $ cd src
  $ python make_citycode_json.py
  ```
* search_citycode.pyを使用して郵便番号から市町村コードを検索する
  - 実行前にsettings.pyのINPUT_FILE_DIRを変更すること。INPUT_FILE_DIRは検索用CSV格納ディレクトリ
  - 第一引数に検索用CSVを指定。検索用CSVはdata/sample/sample.csvを参照。
  - 検索用CSVは2列目に郵便番号、3列名に都道府県コードを格納すること
  - 結果ファイルはdata/result/に格納される
  ```
  $ python search_citycode.py sample.csv
  ```

## 仕様
* 都道府県をまたいで同じ郵便番号が存在する対策として、検索用CSVの都道府県コードを利用して、対象都道府県の郵便番号を検索します
* 同都道府県内の複数の市町村に同じ郵便番号が割り当たっている場合、最大10件まで候補を出力します
* 都道府県の郵便番号CSVにデータがない場合、事業者郵便番号を検索します
* 事業者郵便番号にもヒットしない場合、文字列「ERROR」を出力します