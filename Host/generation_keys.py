import random
from math import gcd


def generate_keypair():
    # обираємо прості числа p та q
    p = generate_prime_number(100, 1000)
    q = generate_prime_number(100, 1000)

    print(f'Прості множники:p={p}; q={q}')

    # обраховуємо їх добуток n
    n = p * q

    # обраховуємо функцію Ейлера
    phi = (p - 1) * (q - 1)

    # обираємо непарне число e, яке має бути взаємно просте з phi
    e = choose_public_exponent(phi)

    # обираємо число d так, щоб (e * d) % phi = 1
    d = calculate_private_exponent(e, phi)

    # повертаємо пару ключів
    public_key = (e, n)
    private_key = (d, n)

    return public_key, private_key


def generate_prime_number(start, end):
    primes = []
    for possiblePrime in range(start, end + 1):
        isPrime = True
        for num in range(2, int(possiblePrime ** 0.5) + 1):
            if possiblePrime % num == 0:
                isPrime = False
                break
        if isPrime:
            primes.append(possiblePrime)
    return random.choice(primes)


def choose_public_exponent(phi):
    # обираємо непарне число e, яке має бути взаємно просте з phi
    while True:
        e = random.randrange(3, phi - 1, 2)
        if gcd(e, phi) == 1:
            return e


def calculate_private_exponent(e, phi):
    # обираємо число d так, щоб (e * d) % phi = 1
    d = pow(e, -1, phi)
    return d
