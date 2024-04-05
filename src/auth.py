from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher.PKCS1_OAEP import PKCS1OAEP_Cipher


def load_rsa_key(fpath: str) -> RSA.RsaKey:
    """rsa key 불러오기"""
    with open(fpath, 'rb') as f:
        return RSA.import_key(f.read())


def load_rsa_cipher(fpath: str) -> PKCS1OAEP_Cipher:
    """키 정보 불러오기"""
    key = load_rsa_key(fpath)
    return PKCS1_OAEP.new(key)

