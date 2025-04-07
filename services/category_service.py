import datetime
from typing import Tuple, Optional

class CategoryService:
    def __init__(self, store):
        self.store = store
    
    def get_category_listings(self, username: str, category: str) -> Tuple[str, Optional[str]]:
        """獲取類別下的所有列表"""
        # 驗證用戶
        user = self.store.find_user_by_username(username)
        if not user:
            return "", "unknown user"
        
        # 查詢列表
        listings = self.store.find_listings_by_category(category)
        if not listings:
            return "", "category not found"
        
        
        # 格式化輸出
        result = []
        for listing in listings:
            created_at = listing['created_at']
            if isinstance(created_at, str):
                try:
                    dt = datetime.datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    created_at = dt.strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    pass
            else:
                created_at = created_at.strftime("%Y-%m-%d %H:%M:%S") 
            
            result.append(
                f"{listing['title']}|{listing['description']}|{listing['price']}|{created_at}"
            )
        
        return "\n".join(result), None
    
    def get_top_category(self, username: str) -> Tuple[str, Optional[str]]:
        """獲取列表數量最多的類別"""
        # 驗證用戶
        user = self.store.find_user_by_username(username)
        if not user:
            return "", "unknown user"
        
        # 查詢頂級類別
        top_categories = self.store.find_categories_with_max_listing_count()
        if not top_categories:
            return "", "no categories found"
        
        # 如果有多個類別具有相同的最大數量，按字母順序排序
        if len(top_categories) > 1:
            top_categories.sort(key=lambda x: x['name'])
        
        # 返回排序後的第一個類別
        return "\n".join([x['name'] for x in top_categories]), None