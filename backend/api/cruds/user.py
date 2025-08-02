from typing import List, Optional
from api.schemas.user import User, UserCreate, UserUpdate

class UserCRUD:
    def __init__(self):
        # In-memory storage for now (replace with database later)
        self.users_db: List[User] = []
        self.next_id = 1
    
    def get_users(self) -> List[User]:
        return self.users_db
    
    def get_user(self, user_id: int) -> Optional[User]:
        for user in self.users_db:
            if user.id == user_id:
                return user
        return None
    
    def create_user(self, user_create: UserCreate) -> User:
        new_user = User(
            id=self.next_id,
            name=user_create.name,
            email=user_create.email
        )
        self.users_db.append(new_user)
        self.next_id += 1
        return new_user
    
    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        for i, user in enumerate(self.users_db):
            if user.id == user_id:
                update_data = user_update.model_dump(exclude_unset=True)
                updated_user = user.model_copy(update=update_data)
                self.users_db[i] = updated_user
                return updated_user
        return None
    
    def delete_user(self, user_id: int) -> bool:
        for i, user in enumerate(self.users_db):
            if user.id == user_id:
                del self.users_db[i]
                return True
        return False