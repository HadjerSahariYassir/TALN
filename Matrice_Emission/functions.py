# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 18:36:27 2020

@author: asus
"""
import numpy as np
from hmmlearn import hmm
import nltk
from nltk import re
from nltk import defaultdict
import io
from nltk import  word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import codecs
import random 
import pandas as pd
import pickle


def count_e(etiq, text):
    se = 0
    for line in text:
        words = line.split()
        if words[1] == etiq:
                se = se + 1
    return se

def all_count_e(text):
    etiq_count = []
    for i in range(0, len(etiquettes)):
        etiq_count.append(count_e(etiquettes[i], text))
    return etiq_count

def all_count_m_e(text):
    count_m_e = nltk.FreqDist()
    for i in range(0,len(etiquettes)):
        count_m_e[etiquettes[i]] = nltk.FreqDist()
    for line in text:
        words = line.split()
        count_m_e[words[1]][words[0]] += 1
    return count_m_e
        
def etiq(text):
    etiquettes = []
    for line in text:
        words = line.split()
        if words[1] not in etiquettes:
                etiquettes.append(words[1])
    return etiquettes

def words(text):
    mots = []
    for line in text:
        words = line.split()
        if words[0] not in mots:
            mots.append(words[0])
    return mots

def proba_init() :
    init = []
    rest = 1
    for i in range(1,len(etiquettes)):
        rand = random.uniform(0, rest)
        rest = rest - rand
        init.append(rand)
    init.append(rest)
    return init 

def save_pickle(variable,filename):
    path = 'G:/Spyder workspace/Projet TALN/'
    with open(path+filename, 'wb') as handle :
        pickle.dump(variable, handle, protocol = pickle.HIGHEST_PROTOCOL)

def matrice_emission(text):  
   
    init = proba_init()
    state_space = pd.Series(init, index=etiquettes, name='Etiquettes')  
    observable_states = mots
    b_df = pd.DataFrame(columns=observable_states, index=etiquettes)
       
    count_etiq = all_count_e(text)
    count = all_count_m_e(text)
    
    for i in range(0, len(etiquettes)):
        for j in range(0, len(observable_states)): 
            b_df.loc[etiquettes[i]][observable_states[j]] = count[etiquettes[i]][mots[j]] / count_etiq[i]
    filename = 'matrice_obs.pickle' 
    save_pickle(b_df,filename)
etiquettes = []
mots = []
etiquettes = etiq(text)
mots =words(text) 
"""
def freq(etiq, count):
    s = 0
    for i in range(0,len(mots)):
        s = s + count[etiq][mots[i]]
    return s
f = freq(etiquettes[0],count)
"""
        
    