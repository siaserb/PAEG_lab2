import socket
from generation_keys import *
from checks_and_records import *


def main():
    # GoTo: rewrite oblik.txt
    candidates = (1, 2, 3, 4)
    voters = ('Voter 1', 'Voter 2', 'Voter 3', 'Voter 4', 'Voter 5')



    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8345))
    server_socket.listen(1)

    print('Сервер слухає на порті 8345...')

    while True:
        print(f'****************************  Початок сесії  ****************************\n')

        public_key, private_key = generate_keypair()
        print(f'Приватний ключ:{private_key}, публічний ключ:{public_key}')

        d = private_key[0]
        n = private_key[1]

        client_socket, client_address = server_socket.accept()
        print(f'''З'єднано з {client_address}''')

        data = client_socket.recv(1024)
        print('Отримані дані від клієнта:', data.decode('utf-8'))

        client_socket.sendall(str(candidates).encode('utf-8'))
        print(client_socket.recv(1024).decode('utf-8'))

        client_socket.sendall(str(voters).encode('utf-8'))
        print(client_socket.recv(1024).decode('utf-8'))

        client_socket.sendall(str(public_key).encode('utf-8'))

        encoded_messages = eval(client_socket.recv(1024).decode('utf-8'))
        print('Отримані дані від клієнта(зашифровані маскувальним множником та підписані повідомлення):\n',
              encoded_messages)

        r = int(client_socket.recv(1024).decode('utf-8'))
        print('Отримані дані від клієнта(маскувальний множник):', r)

        random_number = random.randint(0, len(encoded_messages) - 1)
        signed_messages = sign_messages(encoded_messages, d, n)
        encoded_messages_for_check = encoded_messages[:random_number] + encoded_messages[random_number + 1:]

        # voter_id = encoded_messages_for_check[1][0][:-1]
        # if check_voter_id(voter_id):
        #     client_socket.sendall("Відмова, виявлено шахрая".encode('utf-8'))
        #     continue
        # else:
        decoded_messages = decode_messages(encoded_messages_for_check, d, r, n)
        print('Розшифровані 9 повідомлень для перевірки:', decoded_messages)

        print('Підписане повідомлення ВК:', signed_messages[random_number])
        client_socket.sendall(str(signed_messages[random_number]).encode('utf-8'))

        bullet = int(client_socket.recv(1024).decode('utf-8'))
        print('Отримані дані від клієнта(підписаний бюлетень з голосом):', bullet)

        decoded_bullet = decode_bullet(bullet, d, n)
        print('Розшифрований бюлетень:', decoded_bullet)

        if decoded_bullet not in signed_messages[random_number]:
            print('Надісланий бюлетень не був підписаний ВК!\n')
            continue
        else:
            print(f'************************ Голосування успішне! ************************\n')

        client_socket.close()


if __name__ == '__main__':
    main()
