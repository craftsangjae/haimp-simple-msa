import pytest

from src.auth import load_rsa_key, load_rsa_cipher


def test_load_rsa_private_key(given_private_pem_file, given_public_pem_file):
    """RSA를 올바르게 불러오기"""
    private_key = load_rsa_key(given_private_pem_file)

    assert hasattr(private_key, 'n')
    assert hasattr(private_key, 'e')
    assert hasattr(private_key, 'd')
    assert hasattr(private_key, 'p')
    assert hasattr(private_key, 'q')


def test_load_rsa_public_key(given_private_pem_file, given_public_pem_file):
    """RSA를 올바르게 불러오기"""
    public_key = load_rsa_key(given_public_pem_file)

    assert hasattr(public_key, 'n')
    assert hasattr(public_key, 'e')
    assert not hasattr(public_key, 'd')
    assert not hasattr(public_key, 'p')
    assert not hasattr(public_key, 'q')


def test_cipher_encrypt_and_decrypt(given_private_pem_file, given_public_pem_file):
    """cipher를 가져와서 암호화 복호화하기"""
    given_private_key_cipher = load_rsa_cipher(given_private_pem_file)
    given_public_key_cipher = load_rsa_cipher(given_public_pem_file)
    given_text = '안녕 강상재'

    cipher_text = given_public_key_cipher.encrypt(given_text.encode('utf-8'))
    output = given_private_key_cipher.decrypt(cipher_text)

    assert output.decode('utf-8') == given_text


def test_try_decrypt_using_public_key_raise_exception(given_public_pem_file):
    given_public_key_cipher = load_rsa_cipher(given_public_pem_file)
    given_text = '안녕 강상재'

    cipher_text = given_public_key_cipher.encrypt(given_text.encode('utf-8'))

    with pytest.raises(TypeError):
        given_public_key_cipher.decrypt(cipher_text)
