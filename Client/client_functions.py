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


# функція для генерації заданої кількості повідомлень з бюлетенями від виборця
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
