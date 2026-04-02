from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from app.db.supabase_client import insert_data, fetch_data
import uuid

class UserService:
    def create_user(self, user_in: UserCreate):
        user_data = user_in.dict()
        user_data['password'] = get_password_hash(user_data['password'])
        user_data['id'] = str(uuid.uuid4())
        
        # Insert user directly using the reusable db layer
        inserted_user = insert_data('users', user_data)
        return inserted_user if inserted_user else None

    def get_user_by_email(self, email: str):
        users = fetch_data('users', {'email': email})
        return users[0] if users else None

    def get_user_by_id(self, user_id: str):
        users = fetch_data('users', {'id': user_id})
        return users[0] if users else None

user_service = UserService()
