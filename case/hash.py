import hashlib
import secrets
import random

def calculate_hash(server_seed, client_seed, nonce):
    seed = server_seed + ':' + client_seed + ':' + str(nonce)
    return hashlib.sha512(seed.encode('utf-8')).hexdigest()

def get_server_seed():
    return secrets.token_hex(16)

def generate_client_seed():
    return secrets.token_hex(16)

def get_nonce():
    return random.randint(1, 100000)