import hashlib

senha = "Vinicius25@"  # substitua pela sua senha desejada
senha_hash = hashlib.sha256(senha.encode()).hexdigest()

print(senha_hash)