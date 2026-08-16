from cryptography.fernet import Fernet

# Generate key once and save securely
key = Fernet.generate_key()
print("Generated Key:", key)   # <-- print to see the key

cipher = Fernet(key)

# Encrypt log
encrypted = cipher.encrypt(b"User command: open google")
print("Encrypted:", encrypted)  # <-- print to see gibberish

# Decrypt when needed
decrypted = cipher.decrypt(encrypted)
print("Decrypted:", decrypted)  # <-- print to see original
