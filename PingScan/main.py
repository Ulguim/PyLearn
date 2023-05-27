from datetime import datetime
import subprocess

import pingparsing
import platform
import csv

date = datetime.now().strftime("%d/%m/%Y ")
time = datetime.now().strftime("%H:%M:%S")
parser = pingparsing.PingParsing()
jumps = 4


def detectOS():
    os = platform.system()
    return os

def pingSitesFromFile():
    with open("ips.txt", "r") as sites_file:
        sitesToPing = sites_file.read().splitlines()
    
    with open(f'Results_{time}.csv', 'w', newline='') as file:
        header = ['URL', 'date', 'Status', 'time', 'Perda De Pacotes', 'Tempo']
        writer = csv.writer(file)
        writer.writerow(header)
        try:
            for site in sitesToPing:
                print(f"-------------Pingando: {site}")

                pingTime = datetime.now().strftime("%H:%M:%S")
                pingCommands = ["ping", "-n" if platform.system() == "Windows" else "-c", str(jumps), site]

                pingProcess = subprocess.Popen(pingCommands, stdout=subprocess.PIPE)

                pingOutput = pingProcess.communicate()[0]
                print("".join(map(chr, pingOutput)))
                rttAvg = parser.parse(pingOutput).rtt_avg

                status = "Ativo" if pingProcess.returncode == 0 else "Inativo"
                
                packetLoss = parser.parse(pingOutput).packet_loss_rate
                
                row = [site, date, status, pingTime, f"{packetLoss}%", f"{rttAvg}ms"]
                writer.writerow(row)
        except:
            print("Erro ao pingar sites")
            menu()

    print("-------------Fim")
    menu()


def pingSitesFromUrl():
    url = input("Digite a url: ")

    with open(f'Results{time}.csv', 'w', newline='') as fileUrl:
        header = ['URL', 'date', 'Status', 'time', 'Perda De Pacotes', 'Tempo']
        writer = csv.writer(fileUrl)
        writer.writerow(header)

        print(f"-------------Pingando: {url}")
        try:
            pingProcess = subprocess.Popen(["ping", f"-n {jumps}" if platform.system() == "Windows" else f"-c {jumps}", url], stdout=subprocess.PIPE)
            pingOutput = pingProcess.communicate()[0]

            print("".join(map(chr, pingOutput)))

            status = "Ativo" if pingProcess.returncode == 0 else "Inativo"
            packetLoss = parser.parse(pingOutput).packet_loss_rate
            rttAvg = parser.parse(pingOutput).rtt_avg
            row = [url, date, status, time, f"{packetLoss}%",f"{rttAvg}ms"]
            writer.writerow(row)
            fileUrl.close()
            tryAgain = input("Deseja pingar novamente? (s/n): \n")
            
            if tryAgain == "s":
                pingSitesFromUrl()
            else:
                menu()
        except:
            print("Erro ao pingar site")
            menu()

   
    print("-------------Fim")
    menu()
    
def menu():
    print("1 - Pingar sites a partir de arquivo")
    print("2 - Pingar sites a partir de url")
    print("3 - Sair")
    option = int(input("Digite a opção: "))
    if option == 1:
        pingSitesFromFile()
    elif option == 2:
        pingSitesFromUrl()
    elif option == 3:
        exit()
    else:
        print("Opção inválida")
        menu()

menu()