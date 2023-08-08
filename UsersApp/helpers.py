import json
from base64 import encode

from jwcrypto import jwe, jwk

from BooksProject.settings import SIMPLE_JWT


def encrypt_jwt(payload: dict) -> str:
    """Function to encrypt the JWT token using JWE"""
    payload_json = json.dumps(payload)
    jwk_key = jwk.JWK.from_json(SIMPLE_JWT["JWE_SECRET_KEY"])
    jwetoken = jwe.JWE(payload_json, encode({"alg": SIMPLE_JWT["JWE_ALGORITHM"]}))
    jwetoken.add_recipient(jwk_key)
    encrypted_token = jwetoken.serialize(compact=True)
    return encrypted_token


def decrypt_jwt(encrypted_token: str) -> dict:
    """Function to decrypt the JWT token using JWE"""
    jwetoken = jwe.JWE()
    jwetoken.deserialize(encrypted_token, key=jwk.JWK.from_json(SIMPLE_JWT["JWE_SECRET_KEY"]))
    payload_json = jwetoken.payload.decode("utf-8")
    payload = json.loads(payload_json)
    return payload
