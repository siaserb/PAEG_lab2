def check_voter_id(id: int) -> bool:
    with open("oblik.txt", '+a', encoding='utf-8') as file:
        if id in file:
            return True
        else:
            return False


def check_message() -> bool:
    pass


def check_sign() -> bool:
    pass


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
