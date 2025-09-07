#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
================================================================================
NightWave - Dark Message Sender v1.0
Author: KidNapsterOrKidNolifer (Ethical Hacker / CyberSec)
GitHub: https://github.com/KidNapsterOrKidNolifer/NightWave

Descrição:
NightWave é uma ferramenta de aprendizado para automação de envio de mensagens
via Twilio, desenvolvida para fins educativos e testes de cibersegurança ética.
Nunca deve ser utilizada para spam ou assédio.

Funcionalidades:
1. Envio de mensagem única para um número
2. Envio de mensagens para múltiplos números
3. Logging de envios (nightwave.log)
4. Menu interativo com cores e banner hacker

Como usar:
- Execute o script: python3 bomber.py
- Escolha uma opção no menu
- Digite os números de destino (com código do país)
- Digite a mensagem
- Aguarde o envio e confira o log (nightwave.log)

Estrutura do código:
- Banner & UI       -> Funções para exibir logo e interface
- Helpers           -> Funções auxiliares (formatar número, logging)
- Main Sending Logic -> Função de envio via Twilio
- Menu & Main       -> Lógica interativa do usuário
================================================================================
"""

import os
import sys
import random
import string
from time import sleep
from datetime import datetime
from twilio.rest import Client

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    print("Instale colorama: pip install colorama")
    sys.exit(1)

# ------------------- Config Twilio -------------------
ACCOUNT_SID = ""
AUTH_TOKEN = ""
TWILIO_NUMBER = ""
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# ------------------- Cores -------------------
ALL_COLORS = [Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.YELLOW, Fore.BLUE, Fore.RED, Fore.WHITE]
NEON_COLORS = [Fore.GREEN, Fore.CYAN, Fore.MAGENTA]
RESET_ALL = Style.RESET_ALL

# ------------------- Banner & UI -------------------
def clr():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    clr()
    logo = """
███╗   ██╗ ██████╗ ██╗  ██╗    ██╗    ██╗ █████╗ ██╗    ██╗███████╗
████╗  ██║██╔═══██╗██║ ██╔╝    ██║    ██║██╔══██╗██║    ██║██╔════╝
██╔██╗ ██║██║   ██║█████╔╝     ██║ █╗ ██║███████║██║ █╗ ██║█████╗  
██║╚██╗██║██║   ██║██╔═██╗     ██║███╗██║██╔══██║██║███╗██║██╔══╝  
██║ ╚████║╚██████╔╝██║  ██╗    ╚███╔███╔╝██║  ██║╚███╔███╔╝███████╗
╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝     ╚══╝╚══╝ ╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝

"""
    print(random.choice(NEON_COLORS) + logo + RESET_ALL)
    print(Fore.CYAN + "NightWave - Dark Message Sender v1.0\n" + RESET_ALL)

# ------------------- Helpers -------------------
def format_number(num):
    return ''.join([n for n in num if n in string.digits])

def log_message(number, text, status):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("nightwave.log", "a") as f:
        f.write(f"{timestamp} | {number} | {status} | {text}\n")

# ------------------- Main Sending Logic -------------------
def send_message(number, text):
    try:
        message = client.messages.create(
            body=text,
            from_=TWILIO_NUMBER,
            to=number
        )
        print(Fore.GREEN + f"Mensagem enviada para {number}! SID: {message.sid}" + RESET_ALL)
        log_message(number, text, "SUCCESS")
        return True
    except Exception as e:
        print(Fore.RED + f"Erro ao enviar para {number}: {e}" + RESET_ALL)
        log_message(number, text, "FAILED")
        return False

# ------------------- Menu & Main -------------------
def main():
    banner()
    
    print(Fore.MAGENTA + "[1] Enviar Mensagem Única" + RESET_ALL)
    print(Fore.MAGENTA + "[2] Enviar Mensagens para Lista" + RESET_ALL)
    print(Fore.MAGENTA + "[3] Sair" + RESET_ALL)
    
    choice = input(Fore.CYAN + "Escolha uma opção: " + RESET_ALL).strip()
    
    if choice == "3":
        print(Fore.RED + "Saindo..." + RESET_ALL)
        sys.exit()
    
    if choice == "1":
        number = format_number(input(Fore.YELLOW + "Digite o número de destino (com código do país): " + RESET_ALL))
        text = input(Fore.YELLOW + "Digite a mensagem: " + RESET_ALL)
        print(Fore.CYAN + "\nEnviando mensagem...\n" + RESET_ALL)
        send_message(number, text)
    
    elif choice == "2":
        numbers_input = input(Fore.YELLOW + "Digite os números separados por espaço: " + RESET_ALL)
        numbers = [format_number(n) for n in numbers_input.split()]
        text = input(Fore.YELLOW + "Digite a mensagem: " + RESET_ALL)
        print(Fore.CYAN + "\nEnviando mensagens...\n" + RESET_ALL)
        success, failed = 0, 0
        for num in numbers:
            if send_message(num, text):
                success += 1
            else:
                failed += 1
            sleep(0.5)
        print(Fore.MAGENTA + f"\nEnvio concluído! Sucesso: {success}, Falhas: {failed}" + RESET_ALL)
    
    else:
        print(Fore.RED + "Opção inválida!" + RESET_ALL)

    print(Fore.CYAN + "\nNightWave loaded successfully. Stay ethical. 🌌" + RESET_ALL)

# ------------------- Entry Point -------------------
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Operação cancelada pelo usuário." + RESET_ALL)
        sys.exit()

