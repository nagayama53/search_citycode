# coding: utf-8

import codecs
import json
import os
import pandas as pd
import sys

import settings

class CityCode(object):
    """
    郵便局のCSVデータから郵便番号と市町村コードを抽出したJSONファイルを作成する。
    都道府県コード.jsonというファイルで出力される
    """

    def __init__(self):
        self.root_dir = settings.ROOT_DIR
        self.data_dir = os.path.join(self.root_dir, "data")
        self.csv_dir = os.path.join(self.data_dir, "csv")
        self.json_dir = os.path.join(self.data_dir, "json")
        self.prefectures_dir = os.path.join(self.data_dir, "prefectures")


    def main(self):
        """
        メインルーチン
        """

        # 01から47まで(都道府県コード)ループ
        for num in range(1, 48):
            # 都道府県コードを生成
            prefecture_key = str(num)
            prefecture_key = prefecture_key.zfill(2)

            # CSVファイルを読み込み
            csv_data = self.read_file(prefecture_key)

            # データ整形
            data = self.make_citycode_dict(prefecture_key, csv_data)

            # JSONファイルを吐き出し
            self.out_file(prefecture_key, data)

        # 事業所CSVをJSON化
        key = settings.JIGYOSYO_FILE_NAME

        # CSVファイルを読み込み
        jigyo_csv_data = self.read_jigyo_file(key)

        # データ整形
        jigyo_data = self.make_citycode_dict(key, jigyo_csv_data)

        # JSONファイルを吐き出し
        self.out_file(key, jigyo_data)


    def make_citycode_dict(self, prefecture_key, data):
        """
        引数dataで受けたデータをJSONに整形する

        引数:
          prefecture_key 都道府県コード(文字列型)
          data 出力データ(Pandas DataFrame)
        戻り値: 
          result_data　整形後データ(dict型)
        """

        # dict作成
        # 返却用dict
        result_data = {prefecture_key: {}}

        # Tmp dict
        tmp_data = {}

        #  DataFrameをループ
        for row in data.itertuples(name=None):
            # 郵便番号を抽出
            # 7桁ゼロパディング
            post_code = str(row[2])
            post_code = post_code.zfill(7)

            # 市町村コードを抽出
            # 5桁ゼロパディング
            city_code = str(row[1])
            city_code = city_code.zfill(5)

            # tmp_dataのキーを抽出
            keys = list(tmp_data.keys())

            # 郵便番号がすでに返却データ配列に含まれている場合
            try:
                if post_code in keys:
                    post_code_dict = tmp_data[post_code]

                    # 市町村コードがリストに含まれていない場合
                    # 一つの郵便番号が複数の市町村コードに紐づく場合に対応
                    if city_code not in post_code_dict["city_codes"]:
                        post_code_dict["city_codes"].append(city_code)
                else:
                    # 郵便番号をキーに市町村コードを格納
                    tmp_data[post_code] = {
                        "city_codes": [city_code]
                    }
            except Exception:
                tmp_data[post_code] = {
                        "city_codes": ["ERROR"]
                    }

        result_data[prefecture_key] = tmp_data

        return result_data


    def read_file(self, prefecture_key):
        """
        引数prefecture_keyで受けたファイル名のCSVファイルを読み込む

        引数:
          prefecture_key 都道府県コード(文字列型)
        戻り値:
          data データ(Pandas DataFrame)
        """
        # ファイル名生成
        file_name_raw = prefecture_key + ".csv"
        file_name = os.path.join(self.csv_dir, file_name_raw)

        # データ読み込み
        # 常用外漢字が存在するためcp932で読み込み
        data = pd.read_csv(file_name, encoding="cp932", header=None, usecols=[0, 2])

        return data


    def read_jigyo_file(self, key):
        """
        引数keyで受けたファイル名のCSVファイルを読み込む
        事業所郵便番号CSVのデータ形式に合わせ1列目、8列目を取得する

        引数:
          key ファイル名(文字列型)
        戻り値:
          data データ(Pandas DataFrame)
        """
        # ファイル名生成
        file_name_raw = key + ".csv"
        file_name = os.path.join(self.csv_dir, file_name_raw)

        # データ読み込み
        # 常用外漢字が存在するためcp932で読み込み
        data = pd.read_csv(file_name, encoding="cp932", header=None, usecols=[0, 7])

        return data


    def out_file(self, prefecture_key, data):
        """
        引数dataで受けたデータをJSONファイルとして出力する
        出力先はjson_dir

        引数:
          prefecture_key: 都道府県コード(文字列型)
          data: 出力データ(dict型)
        戻り値: なし
        """
        # ファイル名生成
        file_name_raw = prefecture_key + ".json"
        file_name = os.path.join(self.json_dir, file_name_raw)

        # ファイルにデータ保存
        with codecs.open(file_name, "w", encoding="utf-8") as f:
            json.dump(data, f)
            f.close()

if __name__ == "__main__":
    # メインルーチン実行
    citycode_obj = CityCode()
    citycode_obj.main()