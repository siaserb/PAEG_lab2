import socket
from generation_keys import *
from checks_and_records import *

# Binary codes for change texts colors in console
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'


def main():
    port = 8346
    candidates = get_candidates_list()
    voters = get_voters_list()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', port))
    server_socket.listen(1)
    print(f'*** Сервер слухає на порті {port} ***\n')

    while True:

        print(f'****************************  Початок сесії  ****************************')

        # Keys generation
        public_key, private_key = generate_keypair()
        d = private_key[0]
        n = private_key[1]
        e = public_key[0]
        print(f'Приватний ключ:{private_key}, публічний ключ:{public_key}')

        # Wait for client
        client_socket, client_address = server_socket.accept()
        print(f'''З'єднано з {client_address}''')

        # Collect data from client
        data1 = client_socket.recv(1024).decode("utf-8")
        print(f'Отримані дані від клієнта: {data1}')

        # Send list of candidates
        client_socket.sendall(str(candidates).encode('utf-8'))

        # Collect data from client
        data2 = client_socket.recv(1024).decode('utf-8')
        print(data2)

        # Send list of voters
        client_socket.sendall(str(voters).encode('utf-8'))

        # Collect data from client
        data3 = client_socket.recv(1024).decode('utf-8')
        print(data3)

        # Send public key
        client_socket.sendall(str(public_key).encode('utf-8'))

        # Collect messages from client
        encoded_messages = eval(client_socket.recv(1024).decode('utf-8'))
        print(f'Дані клієнта(зашифровані маскувальним множником підписані повідомлення):\n{encoded_messages}')

        # Collect masking factor from client
        masking_factor = int(client_socket.recv(1024).decode('utf-8'))
        print(f'Маскувальний множник клієнта: {masking_factor}')

        random_number = random.randint(0, len(encoded_messages) - 1)
        signed_messages = sign_messages(encoded_messages, d, n)
        encoded_messages_for_check = encoded_messages[:random_number] + encoded_messages[random_number + 1:]

        if not messages_format_check(encoded_messages_for_check):
            raise Exception(f'{RED}Надіслані бюлетені не відповідають формату!{RESET}\n')

        # Decode 9 messages
        decoded_messages = decode_messages(encoded_messages_for_check, d, masking_factor, n)
        bulletin_for_vote = signed_messages[random_number]
        print(f'Розшифровані 9 повідомлень для перевірки: {decoded_messages}')
        print(f'Підписане ВК повідомлення: {bulletin_for_vote}')

        # Check voter by id
        voter_id = decoded_messages[0][0] // 10
        if check_voter_id(voter_id):
            raise Exception(f'{RED}Даний виборець вже надсилав повідомлення на підпис!{RESET}')
        else:
            write_voter_id(voter_id)

        # Send signed message
        signed_bulletin = str(signed_messages[random_number])
        client_socket.sendall(signed_bulletin.encode('utf-8'))

        # Collect final bulletin from voter
        bullet = int(client_socket.recv(1024).decode('utf-8'))
        decoded_bulletin = decode_bullet(bullet, d, n)
        print(f'Отримані дані від клієнта(підписаний бюлетень з голосом): {GREEN}{bullet}{RESET}')
        print(f'Розшифрований бюлетень до стану підписаного комісією: {GREEN}{decoded_bulletin}{RESET}')

        # Calculation of the result
        candidate = bulletin_for_vote.index(decoded_bulletin) + 1
        add_vote_to_result(voter_id, candidate)

        if decoded_bulletin not in signed_messages[random_number]:
            raise Exception(f'{RED}Надісланий бюлетень не був підписаний ВК!{RESET}\n')

        unsigned_bullet = unsign_bullet(decoded_bulletin, e, n, d, masking_factor)
        print('Розшифрований бюлетень до початкового стану:', unsigned_bullet)

        voter_id_1 = unsigned_bullet // 10
        if not check_voter_id(voter_id_1):
            raise Exception(f'{RED}Виборця нема у обліку!{RESET}')

        print(count_votes('results.txt', candidates))

        print(f'{GREEN}************************ Голосування успішне! ************************{RESET}\n')

        client_socket.close()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'{RED}Некоректні вхідні дані, exception: {e}{RESET}\n')
