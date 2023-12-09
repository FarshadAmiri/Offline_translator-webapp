from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_v1_5
from base64 import b64decode


def decode_chuncks(encrypted_chunks, lang, chunkded=False):
    with open('private_key.pem', 'rb') as f:
        private_key_data = f.read()
    private_key = RSA.import_key(private_key_data)
    print(f"\private_key: {private_key}\n")
    cipher = PKCS1_v1_5.new(private_key)

    if chunkded == False:
        encrypted_chuncks = [encrypted_chunks]

    decrypted_chuncks = []
    for txt in encrypted_chuncks:
        txt_bytes = b64decode(txt)
        decrypted_bytes = cipher.decrypt(txt_bytes, None)
        decrypted_text = decrypted_bytes.decode('utf-8')
        if lang == "Persian":
            decrypted_text = b64decode(decrypted_text).decode('utf-8')
        decrypted_chuncks.append(decrypted_text)

    decrypted_text = "".join(decrypted_chuncks)
    return decrypted_text


def encrypt_and_chunck(text, lang):
    with open('public_key.pem', 'rb') as f:
        public_key_data = f.read()
    public_key = RSA.import_key(public_key_data)
    print(f"\public_key: {public_key}\n")
    cipher = PKCS1_v1_5.new(public_key)

    if lang == "Persian":
        text = text.encode('utf-8')

    encrypted_chunks = []
    for i in range(0, len(text), 128):
        chunk = text[i:i + 128]
        encrypted_bytes = cipher.encrypt(chunk)
        encrypted_chunk = b64encode(encrypted_bytes).decode('utf-8')
        encrypted_chunks.append(encrypted_chunk)
        