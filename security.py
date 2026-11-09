from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hash_password(password: str):
    final_password = password_hash.hash(password)

    return final_password

def verify_password(password: str, hashed_password: str):
    return password_hash.verify(password, hashed_password)