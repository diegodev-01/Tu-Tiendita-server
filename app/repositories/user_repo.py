from db import db
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRepository:
    def __init__(self):
        self.collection = db["users"]

    def get_user_by_username(self, username: str):
        return self.collection.find_one({"username": username})

    def create_user(self, user_data: dict):
        user_data["password"] = pwd_context.hash(user_data["password"])
        if "roles" not in user_data:
            user_data["roles"] = ["customer"]
        if "permissions" not in user_data:
            user_data["permissions"] = ["product:view"]

        return self.collection.insert_one(user_data)

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def update_password(self, username: str, new_password_plain: str):
        new_hashed_password = pwd_context.hash(new_password_plain)

        return self.collection.update_one(
            {"username": username}, {"$set": {"password": new_hashed_password}}
        )

    def update_user_data(self, username: str, data: dict):
        if "password" in data:
            data["password"] = pwd_context.hash(data["password"])

        return self.collection.update_one({"username": username}, {"$set": data})

    def delete_user(self, username: str):
        return self.collection.delete_one({"username": username})
