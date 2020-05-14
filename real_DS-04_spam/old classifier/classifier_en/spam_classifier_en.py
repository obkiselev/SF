# -*- coding: utf-8 -*-

import pandas as pd

pA = 0
pNotA = 0

cntA = 0    #кол-во спам-писем
cntNotA = 0

dctA = {}    #словарь для хранения количеств спам-слов
dctNotA = {} #словарь для хранения количеств НЕспам-слов

SPAM = 1
NOT_SPAM = 0

# Заполнение словаря
def fill_dict(p_dict, p_word):
    if p_word not in p_dict.keys():
        p_dict[p_word] = 1
    else:
        p_dict[p_word] += 1

# Вычислить словарь
def get_dict(label):
    if label == SPAM:
        return dctA
    else:
        return dctNotA
    
# Преобразование строки        
def replace_symb(text):
    txt = str(text).replace('!', '')
    txt = txt.replace('?', '')
    txt = txt.replace('.', '')
    txt = txt.replace(',', '')
    txt = txt.replace(':', '')
    txt = txt.replace(';', '')
    txt = txt.replace('"', '')
    return txt.lower()

str_dig = '0123456789'

#Ф-я заполнения словарей
def calculate_word_frequencies(body, label):
    txt = replace_symb(body)
    for word in txt.split():
        if label == SPAM:
            fill_dict(dctA, word)
        elif label == NOT_SPAM:
            fill_dict(dctNotA, word)

#Функция обучения
def train():
    global pA, pNotA
    global dctA, dctNotA
    global cntA, cntNotA

    dctA = {}
    dctNotA = {}
    cntA = 0
    cntNotA = 0

    df = pd.read_csv('data/spam_or_not_spam.csv')
    train_data = df.values.tolist()
    
    for i in range(len(train_data)):
        if train_data[i][1] == SPAM:
            cntA += 1
        else:
            cntNotA += 1
        calculate_word_frequencies(train_data[i][0], train_data[i][1])
    pA = round(cntA / (cntA + cntNotA), 6)
    pNotA = round(1 - pA, 6)
    print('pA =', pA, ', pNotA =', pNotA)


# Проверка слова/части слова в словаре. Возвращает подходящий ключ
def get_key_by_word(p_dict, p_word):
    for key in p_dict.keys():
        if len(p_word) <= 3:
            if p_word in p_dict.keys():
                return key
        else:
            if ((len(p_word) > 3 and p_word in str(key)) | #в точности такое слово или часть слова
            (len(p_word) > 3 and str(p_word)[:-2] == str(key)) |
            (len(p_word) > 1 and str(p_word)[:-1] == str(key)[:-1]) | #один корень, разные окончания
            (len(p_word) > 2 and str(p_word)[:-2] == str(key)[:-2]) | #один корень, разные окончания
            (len(p_word) > 3 and str(p_word)[:-3] == str(key)[:-3]) #один корень, разные окончания
           ): 
                return key
    return None

# Для отдельного слова
def calculate_P_Bi_A(word, label):
    d = get_dict(label)
    key = get_key_by_word(d, word)
    if key == None:
        return 1 / len(d)
    else:
        return (d[key] + 1) / len(d)

# Для всего предложения
def calculate_P_B_A(text, label):
    P = 1
    txt = replace_symb(text)
    for word in txt.split():
        prb = calculate_P_Bi_A(word, label)
        P *= prb
    return P

# Итоговая ф-я
def classify(email):
    global pA, pNotA
    P_B_A_SPAM = calculate_P_B_A(email, SPAM)
    P_B_A_notSPAM = calculate_P_B_A(email, NOT_SPAM)
    if pA * P_B_A_SPAM > pNotA * P_B_A_notSPAM:
        return True
    else:
        return False
