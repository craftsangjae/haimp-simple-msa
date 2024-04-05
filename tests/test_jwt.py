import pytest

from src.auth import load_pem
import json
import jwt
import base64
from datetime import datetime
from jwt.exceptions import ExpiredSignatureError, InvalidAudienceError

def test_jwt_encode(given_private_pem_file):
    given_payload = {
        "user-name": "sang jae",
        "user-group": "haimp-developer",
        "user-role": "admin",
    }
    private_pem = load_pem(given_private_pem_file)

    jwt_token = jwt.encode(given_payload, private_pem, algorithm='RS256')
    header_b64, payload_b64, signature = jwt_token.split('.')

    # 헤더 확인
    result_header = json.loads(base64.decodebytes(header_b64.encode('utf-8')))
    assert result_header['alg'] == 'RS256'
    assert result_header['typ'] == 'JWT'

    # payload 확인
    result_payload = json.loads(base64.decodebytes(payload_b64.encode('utf-8')))
    assert result_payload == given_payload


def test_verify_using_jwt(given_private_pem_file, given_public_pem_file):
    """ jwt.decode는 사실상 verify 기능을 동시에 수행한다. """
    given_payload = {
        "user-name": "sang jae",
        "user-group": "haimp-developer",
        "user-role": "admin",
    }
    private_pem = load_pem(given_private_pem_file)
    public_pem = load_pem(given_public_pem_file)
    given_token = jwt.encode(given_payload, private_pem, algorithm='RS256')

    output = jwt.decode(given_token, public_pem, algorithms=['RS256'])
    assert given_payload == output


def test_spec_exp_jwt_normal_case(given_private_pem_file, given_public_pem_file):
    given_payload = {
        "exp": datetime.now().timestamp() + 10,
        "user-name": "sang jae",
        "user-group": "haimp-developer",
        "user-role": "admin",
    }
    private_pem = load_pem(given_private_pem_file)
    public_pem = load_pem(given_public_pem_file)
    given_token = jwt.encode(given_payload, private_pem, algorithm='RS256')

    output = jwt.decode(given_token, public_pem, algorithms=['RS256'])
    assert given_payload == output


def test_spec_exp_jwt_expired_case(given_private_pem_file, given_public_pem_file):
    given_payload = {
        "exp": datetime.now().timestamp() - 10,
        "user-name": "sang jae",
        "user-group": "haimp-developer",
        "user-role": "admin",
    }
    private_pem = load_pem(given_private_pem_file)
    public_pem = load_pem(given_public_pem_file)
    given_token = jwt.encode(given_payload, private_pem, algorithm='RS256')

    with pytest.raises(ExpiredSignatureError):
        jwt.decode(given_token, public_pem, algorithms=['RS256'])


def test_skip_verify_decode_value(given_private_pem_file, given_public_pem_file):
    """ 만료가 되더라도 payload를 확인하고 싶은 경우에 이거 활용하세요 """
    given_payload = {
        "exp": datetime.now().timestamp() - 10,
        "user-name": "sang jae",
        "user-group": "haimp-developer",
        "user-role": "admin",
    }
    private_pem = load_pem(given_private_pem_file)
    public_pem = load_pem(given_public_pem_file)

    given_token = jwt.encode(given_payload, private_pem, algorithm='RS256')

    output = jwt.decode(given_token, public_pem, algorithms=['RS256'], options={
        "verify_signature": False
    })

    assert given_payload == output


def test_spec_leeway(given_private_pem_file, given_public_pem_file):
    """ 만료가 되더라도 payload를 확인하고 싶은 경우에 이거 활용하세요 """
    given_payload = {
        "exp": datetime.now().timestamp() - 3,
        "user-name": "sang jae",
        "user-group": "haimp-developer",
        "user-role": "admin",
    }
    private_pem = load_pem(given_private_pem_file)
    public_pem = load_pem(given_public_pem_file)

    given_token = jwt.encode(given_payload, private_pem, algorithm='RS256')
    output = jwt.decode(given_token, public_pem, algorithms=['RS256'], leeway=10)

    assert given_payload == output


def test_audience(given_private_pem_file, given_public_pem_file):
    """ 만료가 되더라도 payload를 확인하고 싶은 경우에 이거 활용하세요 """
    given_payload = {
        "aud": "haimp-api-gateway",
        "user-name": "sang jae",
        "user-group": "haimp-developer",
        "user-role": "admin",
    }
    private_pem = load_pem(given_private_pem_file)
    public_pem = load_pem(given_public_pem_file)

    given_token = jwt.encode(given_payload, private_pem, algorithm='RS256')

    output = jwt.decode(given_token, public_pem, algorithms=['RS256'], audience='haimp-api-gateway')
    assert output == given_payload

    with pytest.raises(InvalidAudienceError):
        jwt.decode(given_token, public_pem, algorithms=['RS256'])