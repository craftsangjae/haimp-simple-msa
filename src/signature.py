from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from src.auth import load_rsa_key


def load_sig_scheme(key_path:str):
    key = load_rsa_key(key_path)
    return pkcs1_15.new(key)


def sign_data_by_rsa(message:bytes, private_key_path:str) -> bytes:
    """ 서명하기
    :param message:
    :param private_key_path:
    :return:
    """
    digest = SHA256.new(message)
    sig_scheme = load_sig_scheme(private_key_path)
    return sig_scheme.sign(digest)


def verify_data_by_rsa(message: bytes, signature:bytes, public_key_path: str) -> bool:
    """ 검증하기
    """
    digest = SHA256.new(message)
    sig_scheme = load_sig_scheme(public_key_path)

    try:
        sig_scheme.verify(digest, signature)
        return True
    except ValueError:
        return False
