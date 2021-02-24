# coding: utf-8

import codecs
import json
import os
import pandas as pd
import sys

import settings

class SearchCityCode(object):
    """
    入力CSVの郵便番号から市町村コードを検索した結果をCSVファイルに出力する
    settingsのRESULT_FILE_NAMEのファイル名で出力される
    """

    def __init__(self):
        self.root_dir = settings.ROOT_DIR
        self.data_dir = os.path.join(self.root_dir, "data")
        self.csv_dir = os.path.join(self.data_dir, "csv")
        self.json_dir = os.path.join(self.data_dir, "json")
        self.result_dir = os.path.join(self.data_dir, "result")
        self.prefectures_dir = os.path.join(self.data_dir, "prefectures")


    def main(self, input_file_name):
        """
        メインルーチン

        引数:
          input_file_name 入力ファイル名
        """

        # 入力CSVファイルを読み込み
        data = self.read_input_file(input_file_name)

        # 市町村コードを抽出
        result_data = self.search_citycode(data)

        # 結果ファイルを出力
        self.out_file(result_data)


    def search_citycode(self, data):
        """
        引数dataで受けたデータの各列に対して郵便コードから市町村コードを抽出する

        引数:
          data 入力データ(Pandas DataFrame)
        戻り値: 
          result_data　整形後データ(Pandas DataFrame)
        """

        # 市町村コードを格納する列を追加する
        result_data = data.assign(
            E=0,
            F=0,
            G=0,
            H=0,
            I=0,
            J=0,
            K=0,
            L=0,
            M=0,
            N=0,
        )
        print(result_data)

        #  DataFrameをループ
        for num, row in enumerate(result_data.itertuples(name=None)):
            # 郵便番号を抽出
            # 7桁ゼロパディング
            post_code = str(int(row[2]))
            post_code = post_code.zfill(7)

            # 都道府県コードを抽出
            # 5桁ゼロパディング
            prefecture_code = str(int(row[3]))
            prefecture_code = prefecture_code.zfill(2)

            # 対象都道府県の郵便番号JSONを開く
            city_code_json = self.read_citycode_file(prefecture_code)

            # 郵便番号から市町村コードを検索
            try:
                post_code_dict = city_code_json.get(post_code, None)

                if post_code_dict is None:
                    # 郵便番号がヒットしない場合は「候補1」にERRORを格納
                    result_data.iloc[num, 4] = "ERROR"
                else:
                    # 郵便番号がヒットした場合候補に値を格納
                    city_codes = post_code_dict["city_codes"]

                    for i, city_code in enumerate(city_codes):
                        print(city_code)
                        result_data.iloc[num, 4 + i] = city_code
            except Exception:
                # エラーの場合は「候補1」にERRORを格納
                result_data.iloc[num, 4] = "ERROR"

        return result_data


    def read_input_file(self, file_name):
        """
        引数file_nameで受けたファイル名のCSVファイルを読み込む

        引数:
          file_name ファイル名
        戻り値:
          data データ(Pandas DataFrame)
        """
        # データ読み込み
        data = pd.read_csv(file_name, encoding="SHIFT-JIS")
        print(data)

        return data


    def read_citycode_file(self, prefecture_key):
        """
        引数prefecture_keyで受けたファイル名のJSONファイルを読み込む

        引数:
          prefecture_key 都道府県コード(文字列型)
        戻り値:
          data データ(dict型)
        """
        # 戻り値変数生成
        data = {}

        # ファイル名生成
        file_name_raw = prefecture_key + ".json"
        file_name = os.path.join(self.json_dir, file_name_raw)

        # データ読み込み
        with codecs.open(file_name, "r", encoding="utf-8") as f:
            data = json.load(f)
            f.close()

        return data[prefecture_key]


    def out_file(self, data):
        """
        引数dataで受けたデータをCSVファイルとして出力する
        出力先はresult_dir

        引数:
          data: 出力データ(Pandas DataFrame)
        戻り値: なし
        """
        # ファイル名生成
        file_name_raw = settings.RESULT_FILE_NAME
        file_name = os.path.join(self.result_dir, file_name_raw)

        # ファイルにデータ保存
        data.to_csv(file_name)

if __name__ == "__main__":
    # 引数を抽出
    argvs = sys.argv
    input_file_name = argvs[1]

    # settings.pyのINPUT_FILE_DIRとファイルパスを結合
    input_file = os.path.join(settings.INPUT_FILE_DIR, input_file_name)

    # メインルーチン実行
    citycode_obj = SearchCityCode()
    citycode_obj.main(input_file)