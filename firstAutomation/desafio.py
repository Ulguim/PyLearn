import os
import json
from datetime import datetime
import subprocess
from urllib.request import urlopen  
import random


exitLogo = open("exit.txt", "r")
logo = open("anim.txt", "r")
print(logo.read())

def login():
    with open('passwords.json') as f:
        storedUsers = json.load(f) 

    attempts = 0
    while True and attempts < 3:
        print(logo.read())
        username = str(input('Login: '))
        password = str(input('passsword: '))

        for info in storedUsers:
            if username == info['user'] and password == info['password']:
                print('\n')
                main()
                break

        else:
            attempts += 1
            if attempts == 3:  
                print("Tentativas de login esgotadas. Tente novamente mais tarde.")
                print(exitLogo.read())
                return False
            else:
                print(f"Usuário ou senha incorretos. Tentativa {attempts} de 3.")
              
               
            
def getRandomASCII():
    try:
        num = random.randint(0, 40)
        url = f'http://www.textfiles.com/art/ASCIIPR0N/anime{num:02}.txt'
        response = urlopen(url)
        if response.getcode() == 200:
            data = response.read().decode('utf-8')
            print(data)
          
    except:
            print('Erro ao tentar acessar a API')
         


def main():
    print('Bem vindo ao terminal')
    path = os.getcwd()
    dateAndTime = datetime.now()
    list_dir = os.listdir(path='.')
    list_dir.sort()
    system = os.name 
    user = subprocess.run(["whoami"], capture_output=True, text=True).stdout.replace('\n',"")
    print(f'Data do login: {dateAndTime.date()}')
    print(f'Horário: {str(dateAndTime.strftime("0:%I:%M%p"))}')
    print(f'Diretório atual: {os.getcwd()}')
    print(f'Arquivos: {list_dir}')
    print(f'Total de Arquivos: {len(list_dir)}')
    print(f'Nome do Usuario: {user}')
    print(f'Pasta Atual: {os.path.basename(path)}')
    print(f'Pasta Anterior: {os.path.dirname(path)}')
    if system == 'nt':
        print(f'Unidade do Disco: {path.split(":")[0]}')
    
    while True:
        print('1 - Random ASCII')
        print('2 - Sair')
        option = input('Escolha uma opção: ')
        if option == '1':
            getRandomASCII()
        elif option == '2':
            print('Saindo...')
            exit()
        else:
            print('Opção inválida')

login()
