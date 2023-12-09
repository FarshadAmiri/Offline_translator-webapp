from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# Generate a private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Export private key to text (PEM format)
private_key_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Export public key to text (PEM format)
public_key_pem = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Save private key to a file
with open("private_key.pem", 'wb') as f:
    f.write(private_key_pem)

# Save public key to a file
with open("public_key.pem", 'wb') as f:
    f.write(public_key_pem)

# Load private key from text
with open('private_key.pem', 'rb') as f:
    private_key_loaded = serialization.load_pem_private_key(
        f.read(),
        password=None
    )

# Load public key from text
with open('public_key.pem', 'rb') as f:
    public_key_loaded = serialization.load_pem_public_key(
        f.read()
    )