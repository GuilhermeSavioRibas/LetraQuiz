from werkzeug.security import generate_password_hash

admin_password = generate_password_hash('admin')
user_password = generate_password_hash('user')

print (admin_password)
print (user_password)