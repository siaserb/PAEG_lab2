def get_voters_list() -> list:
    with open("voters.txt", 'r') as file:
        return file.read().splitlines()


def get_candidates_list() -> list:
    with open("candidates.txt", 'r') as file:
        return file.read().splitlines()


def check_voter_id(id: int) -> bool:
    with open("oblik.txt", 'r') as file:
        return id in map(int, file.read().splitlines())



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


def unsign_bullet(signed_bullet, e, n, d, r):

    unsigned_bullet = pow(signed_bullet, e, n)
    unsigned_bullet_again = int(pow(unsigned_bullet, d, n) / r)
    return unsigned_bullet_again


def parse_line(line):

    parts = line.strip('()\n').split(', ')
    numbers = [int(part) for part in parts]
    return numbers

def count_votes(filename, candidates):

    vote_counts = {int(candidate): 0 for candidate in candidates}

    with open(filename, 'r') as file:
        for line in file:
            candidate, vote = parse_line(line)
            if candidate in vote_counts:
                vote_counts[candidate] += 1

    vote_counts_tuple = tuple(vote_counts.items())
    return vote_counts_tuple