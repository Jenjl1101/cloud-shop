import datetime
from typing import Tuple, Optional

class ListingService:
    def __init__(self, store):
        self.store = store
    
    def create_listing(self, username: str, title: str, description: str, price: float, category: str) -> Tuple[str, Optional[str]]:
        """創建新列表"""
        # 驗證用戶
        user = self.store.find_user_by_username(username)
        if not user:
            return "", "unknown user"
        
        # 檢查並更新類別
        cat = self.store.find_category_by_name(category)
        if not cat:
            # 創建新類別
            self.store.save_category({'name': category, 'listing_count': 0})
        
        # 更新類別計數
        cat = self.store.find_category_by_name(category)
        self.store.update_category(category, {'listing_count': cat.listing_count + 1})
        
        # 創建列表
        listing_data = {
            'title': title,
            'description': description,
            'price': price,
            'username': username,
            'category': category
        }
        
        listing_id, error = self.store.save_listing(listing_data)
        if error:
            return "", error
        
        return str(listing_id), None
    
    def get_listing(self, username: str, listing_id: int) -> Tuple[str, Optional[str]]:
        """獲取列表詳情"""
        # 驗證用戶
        user = self.store.find_user_by_username(username)
        if not user:
            return "", "unknown user"
        
        # 查詢列表
        listing = self.store.find_listing_by_id(listing_id)
        if not listing:
            return "", "not found"
        
        # 格式化輸出
        created_at = listing['created_at']
        if isinstance(created_at, str):
            try:
                dt = datetime.datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                created_at = dt.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                pass
        else:
            created_at = created_at.strftime("%Y-%m-%d %H:%M:%S")
        
        return f"{listing['title']}|{listing['price']}|{created_at}|{listing['category']}|{listing['username']}", None
    
    def delete_listing(self, username: str, listing_id: int) -> Tuple[str, Optional[str]]:
        """刪除列表"""
        # 驗證用戶
        user = self.store.find_user_by_username(username)
        if not user:
            return "", "unknown user"
        
        # 查詢列表
        listing = self.store.find_listing_by_id(listing_id)
        if not listing:
            return "", "listing does not exist"
        
        # 驗證所有權
        if listing['username'] != username:
            return "", "listing owner mismatch"
        
        # 更新類別計數
        category = listing['category']
        cat = self.store.find_category_by_name(category)
        if cat:
            new_count = cat.listing_count - 1
            if new_count <= 0:
                # 刪除空類別
                self.store.delete_category(category)
            else:
                # 更新計數
                self.store.update_category(category, {'listing_count': new_count})
        
        # 刪除列表
        success, error = self.store.delete_listing_by_id(listing_id)
        if not success:
            return "", error
        
        return "Success", None