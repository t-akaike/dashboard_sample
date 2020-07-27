# dashboard_sample
勉強会用サンプル

## 使用データ
- kaggleの「Recruit Restaurant Visitor Forecasting」コンペのデータ
- 予め下記データをダウンロードし、`dashboard_sample/data/input/raw`に配置しておく
    - URL
        - https://www.kaggle.com/c/recruit-restaurant-visitor-forecasting/data
    - file
        - air_store_info.csv.zip
        - air_visit_data.csv.zip

## 実行手順
1. 上記データを該当のパスに配置
2. `dashboard_sample/src/preprocess.py`を実行
3. `streamlit run src/main.py`を実行
