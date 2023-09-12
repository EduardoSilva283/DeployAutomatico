import os 
import PySimpleGUI as sg
import py7zr as zip
import shutil as sh
from io import StringIO
import filecmp as fc

arquivo_deploy = []
caminho_deploy = []
destino = []

def valida_backup(path_deploy_destino,path_bkp_completo,file_deploy):
    destino_completo= path_bkp_completo.replace('/', '\\') + '\\' + file_deploy
    try:
        fc.cmp(path_deploy_destino,destino_completo)
        return True
    except Exception as inst:
        sg.popup(type(inst))
        return False


def exec_backup(file_destino,path_bkp_completo, file_deploy):
    try:
        sh.copy(file_destino,path_bkp_completo)
        #valida_backup(file_destino,path_bkp_completo,file_deploy)
        sg.popup('Backup realizado com sucesso: ' + file_deploy)   
        print('Backup realizado com sucesso: ' + file_deploy)    
    except FileNotFoundError:
        sg.popup('Arquivo não disponivel para Backup: ' + file_destino)
    except Exception as inst:
        vl = sg.popup_yes_no('Backup do Arquivo: ' + file_destino + ' falhou, Deseja continuar mesmo assim?',  title='Deseja continuar?')
        if vl == 'Yes':
            return True
        else:
            return False


def exec_deploy(file_new, path_dest,file_backup):
    try:
        sh.copy(file_new,path_dest)
        sg.popup('Deploy Realizado: ' + file_backup)
        print('Deploy Realizado: ' + file_backup)
    except FileNotFoundError:
        sg.popup('Caminho do arquivo de Deploy não existe: ' + file_new)
    #except Exception as inst:
        #sg.popup(type(inst))

def create_dir(novo_diretorio): 
    if novo_diretorio != '':
        dir_split = novo_diretorio.split('/')
        final_dir = StringIO()
        for i in range(1,len(dir_split)):
            final_dir.write('\\'+dir_split[i])
            if i > 0: 
                try:
                  os.mkdir('\\' + final_dir.getvalue()[1:])
                except FileExistsError:
                    continue
                except FileNotFoundError:
                    sg.popup('Valide o Caminho do Diretório')
                except Exception as inst:
                    sg.popup(type(inst))        
    else:
        print('Diretório Vazio')
    return final_dir.getvalue()[1:]
    

def extrai_arq(diretorio):
    teste = diretorio.split('/')
    qtd = len(teste)-1
    return teste[qtd]

lay_param = [
    #[sg.Image(r'C:\\sys\\teste.png',size=(50,50))],
        [
            sg.Radio('Servidor Principal', 1, key='SERV_P'),
            sg.Radio('Servidor Secundários',1,key='SERV_S'),
            sg.Checkbox(text='Parar o sistema?',key='stop_system',default=True)
        ],
        [
            sg.Text('Backup: '),
            sg.Input(key='-BKP-'),
            sg.FolderBrowse('...',target=(1, 1),initial_folder='c:\\sys\\deploy')             
        ],
        [
            sg.Text('',key='pul')
        ]
    ]
layout = [ 
    [
        sg.T('Arquivo: '),
        sg.Input(key=i),
        sg.FileBrowse('...',target=(i+4, 1),initial_folder='c:\\sys\\deploy'),
        sg.T('Destino: '),
        sg.Input(key=i+100),
        sg.FolderBrowse('...',target=(i+4, 4),initial_folder='c:\\wts\\')
    ] for i in range(0,10)
        ]

lay_button = [
            [sg.Button(key='Deploy',button_text='Executa Deploy')]
            ]
lay_print = [
    [sg.Output(size=(115,5))]
]


window = sg.Window('Deploy Automático',[lay_param,layout,lay_button,lay_print],resizable=True,finalize=True)
if not os.path.exists('c:\\sys\\deploy'):
    pd = sg.popup_yes_no("Pasta C:\\sys\\deploy não encontrada, Deseja Criar?",  title="Pasta Deploy")
    if (pd == 'Yes'):
        create_dir('c:/sys/deploy')

while True:  # Event Loop
    event, values = window.read()

    if event == 'Deploy':
        if values['stop_system']:
            os.system("taskkill -im wts* -f")

        arquivo_deploy.clear()
        caminho_deploy.clear()
        destino.clear()
        for t in range(0,10):
            if (values[t] != '') and  (values[t+100] != ''):
                caminho_deploy.append(values[t])
                arquivo_deploy.append(extrai_arq(values[t]))
                destino.append(values[t+100])

        for arq in range(0,len(arquivo_deploy)):
            
            path_deploy_destino = destino[arq].replace('/', '\\') + '\\' + arquivo_deploy[arq]  #CAMINHO DO DEPLOY COM O NOME DO ARQUIVO (C:\wts\millenium_wms_coletor.dll)
            path_backup = values['-BKP-'].replace('/', '\\')                                    #DIRETÓRIO DO BKP SEM O NOME DO ARQUIVO (C:\sys\deploy\11\bkp)
            path_arquivo_novo = caminho_deploy[arq].replace('/', '\\')                          #CAMINHO DO NOVO ARQUIVO COMPLETO (C:\sys\deploy\11\millenium_wms_coletor.dll)                                    
            path_destino = destino[arq].replace('/', '\\')                                      #CAMINHO DA PASTA DE DESTINO (C:\wts)                                             
            arq_deploy = arquivo_deploy[arq]                                                    #NOME DO ARQUIVO PARA DEPLOY (millenium_wms_coletor.dll)
            path_final_bkp= values['-BKP-'] +'/' + destino[arq][3:]                             #CAMINHO COMPLETO DO BACKUP (C:/sys/deploy/11/bkp/wts)

        
            if valida_backup(path_deploy_destino,path_final_bkp,arq_deploy):
                ch = sg.popup_yes_no('O arquivo ' + path_arquivo_novo + ' esta identico ao arquivo ' + path_deploy_destino + ' Deseja Continuar?',  title='Deseja continuar?')
                if ch == 'Yes':   
                    create_dir(path_final_bkp)
                    if exec_backup(path_deploy_destino,path_final_bkp,arq_deploy):
                        print('Backup: ' + path_deploy_destino + ' | ' + path_final_bkp + '/' +  arq_deploy)
                        exec_deploy(path_arquivo_novo,path_destino,arq_deploy) 
                    else:
                        break
            else:
                create_dir(path_final_bkp)
                exec_backup(path_deploy_destino,path_final_bkp,arq_deploy)
                exec_deploy(path_arquivo_novo,path_destino,arq_deploy)  
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
 