import PySimpleGUI as sg
import py7zr as zip
import shutil as sh
import os
from io import StringIO

dir_bkp = 'C:/sys/deploy/04-09-2023/bkp/wts/files/apps'
new_dir = dir_bkp.split('/')
final_dir = StringIO()

def create_dir(novo_diretorio): 
    if novo_diretorio != '':
        dir_split = novo_diretorio.split('/')
        for i in range(1,len(dir_split)):
            final_dir.write('\\'+dir_split[i])
            if i > 0: 
                try:
                    print('\\' + final_dir.getvalue()[1:])
                except FileExistsError:
                    continue
                except FileNotFoundError:
                    sg.popup('Valide o Caminho do Diretório')
                except Exception as inst:
                    sg.popup(type(inst))
    else:
        print('Diretório Vazio')
        return final_dir.getvalue()[1:]
    
def create_dir_c(novo_diretorio): 
    if novo_diretorio != '':
        dir_split = novo_diretorio.split('/')
        for i in range(1,len(dir_split)):
            final_dir.write('\\'+dir_split[i])
            if i > 0: 
                try:
                    print('\\' + final_dir.getvalue()[1:])
                    #os.mkdir('\\' + final_dir.getvalue()[1:])
                except FileExistsError:
                    continue
                except FileNotFoundError:
                    sg.popup('Valide o Caminho do Diretório')
                except Exception as inst:
                    sg.popup(type(inst))
    else:
        print('Diretório Vazio')
        return final_dir.getvalue()[1:]

create_dir_c(dir_bkp)
