from src.signature import sign_data_by_rsa, verify_data_by_rsa
import json


def test_generate_signature_and_verify(given_private_pem_file, given_public_pem_file):
    given_payload = {
        "username": "paj-cm",
        "usergroup": "haimp-developer",
        "role": "admin"
    }
    given_message = json.dumps(given_payload).encode('utf-8')

    # 시나리오 상 이걸 작업하는 곳: auth server
    signature = sign_data_by_rsa(given_message, given_private_pem_file)

    # 검증하고 싶은 곳: api gateway server
    assert verify_data_by_rsa(given_message, signature, given_public_pem_file) is True


def test_scenario1_client_is_thief(given_private_pem_file, given_public_pem_file):
    thief_payload = {
        "username": "paj-cm",
        "usergroup": "haimp-developer",
        "role": "admin"
    }
    given_message = json.dumps(thief_payload).encode('utf-8')

    # 거짓된 시그니처를 담아서 보내기
    signature = b'12369127647812690ashjkdkfgwgoe7irtcboiw7segbcafioweasndkask'

    # 검증하고 싶은 곳: api gateway server
    assert verify_data_by_rsa(given_message, signature, given_public_pem_file) is False


def test_scenario2_client_is_thief(given_private_pem_file, given_public_pem_file):
    given_payload = {
        "username": "paj-cm",
        "usergroup": "haimp-developer",
        "role": "admin"
    }
    given_message = json.dumps(given_payload).encode('utf-8')
    signature = sign_data_by_rsa(given_message, given_private_pem_file)

    # 메세지를 조작 시도
    fraud_payload = {
        **given_payload,
        "username": "pai-sj"
    }
    fraud_message = json.dumps(fraud_payload).encode('utf-8')

    assert verify_data_by_rsa(fraud_message, signature, given_public_pem_file) is False