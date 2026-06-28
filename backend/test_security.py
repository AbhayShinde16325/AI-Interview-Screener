from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)

password = "Password123!"

hashed_password = hash_password(password)

print("Hash:")
print(hashed_password)

print("\nPassword Verified:")
print(verify_password(password, hashed_password))

token = create_access_token("123456")

print("\nJWT:")
print(token)

print("\nDecoded Payload:")
print(decode_access_token(token))