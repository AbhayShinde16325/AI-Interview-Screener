import unittest

from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


class TestSecurity(unittest.TestCase):

    def test_password_hash_roundtrip(self):
        password = "SuperSecret123!"
        hashed = hash_password(password)

        self.assertNotEqual(hashed, password)
        self.assertTrue(verify_password(password, hashed))
        self.assertFalse(verify_password("wrong-password", hashed))

    def test_jwt_roundtrip(self):
        token = create_access_token("user-123")
        payload = decode_access_token(token)
        self.assertIsNotNone(payload)
        self.assertEqual(payload["sub"], "user-123")

    def test_decode_rejects_garbage(self):
        self.assertIsNone(decode_access_token("not-a-jwt"))


if __name__ == "__main__":
    unittest.main()
