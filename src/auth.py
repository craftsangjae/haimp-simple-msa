from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher.PKCS1_OAEP import PKCS1OAEP_Cipher


def load_pem(fpath: str) -> bytes:
    with open(fpath, 'rb') as f:
        return f.read()


def load_rsa_key(fpath: str) -> RSA.RsaKey:
    """rsa key 불러오기"""
    pem_file = load_pem(fpath)
    return RSA.import_key(pem_file)


def load_rsa_cipher(fpath: str) -> PKCS1OAEP_Cipher:
    """키 정보 불러오기"""
    key = load_rsa_key(fpath)
    return PKCS1_OAEP.new(key)

