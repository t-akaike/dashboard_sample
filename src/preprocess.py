#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import pandas as pd
import util

# パス取得
paths             = util.get_paths()
data_path         = paths['data_path']
input_path        = paths['input_path']
input_raw_path    = paths['input_raw_path']
input_unzip_path  = paths['input_unzip_path']


def merge_data():
    """
    ### サンプルデータ作成
    - kaggleのリクルートホールディングスのデータを加工
    """
    # データ解凍・読み込み
    for fname in ['air_visit_data', 'air_store_info']:
        util.unzip(f'{input_raw_path}/{fname}.csv.zip', input_unzip_path)
    df_visit = pd.read_csv(f'{input_unzip_path}/air_visit_data.csv')
    df_store = pd.read_csv(f'{input_unzip_path}/air_store_info.csv')

    (
        df_visit
        .merge(df_store, on='air_store_id', how='left')
        .assign(
            pref_name=lambda x : x['air_area_name']
            .str.split(' ')
            .str.get(0)
            .str.replace('Tōkyō-to'     , '東京都')
            .str.replace('Ōsaka-fu'     , '大阪府')
            .str.replace('Hokkaidō'     , '北海道')
            .str.replace('Shizuoka-ken' , '静岡県')
            .str.replace('Fukuoka-ken'  , '福岡県')
            .str.replace('Hiroshima-ken', '広島県')
            .str.replace('Hyōgo-ken'    , '兵庫県')
            .str.replace('Niigata-ken'  , '新潟県')
            .str.replace('Miyagi-ken'   , '宮城県')
        )
        .to_csv(f'{input_path}/sample.csv', index=False)
    )


def aggregate():
    df = pd.read_csv(f'{input_path}/sample.csv')

    # 任意の範囲を1日おきに
    start = df['visit_date'].min()
    end   = df['visit_date'].max()
    df_date = pd.DataFrame(
        data=pd.date_range(start, end, freq='D'),
        columns=['visit_date']
    ).set_index('visit_date')

    (
        df
        .groupby(['pref_name', 'air_genre_name', 'visit_date'])
        [['visitors']]
        .sum()
        .merge(df_date, left_index=True, right_index=True, how='right')
        .to_csv(f'{input_path}/aggregate.csv')
    )


if __name__ == '__main__':
    merge_data()
    aggregate()
