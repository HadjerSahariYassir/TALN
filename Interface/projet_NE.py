from PyQt5.uic import loadUi
import sys
import math
import pickle
from PyQt5 import  QtWidgets,QtCore
import nltk
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
import re 

import finale2
from finale2 import *

import code_matrice_transition_v2
from  code_matrice_transition_v2 import *

import code_2
from code_2 import *

import functions
from functions import *


class projet_NE(QtWidgets.QMainWindow):

    def __init__(self):
        super(projet_NE,self).__init__()
        loadUi("projet_NE.ui",self)
        self.path="C:\\Users\\ACER\\Desktop\\pfe_m2\\python\\projet guessouum\\"
        self.list_words=""
        self.open_file_btn.clicked.connect(self.openFile)
        self.show_Button.clicked.connect(self.show_results)
        self.modify_btn.clicked.connect(self.update_dataset)
        self.retrain_btn.clicked.connect(self.retrain)
        
    def load_index_file_INV(self):
        with open(self.path,'rb') as file_index: 
            dic=pickle.load(file_index)
        return(dic)
        
    def save_pickle(variable,filename):
        path = "C:\\Users\\ACER\\Desktop\\pfe_m2\\python\\projet guessouum\\"
        with open(path+filename, 'wb') as handle :
            pickle.dump(variable, handle, protocol = pickle.HIGHEST_PROTOCOL)
        
    def openFile(self):   
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        print("filename",fileName)
        #f=open(fileName,'r')
        #data=f.read()
        #print(data)
        #list_words=['الولايات','في','بولتون' ,'جون','السيارات','صناعة','اتحاد','رفض']
        #words='الولايات في بولتون جون السيارات صناعة اتحاد رفض'
        #filename="input.txt"
        text=open_txt(fileName)
        self.plainTextEdit_input.setPlainText(text)
        # preprocessing
        self.list_words=preprocess("input.txt")
        print(input)
         
    def openFileDialogue(MainWindow):
        #self.filename = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select folder');
        filename=QFileDialog.getOpenFileName(self,'Open File','/home')
        if self.filename[0]:
            f=open(self.filename[0],'r')
            with f:
                data= f.read()
                self.ui.textEdit.setText(data)
         
    def show_results(self):
        path_transition="C:/Users/ACER/Desktop/pfe_m2/python/projet guessouum/matrice_transition.pickle"
        path_observation="C:/Users/ACER/Desktop/pfe_m2/python/projet guessouum/matrice_obs.pickle"
        #list_words=['الولايات','في','بولتون' ,'جون','السيارات','صناعة','اتحاد','رفض']  
        reversed_arr,path,delta,phi=fill_matrices(path_transition,path_observation,self.list_words)
        #self.textEdit_output
        obs_seq,state_path=show(reversed_arr,path)
        
        #print((pd.DataFrame()
        #.assign(Observation=obs_seq)
        #.assign(Best_Path=state_path)))  
        
        s=str(pd.DataFrame()
        .assign(Observation=obs_seq)
        .assign(Best_Path=state_path))
        
        print(s)
        self.textEdit_output.setText(s)
        
        
        filename="C:/Users/ACER/Desktop/pfe_m2/python/projet guessouum/output1.txt"
        with codecs.open(filename,"w","utf-8") as f1:
            f1.write(s)
        
        mytext = self.textEdit_output.toPlainText()
        lines=mytext.split("\n")
        new_elt=''
        for i in range(1,len(lines)) :
             line=lines[i]
             list=re.split(r'\s+',line)
         #recuperrer à partir de l'interface le resultat
             word=list[1]
             word_etiq=list[2]
             if(word != ''):
                 new_elt=new_elt+word+'\t'+word_etiq+"\n"
                 print("new_elmt"+new_elt)
                 
        filename="C:/Users/ACER/Desktop/pfe_m2/python/projet guessouum/output.txt"
        with codecs.open(filename,"w","utf-8") as f1:
            f1.write(new_elt)
            
        '''
        output = pd.DataFrame(columns=obs_seq, index=state_path)
        save_pickle(pd.dataFrame,filename)
        dataFrame_result=open_pickle("C:/Users/ACER/Desktop/pfe_m2/python/projet guessouum/output.pickle") 
        print("hhh")
        print(dataFrame_result)
        ''' 
    def update_dataset(self):
         text=open_txt("dataset_finale.txt")       
         mytext = self.textEdit_output.toPlainText()
         print(mytext)
         lines=mytext.split("\n")
         new_elt=''
         for i in range(1,len(lines)) :
             print("voila")
             print(lines[i])
             line=lines[i]
             list=re.split(r'\s+',line)
             print(list)
         #recuperrer à partir de l'interface le resultat
             word=list[1]
             word_etiq=list[2]
             
             if(word != ''):
                 new_elt=new_elt+"\n"+word+'\t'+word_etiq
                 print("new_elmt"+new_elt)
             
         final_text=text+new_elt 
        
        #save text
         file1 = open(path+"dataset_finale.txt","a+",encoding="utf-8")
         file1.writelines(str(final_text))
         #file1.writelines(str(final_text)) 
         file1.close()
         
    def retrain(self) :
        #calculate new matrix 
        file = codecs.open(self.path+"dataset_finale.txt", 'r', 'utf-8')
        text = file.readlines()
        matrice_emission(text)
        matrice_transiton(self.path)
        
        

app = QtWidgets.QApplication(sys.argv)  
wind=projet_NE()      
wind.show()
sys.exit(app.exec_())
