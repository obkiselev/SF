import pandas as pd
import re

pA = 0    #P of SPAM
pNotA = 0 

cntA = 0    #qnt of SPAM letters
cntNotA = 0

dctA = {}
dctNotA = {}

SPAM = 1
NOT_SPAM = 0

# string transforming
def replace_symb(text):
    txt = str(text).lower()
    txt = re.sub('\.+|\,+|\_+|\!+|\?+|\;+|\:+\"+', ' ', txt)
    txt = re.sub('[^0-9a-z ]', '', txt) #only digits, symbols, spaces
    return txt

# fill one dictionary
def fill_dict(p_dict, p_word):
    if p_word not in p_dict.keys():
        p_dict[p_word] = 1
    else:
        p_dict[p_word] += 1
        
# fill dictionaries
def calculate_word_frequencies(body, label):
    txt = replace_symb(body)
    word_old = None
    for word in txt.split():
        if word_old == word: #������� ������� ����
            continue
        word_old = word
            
        if label == SPAM:
            fill_dict(dctA, word)
        elif label == NOT_SPAM:
            fill_dict(dctNotA, word)

#train
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
    pA    = cntA / (cntA+cntNotA)
    pNotA = 1 - pA
#     print('SPAM dict:\n', dctA)
#     print('NOT_SPAM dict:\n', dctNotA)
    print('cntA    =', cntA, ', pA =', pA, ', len_A =', len(dctA))
    print('cntNotA =', cntNotA, ', pNotA =', pNotA, ', len_NotA =', len(dctNotA))

# get dictionary
def get_dict(label):
    if label == SPAM:
        return dctA
    else:
        return dctNotA
    
# one word
def calculate_P_Bi_A(word, label):
    d = get_dict(label)
    N = len(d)
    qnt = d.get(word, 1)
#     print(label, ': word =', word, ', qnt =', qnt, ', N = ', N)
    p = qnt / N
    if p > 1: return 1 #��������� ���� ��� ����, ��� p > 1
    return p

# whole sentence
def calculate_P_B_A(text, label):
    P = 1
    txt = replace_symb(text)
    for word in txt.split():
        prb = calculate_P_Bi_A(word, label)
        P *= prb
#         print(label,': word =', word, ', prb =', round(prb,6), ', P =', P)
    return P

# classify
def classify(email):
    global pA, pNotA
    P_B_A_SPAM = calculate_P_B_A(email, SPAM)
    P_B_A_notSPAM = calculate_P_B_A(email, NOT_SPAM)
    print('len(dctA)    =',len(dctA),', pA    =',pA,', P_B_A_SPAM =',P_B_A_SPAM,', P_SPAM =',pA * P_B_A_SPAM)
    print('len(dctNotA) =',len(dctNotA),', pNotA =',pNotA,', P_B_A_notSPAM =',P_B_A_notSPAM,', P_notSPAM =',pNotA * P_B_A_notSPAM)
    if pA * P_B_A_SPAM > pNotA * P_B_A_notSPAM:
        return True
    else:
        return False
