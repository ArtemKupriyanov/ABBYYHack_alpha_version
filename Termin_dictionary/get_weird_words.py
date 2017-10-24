import numpy as np
import pandas as pd
import pymorphy2 as pm
import re

def get_meaning(df, word):
    if word in df.index:
        string = df.loc[word]
        string = string.dropna()
        l = len(string)
        name = str(string.name)
        mean = str()
        for i in range(l):
            mean += str(string[i])
        return name, mean
    else: return '',''

def find_law_words(text):
    df = pd.read_csv('../Termin_dictionary/book_data.csv', sep='-()', index_col=0)
    df = df.loc[df.index.dropna()]
    sep_words = re.split('[., ]+', text)
    morph = pm.MorphAnalyzer()
    res = []
    for word in sep_words:
        root = morph.parse(word)[0].normal_form
        root += ' '
        root = root[0].upper()+root[1:]
        #print (root)
        name, mean = get_meaning(df, root)
        if (name!='') and (mean!=''):
            res.append([name, mean])
    return res