from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from ..utils.file_operations import read_file, write_file, get_decrypted_file_path
import os, binascii

MAX_RSA_BLOCK_SIZE = 256


def decrypt_rsa(encrypted_file_path, private_key_path, directory):
    try:
        private_key_data = read_file(private_key_path)
        private_key = RSA.import_key(private_key_data)
        cipher_rsa = PKCS1_OAEP.new(private_key)

        encrypted_data = read_file(encrypted_file_path)
        decrypted_data = b""

        for i in range(0, len(encrypted_data), MAX_RSA_BLOCK_SIZE):
            block = encrypted_data[i : i + MAX_RSA_BLOCK_SIZE]
            decrypted_block = cipher_rsa.decrypt(block)
            decrypted_data += decrypted_block

        decrypted_file_path = get_decrypted_file_path(encrypted_file_path)
        decrypted_file_full_path = os.path.join(
            directory, os.path.basename(decrypted_file_path)
        )
        write_file(decrypted_file_full_path, decrypted_data)

        return decrypted_file_full_path
    except Exception as e:
        raise Exception(f"Error during RSA decryption: {e}")

def layered_rsa_decrypt(encrypted_aes_key_hex, private_key_path):
    encrypted_aes_key = binascii.unhexlify(encrypted_aes_key_hex)
    # for private_key_path in private_key_path[::-1]:
    with open(private_key_path, 'r') as key_file:
        private_key = RSA.import_key(key_file.read())
        cipher = PKCS1_OAEP.new(private_key)
        encrypted_aes_key = cipher.decrypt(encrypted_aes_key)
    return encrypted_aes_key.hex()