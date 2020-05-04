# Импорт необходимых библиотек
import pandas as pd
import re
import datetime as dt

RANDOM_SEED = 124680

# Загрузка датасета
df = pd.DataFrame()
df = pd.read_csv('../data/main_task.csv')

# Функция отображения вспомогательной информации
def prn_info(p_col):
    global df
    print('    *** value_counts of ['+p_col+']:')
    print(df[p_col].value_counts())
    print('    ***    rows qnty of ['+p_col+']:',df[p_col].value_counts().sum())

# Функция записи колонки с новой фичей в файл
# Для последующего merge используется колонка ID_TA
def write_to_csv(p_col):
    global df
    idxLst = df.index.to_list()
    header = 'ID_TA,'+p_col+'\n'

    ouf = open('new_cols/'+p_col+'.csv', 'w')
    ouf.write(header)
    for idx in idxLst:
        s = str(df['ID_TA'].iloc[idx])+','+str(df[p_col].iloc[idx])+'\n'
        ouf.write(s)
    ouf.close()