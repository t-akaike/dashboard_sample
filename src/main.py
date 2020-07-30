#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import streamlit as st
import util

output_path = util.get_paths()['output_path']
df_org = pd.read_csv(f'{output_path}/sample.csv')

def main():
    st.header('店舗への訪問者数')
    st.text('''
    以下サイトから取得したデータを加工し、可視化
    https://www.kaggle.com/c/recruit-restaurant-visitor-forecasting#description
    ''')

    # セレクトボックス作成
    pref_list  = [''] + df_org['pref_name'].unique().tolist()
    genre_list = df_org['air_genre_name'].unique().tolist()
    pref  = st.sidebar.selectbox('都道府県', pref_list)
    genre = st.sidebar.multiselect('ジャンル', genre_list, default=genre_list)

    # クエリ整形
    if pref == '' and genre == '':
        df = df_org.copy()
    else:
        query_list = []
        if pref != '':
            query_list.append(f'pref_name == "{pref}"')
        if genre != '':
            query_list.append(f'air_genre_name in ({genre})')
        df = df_org.query(' and '.join(query_list))

    # 任意の範囲を1日おきに
    df_date = pd.DataFrame(
        data=pd.date_range('2016-01-01', '2017-04-22', freq='D'),
        columns=['visit_date']
    ).set_index('visit_date')

    # 可視化
    st.line_chart(
        df
        .groupby('visit_date')
        [['visitors']]
        .sum()
        .merge(df_date, left_index=True, right_index=True, how='right')
    )
    st.map(
        df
        [['air_store_id', 'latitude', 'longitude']]
        .drop_duplicates()
        .drop('air_store_id', axis=1)
    )

    # TODO: 表示中のグラフを保存するボタンを配置し、クリックすると指定済みのディレクトリに保存されるようにする



if __name__ == '__main__':
    main()
