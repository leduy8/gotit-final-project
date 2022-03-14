import hashlib
import random
import string


def gen_salt(length=12) -> str:
    alphabet = string.digits + string.ascii_letters
    return "".join(random.choice(alphabet) for _ in range(length))


def generate_password_hash(password: str, salt: str) -> str:
    password_hash = hashlib.sha256()
    try:
        password_hash.update(salt.encode("ascii"))
        password_hash.update(password.encode("ascii"))
    except UnicodeDecodeError as e:
        raise e("Can't hash password.")
    return password_hash.hexdigest()


def check_password_hash(password_hash: str, password: str, salt: str) -> bool:
    return generate_password_hash(password=password, salt=salt) == password_hash
