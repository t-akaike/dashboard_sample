#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import yaml
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import util
sns.set()

paths           = util.get_paths()
src_path        = paths['src_path']
input_path      = paths['input_path']
output_csv_path = paths['output_csv_path']
output_fig_path = paths['output_fig_path']


def set_widget(df, column, wtype, display_name=''):
    """
    ウィジェット追加の制御
    """
    query = ''
    if display_name == '':
        display_name = column

    # 選択する値の取得
    _list = df[column].unique().tolist()

    # 任意のウィジェットを配置 & 選択中の値、クエリのテンプレート出力
    selected_val, query_tmpl = select_widget_type(display_name, wtype, _list)

    # クエリ生成
    if selected_val != '':
        query = query_tmpl.format(column, selected_val)
    return selected_val, query


def select_widget_type(display_name, wtype, _list):
    """
    指定したウィジェットの設置、選択中の値とクエリのテンプレの出力
    """
    # TODO: ウィジェットの追加
    if wtype == 'selectbox':
        _list = [''] + _list
        selected_val = st.sidebar.selectbox(display_name, _list)
        query_tmpl = '{} == "{}"'
    elif wtype == 'multiselect':
        selected_val = st.sidebar.multiselect(display_name, _list, default=_list)
        query_tmpl = '{} in ({})'
    return selected_val, query_tmpl


def main():
    # とりあえず、折れ線グラフ作成に特化させる
    value_list = []
    query_list = []

    # 設定読み込み
    with open(f'{src_path}/settings.yaml', 'r') as f:
        settings = yaml.safe_load(f)
    fname     = settings['fname']      # ファイル名
    index_col = settings['index_col']  # プロット時のインデックスのカラム
    col_info  = settings['col_info']   # カラムの情報
    title     = settings['title']      # ダッシュボードのタイトル

    widget_col_list = [col for col in col_info]

    # データ読み込み
    df = pd.read_csv(f'{input_path}/{fname}')
    for column in col_info:
        wtype, display_name = col_info[column]
        selected_val, query = set_widget(df, column, wtype, display_name)  # ウィジェット配置
        value_list.append(selected_val)                                    # 選択中の値保存
        if query != '':
            query_list.append(query)                                       # クエリ生成

    # 表の絞り込み
    if len(query_list) == 0:
        _df = df.copy()
    else:
        _df = df.query(' and '.join(query_list))

    # ダッシュボードのタイトル・表出力
    st.header(title)
    st.write(_df)

    # グラフ
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    if len(widget_col_list) > 0:
        _df = _df.drop(widget_col_list, axis=1)
    _df.groupby(index_col).sum().plot(ax=ax)  # ここを取り換えればいろいろ可視化できるはず
    st.pyplot(fig)

    # 表示中の表・グラフを保存
    if st.sidebar.button('Download'):
        # 選択している値の単数 / 複数チェック
        for i, val in enumerate(value_list):
            if type(val) == str:
                value_list[i] = value_list[i].replace('/', '')
            elif type(val) == list:
                value_list[i] = '_'.join(value_list[i]).replace('/', '')
        selected = '_'.join(value_list)

        _df.to_csv(
            f'{output_csv_path}/{title}_{selected}.csv',
            index=False,
            encoding='sjis'
        )
        fig.savefig(f'{output_fig_path}/{title}_{selected}.png')


if __name__ == '__main__':
    main()
