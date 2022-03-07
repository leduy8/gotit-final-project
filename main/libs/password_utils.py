import random
import hashlib
import string


def gen_salt(length=12) -> str:
    ALPHABET = string.digits + string.ascii_letters
    return ''.join(random.choice(ALPHABET) for _ in range(length))


def generate_password_hash(password: str, salt: str) -> str:
    password_hash = hashlib.sha256()
    try:
        password_hash.update(salt.encode('ascii'))
        password_hash.update(password.encode('ascii'))
    except UnicodeDecodeError:
        raise ValueError
    return password_hash.hexdigest()


def check_password_hash(password_hash: str, password: str, salt: str) -> bool:
    password_to_hash = generate_password_hash(password=password, salt=salt)
    return password_to_hash == password_hash
