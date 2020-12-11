

import numpy as np
import pandas as pd
import pickle
import codecs
#import functions

def open_pickle(path):
    with open(path, 'rb') as handle: 
        doc= pickle.load(handle)
    return doc


#----------------------------------------------------
def getWords(list_words,b_df):
    myobs=[]
    observable_states=b_df.columns#tous les mots du corpus
    for i in range (len(list_words)):
        for j in range (len( observable_states)):
             if(list_words[i]==observable_states[j]):
                 print(observable_states[j])
                 #dict_exist={}
                 myobs.append(j) 
                 #dict[list_words[i]]=j
             #else : #word dosn't exist
                 
                 
                 
    return myobs



def viterbi(pi, a, b,obs):
    
    nStates = np.shape(b)[0]
    T = np.shape(obs)[0]
    
    # init blank path
    path = np.zeros(T).astype(int)
    print("paht",path)
    # delta
    delta = np.zeros((nStates, T))
    # phi --> 
    phi =(np.zeros((nStates, T))).astype(int)
    
    print("obs de 0",obs[0])
    print("phi",phi)
  
    # init delta and phi 
    delta[:, 0] = pi * b[:, obs[0]]
    print("delta",delta)
    phi[:, 0] = 0
    print("phi",phi)
    print("prod" ,0.5*0.6*0.3)
    print('\nStart Walk Forward\n')    
    # the forward algorithm 
    for t in range(1, T):
        for s in range(nStates):
            delta[s, t] = np.max(delta[:, t-1] * a[:, s]) * b[s, obs[t]] 
            phi[s, t] =   np.argmax(delta[:, t-1] * a[:, s])
            print('s={s} and t={t}: delta[{s}, {t}] = {delta}'.format(s=s, t=t, delta=delta[s, t]))
            print('s={s} and t={t}: phi[{s}, {t}] = {phi}'.format(s=s, t=t, phi=phi[s, t]))
    
   
    # find optimal path
    print('-'*50)
    print('Start Backtrace\n')
    x=5.0
    y=int(x)
    print("y=",y)
    path[T-1] = (np.argmax(delta[:, T-1])).astype(int)
    path[T-1]=int(path[T-1])
    print("path[t-1]",path[T-1])
   
    for t in range(T-2, -1, -1):
        path[t] = phi[path[t+1], [t+1]]
       
        print('path[{}] = {}'.format(t, path[t]))

    return path, delta, phi



def words(text):
    mots = []
    for line in text:
        words = line.split()
        if words[0] not in mots:
            mots.append(words[0])
    return mots


def save_pickle(variable,filename):
    path = 'C:/Users/ACER/Desktop/pfe_m2/python/projet guessouum/'
    with open(path+filename, 'wb') as handle :
        pickle.dump(variable, handle, protocol = pickle.HIGHEST_PROTOCOL)


def get_words():
    file = codecs.open('dataset_finale.txt', 'r', 'utf-8')
    text = file.readlines()
    obs_list =words(text)
    save_pickle(obs_list,"words_obs.pickle")
    





