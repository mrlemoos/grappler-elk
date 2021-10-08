# -*- coding: utf-8 -*-

import random
import subprocess
import sys
import os

import static_arr


def possui_elk_pass():
    res = subprocess.call(
        'cat ./.env | grep "ELK_PASSWORD"', shell=True, stdout=subprocess.DEVNULL)
    # res igual a
    # 0 = existe,
    # 1 = não existe
    return res == 0


def escolher_cada():
    random_upper = random.choice(static_arr.upper)
    random_lower = random.choice(static_arr.lower)
    random_num = random.choice(static_arr.num)

    return random_upper, random_lower, random_num


def gravar_senha(senha: str):
    command_palette = [
        '( echo "' + senha + '" > ./python/cache/senha.backup.txt )',
        '( echo "ELK_PASSWORD=\'' + senha + '\'" >> .env )',
    ]

    for command in command_palette:
        subprocess.call(command, shell=True, stdout=subprocess.DEVNULL)


def apagar_senha():
    subprocess.call('echo $(sed /^ELK_PASSWORD/d .env) > .env', shell=True)

    if os.path.isfile('./python/cache/senha.backup.txt'):
        subprocess.call('rm ./python/cache/senha.backup.txt', shell=True)


def gerar_senha():
    str_length = int(input('> máximo de caracteres da senha '))

    if str_length == 0:
        str_length = 16
        # lembrar de subtrair 3 depois senão gera sempre o str_length + 3

    upper, lower, num = escolher_cada()

    base_senha = upper + lower + num

    for _ in range(str_length - 3):
        base_senha += random.choice(static_arr.combine_characters())
        base_senha_arr = list(base_senha)
        # faz os caracteres se embaralharem entre si
        random.shuffle(base_senha_arr)
        base_senha = ''.join(base_senha_arr)

    senha = ''.join(base_senha)
    gravar_senha(senha)


def exec():
    if possui_elk_pass():
        print('Já existe um "ELK_PASSWORD" dentre as variáveis de ambiente. ')
        sobrescrever = input('Deseja sobrescrevê-la? ').lower()

        if ['sim', 's'].count(sobrescrever) > 0:
            apagar_senha()
            gerar_senha()
        elif ['nao', 'não', 'n'].count(sobrescrever) > 0:
            print('Mantendo senha declarada em "ELK_PASSWORD"')
            sys.exit(0)
        else:
            print('Opção inválida')
            sys.exit(1)
    else:
        gerar_senha()


if __name__ == '__main__':
    exec()
