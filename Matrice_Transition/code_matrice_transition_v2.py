# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 18:36:02 2020

@author: user
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 12:38:54 2019

@author: user
"""

import numpy as np
import pandas as pd
import nltk
from nltk import re
from nltk import defaultdict
import io
from nltk import  word_tokenize
from nltk import  sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import codecs
import csv
import pickle

#path="C:\\Users\\user\\Desktop\\M2 SII USTHB\\nlp\\NE project\\code\\"
path="C:\\Users\\ACER\\Desktop\\pfe_m2\\python\\projet guessouum\\"
def open_pickle(filename):
    with open(path+filename, 'rb') as handle: 
        doc= pickle.load(handle)
    return doc

def save_pickle(variable,filename): 
    with open(path+filename, 'wb') as handle:
         pickle.dump(variable, handle, protocol=pickle.HIGHEST_PROTOCOL)


def open_txt(filename):
    filehandle = open(path+filename,encoding='utf8')
    text= filehandle.read()
    filehandle.close()
    return text
    
def text_to_list(text):
    liste=[]
    liste=text.split("\n")
    return liste
    
def lexique(liste):
    lexique=nltk.ConditionalFreqDist()
    for x in liste:
        if(x != ''):
            l=x.split("\t")
            lexique[l[0]][l[1]] += 1
    save_pickle(transition_matrix,"lexique_word_etiq.pickle")
    return lexique
        

def bigram_with_max_prob(liste,lexique_max):
    liste_tuple=[]
    for x in liste:
       if(x != ''):
           l=x.split("\t")
           liste_tuple.append((l[0],l[1]))
    return list(nltk.bigrams(liste_tuple))

def freq_etiquette(lexique): 
    
     freq_etiquette=nltk.FreqDist() 
     
     for w in lexique:
         for etiq in lexique[w]:
             freq_etiquette[etiq] +=1
     return freq_etiquette

        

def count_one_etiq(element,freq_etiquette):
    return freq_etiquette[element]

def count_etiq_suiv_etiq(precedant,suivant,bigram): # combien de fois on a  precedent suivi de suivant
    cpt=0
    for x in range(0,len(bigram)):
        if(bigram[x][0][1] == precedant and bigram[x][1][1] == suivant):
            cpt+=1
    return cpt   
        
def transition_matrix(bigrams,freq_etiquette):
    #M=len(freq_etiquette)
    matrix=nltk.ConditionalFreqDist()
    for precedent in freq_etiquette:
        for suivant in freq_etiquette:
            prob=count_etiq_suiv_etiq(precedent,suivant,bigrams)/count_one_etiq(precedent,freq_etiquette)
            print("P(",suivant,"|",precedent,") = ",prob)
            print(count_etiq_suiv_etiq(precedent,suivant,bigrams),"/",count_one_etiq(precedent,freq_etiquette))
            matrix[precedent][suivant]=prob
            
    return matrix
        


#================================================================== CALL =========================================================
#----------- fonction qui ajoute ce que l'utilisateur a entrer
def update_dataset(word_etiq):
    text=open_txt("dataset_finale.txt")
    #lexique=open_pickle("lexique_word_etiq")
    new_elt=''
    for word in word_etiq:
        new_elt='\n'+word+'\t'+word_etiq 
    final_text=text+new_elt
    
    #save text
    file1 = open(path+"dataset_finale.txt","w")
    file1.writelines(str(final_text)) 
    file1.close()
    
        
#----------- fonction qui calcule maatrice de transitioh 
def matrice_transiton(path):
    dataset_txt=open_txt("dataset_finale.txt")
    liste=text_to_list(dataset_txt)
    lexique=lexique(liste)    
    freq_etiquette=freq_etiquette(lexique) #frequence de chaque etiquette
    bigram=bigram_with_max_prob(liste,lexique)
    transition_matrix=transition_matrix(bigram,freq_etiquette)
    save_pickle(transition_matrix,"matrice_transition.pickle")
    return transition_matrix

    



