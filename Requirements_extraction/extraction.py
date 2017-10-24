import numpy as np
import pandas as pd

def prepare_words(path):
    words = pd.read_csv(path) 
    return set(words['word'][i] for i in range(len(words)))
    
def key_words_requirements(sentence, key_words):
    words = sentence.split()
    for i in range(len(words)):
        if words[i] in key_words:
            return True
    return False

def is_requirement(sentence, key_words):
    return key_words_requirements(sentence, key_words) # or rnn_requirement(sentence)

def extract_requirements(doc):
    key_words = prepare_words('../Data/common_key_words.csv')
    sentences = doc.split('.')
    return [sentence for sentence in sentences if is_requirement(sentence, key_words)]
