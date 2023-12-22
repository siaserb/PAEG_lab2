import socket
from generation_keys import *


def sign_messages(encoded_messages, d, n):
    signed_messages = []
    for message in encoded_messages:
        signed_bullets = []
        for bullet in message:
            signed_bullet = pow(bullet, d, n)
            signed_bullets.append(signed_bullet)
        signed_messages.append(tuple(signed_bullets))

    return signed_messages


def decode_messages(encoded_messages, d, r, n):
    decoded_messages = []
    for message in encoded_messages:
        decoded_bullets = []
        for bullet in message:
            decoded_bullet = int(pow(bullet, d, n) / r)
            decoded_bullets.append(decoded_bullet)
        decoded_messages.append(tuple(decoded_bullets))
    return decoded_messages


def decode_bullet(bullet, d, n):
    decoded_bullet = pow(bullet, d, n)
    return decoded_bullet


candidates = [1, 2, 3]
voters = ['Voter 1', 'Voter 2', 'Voter 3', 'Voter 4', 'Voter 5']

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 8345))
server_socket.listen(1)

print('Сервер слухає на порті 8345...')

public_key, private_key = generate_keypair()
print(f'Приватний ключ:{private_key}, публічний ключ:{public_key}')

e = public_key[0]
d = private_key[0]
n = private_key[1]

while True:
    client_socket, client_address = server_socket.accept()
    print('З\'єднано з', client_address)

    data = client_socket.recv(1024)
    print('Отримані дані від клієнта:', data.decode('utf-8'))

    client_socket.sendall(str(public_key).encode('utf-8'))

    encoded_messages = eval(client_socket.recv(1024).decode('utf-8'))
    print('Отримані дані від клієнта(зашифровані маскувальним множником та підписані повідомлення):', encoded_messages)

    r = int(client_socket.recv(1024).decode('utf-8'))
    print('Отримані дані від клієнта(маскувальний множник):', r)

    signed_messages = sign_messages(encoded_messages, d, n)

    random_number = random.randint(0, len(encoded_messages) - 1)

    encoded_messages_for_check = encoded_messages[:random_number] + encoded_messages[random_number + 1:]

    decoded_messages = decode_messages(encoded_messages_for_check, d, r, n)
    print('Розшифровані 9 повідомлень для перевірки:', decoded_messages)

    print('Підписане повідомлення ВК:', signed_messages[random_number])
    client_socket.sendall(str(signed_messages[random_number]).encode('utf-8'))

    bullet = int(client_socket.recv(1024).decode('utf-8'))
    print('Отримані дані від клієнта(підписаний бюлетень з голосом):', bullet)

    decoded_bullet = decode_bullet(bullet, d, n)
    print('Розшифрований бюлетень:', decoded_bullet)

    if decoded_bullet not in signed_messages[random_number]:
        print('Надісланий бюлетень не був підписаний ВК!')
        continue
    client_socket.close()
