import socket
from client_functions import *


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8345))

    message_to_server = 'Привіт, сервачок!'
    client_socket.sendall(message_to_server.encode('utf-8'))

    public_key = client_socket.recv(1024)
    public_key = eval(public_key.decode('utf-8'))
    print('Отримані дані від сервера(публічний ключ ВК):', public_key)
    e = public_key[0]
    n = public_key[1]

    # генеруємо маскувальний множник
    r = generate_coprime(n, 1, 1000)
    print('Маскувальний множник:', r)

    # генеруємо id виборця
    user_id = generate_id(n, r)
    candidates = [1, 2, 3, 4]

    # генеруємо повідомлення
    messages = generate_messages(user_id, candidates, 10)
    print('Згенеровані повідомлення:')
    for message in messages:
        print(message)

    # перетворюємо бюлетені в кожному повідомленні на єдине число та шифруємо маскувальним множником та підписом
    new_messages, encoded_messages = encode_messages(messages, r, e, n)
    print('Вигляд повідомлень після перетворення:', new_messages)
    print('Зашифровані маскувальним множником та підписані повідомлення:', encoded_messages)
    client_socket.sendall(str(encoded_messages).encode('utf-8'))

    client_socket.sendall(str(r).encode('utf-8'))

    signed_message = client_socket.recv(1024)
    signed_message = eval(signed_message.decode('utf-8'))
    if signed_message == "Відмова, виявлено шахрая":
        print("Поліція уже виїхала")
        return
    print('Отримані дані від сервера(підписане повідомлення ВК):', signed_message)

    decoded_signed_message = decode_signed_message(signed_message, r, n)
    print('Розшифроване повідомлення від ВК:', decoded_signed_message)

    bullet = input("Ведіть номер бюлетеню, остання цифра якого, відповідала б номеру кандидата:")
    num_bullet = 0
    if int(bullet) in decoded_signed_message:
        num_bullet = decoded_signed_message.index(int(bullet))

    print('Підписаний бюлетень ВК:', signed_message[num_bullet])
    print('Підписаний бюлетень ВК та виборцем:', sign_bullet(signed_message[num_bullet], e, n))
    client_socket.sendall(str(sign_bullet(signed_message[num_bullet], e, n)).encode('utf-8'))

    client_socket.close()


if __name__ == '__main__':
    main()