def fill_matrices(path_transition, path_observation,list_words):
    # b 
    b_df=open_pickle(path_observation)
    print(b_df)
    b=b_df.values
    print(b)
    #a 
    doc=open_pickle(path_transition)
  
    hidden_states=['O','PREP','B-ORG','I-ORG','B-LOC','MESURE','B-DATE','B-PERS','I-PERS','PRON','CONJ','I-LOC','B-MISC','I-MISC','I-DATE']
    a_df=pd.DataFrame.from_dict(doc)
    print(a_df)
    
    a_df_nv= pd.DataFrame(columns=hidden_states, index=hidden_states)
    a_df_nv.loc[hidden_states[0]]=a_df.loc[hidden_states[0],:]
    a_df_nv.loc[hidden_states[1]]=a_df.loc[hidden_states[1],:]
    a_df_nv.loc[hidden_states[2]]=a_df.loc[hidden_states[2],:]
    a_df_nv.loc[hidden_states[3]]=a_df.loc[hidden_states[3],:]
    a_df_nv.loc[hidden_states[4]]=a_df.loc[hidden_states[4],:]
    a_df_nv.loc[hidden_states[5]]=a_df.loc[hidden_states[5],:]
    a_df_nv.loc[hidden_states[6]]=a_df.loc[hidden_states[6],:]
    a_df_nv.loc[hidden_states[7]]=a_df.loc[hidden_states[7],:]
    a_df_nv.loc[hidden_states[8]]=a_df.loc[hidden_states[8],:]
    a_df_nv.loc[hidden_states[9]]=a_df.loc[hidden_states[9],:]
    a_df_nv.loc[hidden_states[10]]=a_df.loc[hidden_states[10],:]
    a_df_nv.loc[hidden_states[11]]=a_df.loc[hidden_states[11],:]
    a_df_nv.loc[hidden_states[12]]=a_df.loc[hidden_states[12],:]
    a_df_nv.loc[hidden_states[13]]=a_df.loc[hidden_states[13],:]
    a_df_nv.loc[hidden_states[14]]=a_df.loc[hidden_states[14],:]

    a=(a_df_nv.values)
    print(a)
    print(a_df_nv.columns)  
   
   
    # pi
    pi=[0.5,0,0.1,0,0.1,0,0.1,0,0.1,0,0.1,0,0,0,0]
    #array_words
    observable_states=b_df.columns
    print(observable_states)
    myobs=getWords(list_words,b_df)
    print(myobs)
    #reversed_arr=myobs[::-1]
    reversed_arr=myobs
    print("reversed_arr========",reversed_arr)
    path, delta, phi = viterbi(pi, a, b, reversed_arr)
    print('\n best state path: \n', path)
    print('viterbi:\n', delta)
    print('back:\n', phi)
    return reversed_arr,path,delta,phi


#path_transition="C:/Users/ACER/Desktop/pfe_m2/python/projet guessouum/matrice_transition.pickle"
#path_observation="C:/Users/ACER/Desktop/pfe_m2/python/projet guessouum/matrice_obs.pickle"
#list_words=['الولايات','في','بولتون' ,'جون','السيارات','صناعة','اتحاد','رفض']  
#reversed_arr,path,delta,phi=fill_matrices(path_transition,path_observation,list_words)

def show(reversed_arr,path):
    obs_list=open_pickle("C:/Users/ACER/Desktop/pfe_m2/python/projet guessouum/words_obs.pickle") 
    obs_map={}
    for i in range (len(obs_list)):
        obs_map[i]=obs_list[i]
    inv_obs_map=open_pickle("inv_obs_map.pickle")

    obs=reversed_arr

    obs_seq = [inv_obs_map[v] for v in obs]
    print(obs_seq)
  
    
    print(pd.DataFrame(np.column_stack([obs, obs_seq]),    
                columns=['Obs_code', 'Obs_seq']) )  
  
           
    state_map = {0:'O',1:'PREP',2:'B-ORG',3:'I-ORG',4:'B-LOC',5:'MESURE',6:'B-DATE',7:'B-PERS',8:'I-PERS',9:'PRON',10:'CONJ',11:'I-LOC',12:'B-MISC',13:'I-MISC',14:'I-DATE'}
    state_path = [state_map[v] for v in path]
    print("state_path",state_path)
    #print((pd.DataFrame()
    #.assign(Observation=obs_seq)
    #.assign(Best_Path=state_path)))
    
    return obs_seq,state_path
    
#obs_seq,state_path=show(reversed_arr,path)

#s=str(pd.DataFrame(np.column_stack([obs_seq, state_path])))
'''
s=str(pd.DataFrame()
        .assign(Observation=obs_seq)
        .assign(Best_Path=state_path))
print(s)
'''
