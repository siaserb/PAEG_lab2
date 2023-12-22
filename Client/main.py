import socket
import random
from math import gcd


def generate_coprime(n, lower_bound, upper_bound):
    numbers = list(range(lower_bound, upper_bound + 1))
    coprime = random.choice([i for i in numbers if gcd(i, n) == 1])
    return coprime


# функція для генерації id виборця
def generate_id(n, r):
    while True:
        id = random.randint(1, 999)
        if (id * 10 + 9) * r < n:
            return id


# фукнція для генерації заданої кількості повідомлень з бюлетенями від виборця
def generate_messages(user_id, candidates, number_of_messages):
    result_list = []
    for i in range(number_of_messages):
        result_message = []
        for candidate in candidates:
            current_bullet = (user_id, candidate)
            result_message.append(current_bullet)
        result_list.append(tuple(result_message))
    return result_list


# функція для перетворення бюлетенів в єдине число з подальшим маскуванням та підписанням публічним ключем вк
def encode_messages(messages, r, e, n):
    encoded_messages = []
    new_messages = []

    for message in messages:
        new_bullets = []
        encoded_bullets = []

        for bullet in message:
            new_bullet = int(str(bullet[0]) + str(bullet[1]))
            new_bullets.append(new_bullet)

            encoded_bullet = pow(new_bullet * r, e, n)
            encoded_bullets.append(encoded_bullet)

        new_messages.append(tuple(new_bullets))
        encoded_messages.append(tuple(encoded_bullets))

    return new_messages, encoded_messages


def decode_signed_message(signed_message, r, n):
    decoded_signed_message = []
    for bullet in signed_message:
        decoded_signed_bullet = pow(int(bullet / r), 1, n)
        decoded_signed_message.append(decoded_signed_bullet)
    return decoded_signed_message


def sign_bullet(bullet, e, n):
    signed_bullet = pow(bullet, e, n)
    return signed_bullet


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
candidates = [1, 2, 3]

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
