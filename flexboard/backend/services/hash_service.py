"""
Hash library from 'passlib'

We are giving the context of what encryptor we will be using, in this case, bcrypt

@staticmethod annotation gets rid of suggestion
- I didn't want to remove it from the class declaration
- Since we don't use 'self' or instances of the class, Python suggests that this method is a static method..
- Because it is a static method.
"""

from passlib.context import CryptContext

# type of encryptor, bcrypt password encryptor
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class HashService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        # returns 'true' or 'false'
        is_password_valid: bool = pwd_context.verify(plain_password, hashed_password)
        return is_password_valid

    @staticmethod
    def hash(plain_password: str):
        return pwd_context.hash(plain_password)


hash_service: HashService = HashService()
