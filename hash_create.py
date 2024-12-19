from werkzeug.security import generate_password_hash

# Criar hash para a senha 'admin'
admin_password = generate_password_hash('admin', method='pbkdf2:sha256')

# Criar hash para a senha 'user'
user_password = generate_password_hash('user', method='pbkdf2:sha256')

print("Senha do admin:", admin_password)
print("Senha do usuário:", user_password)