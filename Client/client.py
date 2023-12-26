import socket
from client_functions import *

# Binary codes for change texts colors in console
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8346))

    # Sending test message to vk
    message_to_server = 'Привіт, сервачок!'
    client_socket.sendall(message_to_server.encode('utf-8'))

    # Getting list of candidates
    candidates = eval(client_socket.recv(1024).decode('utf-8'))
    client_socket.sendall('Кандидатів отримано!'.encode('utf-8'))
    print('Для голосування доступні такі кандидати', candidates)

    # Getting list of voters
    voters = client_socket.recv(1024).decode('utf-8')
    client_socket.sendall('Список виборців отримано!'.encode('utf-8'))
    print('До голосування допущені наступні виборці:', voters)

    # Opening file for writing and reading with the voters who voted
    with open('voted_voters.txt', 'r') as file:
        voted_voters = file.read().splitlines()

        # The voter enters his name
        name = input('Введіть ваше ім\'я:')
        if name not in voters:
            raise Exception(f'{RED}В даного виборця немає права голосу!{RESET}\n')
        elif name in voted_voters:
            raise Exception(f'{RED}Даний виборець вже голосував!{RESET}\n')

    # Getting public key from vk
    public_key = eval(client_socket.recv(1024).decode('utf-8'))
    print('Отримані дані від сервера(публічний ключ ВК):', public_key)
    e = public_key[0]
    n = public_key[1]

    # Generating r
    r = generate_coprime(n, 1, 1000)
    print('Маскувальний множник:', r)

    # Generating ID
    user_id = get_user_id(n, r)

    # Generating message
    messages = generate_messages(user_id, candidates, 10)
    print('Згенеровані повідомлення:')
    for message in messages:
        print(message)

    # Converting ballots in each message into a single number and encrypt with a masking multiplier and a signature
    new_messages, encoded_messages = encode_messages(messages, r, e, n)
    print('Вигляд повідомлень після перетворення:', new_messages)
    print('Зашифровані маскувальним множником та підписані повідомлення:', encoded_messages)
    client_socket.sendall(str(encoded_messages).encode('utf-8'))

    # Sending vk masking multiplier
    client_socket.sendall(str(r).encode('utf-8'))

    # Getting signed message
    signed_message = client_socket.recv(1024)
    signed_message = eval(signed_message.decode('utf-8'))
    print('Отримані дані від сервера(підписане повідомлення ВК):', signed_message)

    # Decoding message for check
    decoded_signed_message = decode_signed_message(signed_message, r, n)
    print('Розшифроване повідомлення від ВК:', decoded_signed_message)

    # Proces of voting
    bullet = input("Ведіть номер бюлетеню, остання цифра якого, відповідала б номеру кандидата:")
    if int(bullet) in decoded_signed_message:
        num_bullet = decoded_signed_message.index(int(bullet))
    else:
        raise Exception(f'{RED}Введений номер не є вірним!{RESET}\n')

    print('Підписаний бюлетень ВК:', signed_message[num_bullet])
    print('Підписаний бюлетень ВК та виборцем:', sign_bullet(signed_message[num_bullet], e, n))
    client_socket.sendall(str(sign_bullet(signed_message[num_bullet], e, n)).encode('utf-8'))

    client_socket.close()

    # Recording voter to voted_voters
    with open('voted_voters.txt', 'a') as file:
        file.write(f"{name}\n")


if __name__ == '__main__':
    main()
