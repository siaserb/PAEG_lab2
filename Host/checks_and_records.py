def get_voters_list() -> list:
    with open("voters.txt", 'r') as file:
        return file.read().splitlines()


def get_candidates_list() -> list:
    with open("candidates.txt", 'r') as file:
        return file.read().splitlines()


def check_voter_id(id: int) -> bool:
    with open("oblik.txt", 'r') as file:
        if id in file.read().splitlines():
            return True
        else:
            return False


def messages_format_check(messages) -> bool:
    if isinstance(messages, list) and all(isinstance(item, tuple) for item in messages):
        return True
    else:
        return False


def write_voter_id(id: int) -> None:
    with open("oblik.txt", 'a') as f:
        f.write(str(f'{id}\n'))
    return


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


def add_vote_to_result(voter_id, candidate) -> None:
    with open("results.txt", 'a') as results:
        results.write(f'{(candidate, voter_id)}\n')
