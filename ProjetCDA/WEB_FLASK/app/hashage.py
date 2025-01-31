from werkzeug.security import generate_password_hash

passwordj = "secure"
hashed_passwordj = generate_password_hash(passwordj)

print("Jardel mot de passe: ",hashed_passwordj)

passwordi = "bonbon"
hashed_passwordi = generate_password_hash(passwordi)

print("Indrich mot de passe: ",hashed_passwordi)