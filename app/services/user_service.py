from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from app.db.supabase_client import insert_data, fetch_data, update_data
import uuid


class UserService:
    TABLE = "users"

    def create_user(self, user_in: UserCreate):
        user_data = user_in.model_dump()
        user_data['password'] = get_password_hash(user_data['password'])
        user_data['id'] = str(uuid.uuid4())
        inserted_user = insert_data(self.TABLE, user_data)
        return inserted_user if inserted_user else None

    def get_user_by_email(self, email: str):
        users = fetch_data(self.TABLE, {'email': email})
        return users[0] if users else None

    def get_user_by_id(self, user_id: str):
        users = fetch_data(self.TABLE, {'id': user_id})
        return users[0] if users else None

    def get_all_users(self):
        return fetch_data(self.TABLE)

    def set_user_active(self, user_id: str, is_active: bool):
        updated = update_data(self.TABLE, user_id, {'is_active': is_active})
        return updated if updated else None


user_service = UserService()
