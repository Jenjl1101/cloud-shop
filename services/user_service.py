from typing import Tuple, Optional

class UserService:
    def __init__(self, store):
        self.store = store
    
    def register(self, username: str) -> Tuple[str, Optional[str]]:
        """註冊新用戶"""
        success, error = self.store.save_user(username)
        if not success:
            return "", error
        return "Success", None
    
    def authenticate(self, username: str) -> Optional[str]:
        """驗證用戶是否存在"""
        user = self.store.find_user_by_username(username)
        if not user:
            return "unknown user"
        return None