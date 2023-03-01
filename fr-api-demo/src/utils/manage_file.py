import pandas as pd
import yaml
import datetime
import os

def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


def read_csv(csv_path='assets/data_clean_593_1-1.csv', n=100):

    df = pd.read_csv(csv_path)
    df_positive = df[df['check'] == True]
    df_positive = df_positive.sample(frac=1)
    df_positive = df_positive.iloc[:round(n/2)]

    df_negative = df[df['check'] == False]
    df_negative = df_negative.sample(frac=1)
    df_negative = df_negative.iloc[:round(n/2)]

    df_fin = pd.concat([df_positive, df_negative])
    df_fin = df_fin.reset_index(drop=True)
    # print(df_fin['check'].value_counts())
    # print(df_fin.head(10))

    return df_fin

def read_excel(csv_path='../assets/nist/All.xlsx', n=100):

    df = pd.read_excel(csv_path)

    return df

def save_csv(df, csv_path= './assets/result'):

    create_dir(csv_path)
    date = str(pd.Timestamp.now(tz='Asia/Bangkok')).replace(':','_')
    file_name = os.path.join(csv_path, date + '.csv')

    df.to_csv(file_name,index=False)


def read_config(yaml_path='./src/utils/config.yaml'):
    # file_path = os.path.join(project_path, "dia-face-recognition.yaml")
    with open(yaml_path) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    return config
