import PySimpleGUI as sg
import py7zr as zip
import shutil as sh
import os
from io import StringIO


#def extrai_arq(diretorio):
#    teste = diretorio.split('\\')
#    qtd = len(teste)-1
#    return teste[qtd]

#origem =  'C:\wts\millenium_wms_coletor.dll' 
#destino =  'C:\\sys\\deploy\\04-09-2023\\bkp_9'
# copy C:\sys\deploy\04-09-2023\millenium_wms_coletor.dll C:\wts /y


#origem = 'c:\sys\GPReport.html'
#dest = 'c:\wts'


dir_bkp = 'C:/sys/deploy/05-09-2023/bkp/wts/files/web-apps'
new_dir = dir_bkp.split('/')
final_dir = StringIO()

for i in range(1,len(new_dir)):
    final_dir.write('\\'+new_dir[i])
    if i > 0: 
        try:
            os.mkdir(final_dir.getvalue()[1:])
        except FileExistsError:
            continue
        except FileNotFoundError:
            sg.popup('Valide o Caminho do Diretório')
        except Exception as inst:
            sg.popup(type(inst))







