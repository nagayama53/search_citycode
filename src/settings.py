# coding: utf-8
"""
本ファイルには環境ごとに設定する定数を格納する
"""

import re

# ソースコード検索のルートディレクトリを指定
# data, srcディレクトリを配置したディレクトリを指定
ROOT_DIR = "F:\development\city_code\search_citycode"

# 入力ファイルの格納ディレクトリを指定
INPUT_FILE_DIR = "F:\development\city_code\search_citycode\sample"

# 結果ファイル名
RESULT_FILE_NAME = "result.csv"

# 都道府県の正規表現を格納
prefecture_regex = re.compile(r'北海道|青森県|岩手県|宮城県|秋田県|山形県|福島県|茨城県|栃木県|群馬県|埼玉県|千葉県|東京都|神奈川県|新潟県|富山県|石川県|福井県|山梨県|長野県|岐阜県|静岡県|愛知県|三重県|滋賀県|京都府|大阪府|兵庫県|奈良県|和歌山県|鳥取県|島根県|岡山県|広島県|山口県|徳島県|香川県|愛媛県|高知県|福岡県|佐賀県|長崎県|熊本県|大分県|宮崎県|鹿児島県|沖縄県')