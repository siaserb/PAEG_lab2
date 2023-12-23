import socket
from client_functions import *


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8346))

    # Надсилаємо тестове повідомлення до ВК
    message_to_server = 'Привіт, сервачок!'
    client_socket.sendall(message_to_server.encode('utf-8'))

    # Отримуємо список кандидатів від ВК
    candidates = eval(client_socket.recv(1024).decode('utf-8'))
    client_socket.sendall('Кандидатів отримано!'.encode('utf-8'))
    print('Для голосування доступні такі кандидати', candidates)

    # Отримуємо список виборців від ВК
    voters = client_socket.recv(1024).decode('utf-8')
    client_socket.sendall('Список виборців отримано!'.encode('utf-8'))
    print('До голосування допущені наступні виборці:', voters)

    # Відкриваємо файл для запису та читання з виборцями що проголосували
    with open('voted_voters.txt', 'r') as file:
        voted_voters = file.read().splitlines()

        # Виборець вводить своє ім'я та відбувається перевірка
        name = input('Введіть ваше ім\'я:')
        if name not in voters:
            exit('В даного виборця немає права голосу!')
        elif name in voted_voters:
            exit('Даний виборець вже голосував!')

    # Отримуємо публічний ключ ВК
    public_key = eval(client_socket.recv(1024).decode('utf-8'))
    print('Отримані дані від сервера(публічний ключ ВК):', public_key)
    e = public_key[0]
    n = public_key[1]

    # Генеруємо маскувальний множник
    r = generate_coprime(n, 1, 1000)
    print('Маскувальний множник:', r)

    # Генеруємо id виборця
    user_id = get_user_id(n, r)

    # Генеруємо повідомлення
    messages = generate_messages(user_id, candidates, 10)
    print('Згенеровані повідомлення:')
    for message in messages:
        print(message)

    # Перетворюємо бюлетені в кожному повідомленні на єдине число та шифруємо маскувальним множником та підписом
    new_messages, encoded_messages = encode_messages(messages, r, e, n)
    print('Вигляд повідомлень після перетворення:', new_messages)
    print('Зашифровані маскувальним множником та підписані повідомлення:', encoded_messages)
    client_socket.sendall(str(encoded_messages).encode('utf-8'))

    # Надсилаємо ВК маскувальний множник
    client_socket.sendall(str(r).encode('utf-8'))

    # Отримуємо від ВК підписане повідомлення
    signed_message = client_socket.recv(1024)
    signed_message = eval(signed_message.decode('utf-8'))
    print('Отримані дані від сервера(підписане повідомлення ВК):', signed_message)

    # Для перевірки розшифруємо підписане повідомлення від ВК
    decoded_signed_message = decode_signed_message(signed_message, r, n)
    print('Розшифроване повідомлення від ВК:', decoded_signed_message)

    # Процес вибору кандидата виборцем
    bullet = input("Ведіть номер бюлетеню, остання цифра якого, відповідала б номеру кандидата:")
    if int(bullet) in decoded_signed_message:
        num_bullet = decoded_signed_message.index(int(bullet))
    else:
        exit("Введений номер не є вірним!")

    print('Підписаний бюлетень ВК:', signed_message[num_bullet])
    print('Підписаний бюлетень ВК та виборцем:', sign_bullet(signed_message[num_bullet], e, n))
    client_socket.sendall(str(sign_bullet(signed_message[num_bullet], e, n)).encode('utf-8'))

    client_socket.close()

    # Здійснюємо запис виборця до файлу з виборцями, що вже проголосували
    with open('voted_voters.txt', 'a') as file:
        file.write(f"{name}\n")


if __name__ == '__main__':
    main()
