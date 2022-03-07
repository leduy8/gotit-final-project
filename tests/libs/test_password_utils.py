from main.libs.password_utils import gen_salt, generate_password_hash, check_password_hash


def test_gen_salt():
    salt_len_12 = gen_salt()
    salt_len_custom = gen_salt(length=16)
    assert type(salt_len_12) == str
    assert type(salt_len_custom) == str
    assert len(salt_len_12) == 12
    assert len(salt_len_custom) == 16


def test_generate_password_hash():
    password = 'duy123'
    salt = gen_salt()
    password_hash = generate_password_hash(password=password, salt=salt)
    assert type(password_hash) == str
    assert len(password_hash) == 64


def test_success_check_password_hash():
    salt = gen_salt()
    password = 'duy123'
    password_hash = generate_password_hash(password=password, salt=salt)
    assert check_password_hash(password_hash=password_hash,
                               password=password, salt=salt) is True


def test_fail_check_password_hash_wrong_salt():
    salt = '123456123456'
    wrong_salt = 'lmaolmaolmao'
    password = 'duy123'
    password_hash = generate_password_hash(password=password, salt=salt)
    assert check_password_hash(password_hash=password_hash,
                               password=password, salt=wrong_salt) is False


def test_fail_check_password_hash_wrong_password():
    salt = gen_salt()
    password = 'duy123'
    wrong_password = 'duy321'
    password_hash = generate_password_hash(password=password, salt=salt)
    assert check_password_hash(password_hash=password_hash,
                               password=wrong_password, salt=salt) is False
