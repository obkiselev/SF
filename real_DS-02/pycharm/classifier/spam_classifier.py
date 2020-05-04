# -*- coding: utf-8 -*-

pA = 0    #вероятность встретить спам
pNotA = 0 #вероятность НЕ встретить спам

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

    train_data = [  
        ['Купите новое чистящее средство', SPAM],   
        ['Купи мою новую книгу', SPAM],  
        ['Подари себе новый телефон', SPAM],
        ['Добро пожаловать и купите новый телевизор', SPAM],
        ['Довезем до аэропорта из пригорода всего за 399 рублей', SPAM], 
        ['Порадуй своего питомца новым костюмом', SPAM],
        ['Привет давно не виделись', NOT_SPAM], 
        ['Добро пожаловать в Мой Круг', NOT_SPAM],  
        ['Я все еще жду документы для проверки', NOT_SPAM],  
        ['Приглашаем на конференцию Data Science в вашем городе', NOT_SPAM],
        ['Потерял твой телефон напомни его номер', NOT_SPAM]
    ]    
    
    for i in range(len(train_data)):
        if train_data[i][1] == SPAM:
            cntA += 1
        else:
            cntNotA += 1
        calculate_word_frequencies(train_data[i][0], train_data[i][1])
    pA = round(cntA / (cntA + cntNotA), 6)
    pNotA = round(1 - pA, 6)
    print('pA = ',pA)
    print('dctA = ',dctA)


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
        return 'SPAM'
    else:
        return 'NOT_SPAM'
