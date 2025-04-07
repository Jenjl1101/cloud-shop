from sqlalchemy import func, exc
import datetime

# Import models from the models package
from models import Base, User, Listing, Category, get_engine, get_session_maker

class DBStore:
    """ORM-based database storage implementation - 純粹的數據存取層"""
    
    def __init__(self, db_url):
        """Initialize storage with database URL"""
        self.engine = get_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = get_session_maker(self.engine)
        self.next_id = self._get_next_id()
    
    def _get_next_id(self):
        """Get next available listing ID"""
        session = self.Session()
        try:
            max_id = session.query(func.max(Listing.id)).scalar()
            return max(100001, (max_id or 100000) + 1)
        finally:
            session.close()
    
    # User methods
    def save_user(self, username):
        """儲存新用戶，返回是否成功和可能的錯誤"""
        session = self.Session()
        try:
            new_user = User(username=username)
            session.add(new_user)
            session.commit()
            return True, None
        except exc.IntegrityError:
            session.rollback()
            return False, "user already existing"
        finally:
            session.close()
    
    def find_user_by_username(self, username):
        """根據用戶名查詢用戶"""
        session = self.Session()
        try:
            return session.query(User).filter(func.lower(User.username) == func.lower(username)).first()
        finally:
            session.close()
    
    # Listing methods
    def save_listing(self, listing_data):
        """儲存新列表"""
        session = self.Session()
        try:
            # 設置 ID
            listing_id = self.next_id
            self.next_id += 1
            
            # 創建列表對象
            new_listing = Listing(
                id=listing_id,
                title=listing_data['title'],
                description=listing_data['description'],
                price=listing_data['price'],
                username=listing_data['username'],
                category=listing_data['category']
            )
            
            session.add(new_listing)
            
            # 更新類別的 listing_count
            category = session.query(Category).filter_by(name=listing_data['category']).first()
            if category:
                category.listing_count += 1
            
            session.commit()
            return listing_id, None
        except Exception as e:
            session.rollback()
            return None, str(e)
        finally:
            session.close()
    
    def find_listing_by_id(self, listing_id):
        """根據 ID 查詢列表"""
        session = self.Session()
        try:
            listing = session.query(Listing).filter_by(id=listing_id).first()
            if not listing:
                return None
            
            # 轉換為字典
            listing_dict = {
                'id': listing.id,
                'title': listing.title,
                'description': listing.description,
                'price': listing.price,
                'username': listing.username,
                'category': listing.category,
                'created_at': listing.created_at
            }
            
            return listing_dict
        finally:
            session.close()
    
    def delete_listing_by_id(self, listing_id):
        """根據 ID 刪除列表"""
        session = self.Session()
        try:
            listing = session.query(Listing).filter_by(id=listing_id).first()
            if not listing:
                return False, "listing does not exist"
            
            # 獲取類別名稱，用於更新 listing_count
            category_name = listing.category
            
            # 刪除列表
            session.delete(listing)
            
            # 更新類別的 listing_count
            category = session.query(Category).filter_by(name=category_name).first()
            if category and category.listing_count > 0:
                category.listing_count -= 1
            
            session.commit()
            return True, None
        except Exception as e:
            session.rollback()
            return False, str(e)
        finally:
            session.close()
    
    # Category methods
    def find_category_by_name(self, category_name):
        """根據名稱查詢類別"""
        session = self.Session()
        try:
            return session.query(Category).filter_by(name=category_name).first()
        finally:
            session.close()
    
    def save_category(self, category_data):
        """儲存類別"""
        session = self.Session()
        try:
            new_category = Category(
                name=category_data['name'],
                listing_count=category_data.get('listing_count', 0)
            )
            session.add(new_category)
            session.commit()
            return True, None
        except Exception as e:
            session.rollback()
            return False, str(e)
        finally:
            session.close()
    
    def update_category(self, category_name, updates):
        """更新類別信息"""
        session = self.Session()
        try:
            category = session.query(Category).filter_by(name=category_name).first()
            if not category:
                return False, "category not found"
            
            # 更新屬性
            for key, value in updates.items():
                setattr(category, key, value)
            
            session.commit()
            return True, None
        except Exception as e:
            session.rollback()
            return False, str(e)
        finally:
            session.close()
    
    def delete_category(self, category_name):
        """刪除類別"""
        session = self.Session()
        try:
            category = session.query(Category).filter_by(name=category_name).first()
            if not category:
                return False, "category not found"
            
            session.delete(category)
            session.commit()
            return True, None
        except Exception as e:
            session.rollback()
            return False, str(e)
        finally:
            session.close()
    
    def find_listings_by_category(self, category_name):
        """查詢特定類別的所有列表"""
        session = self.Session()
        try:
            listings = session.query(Listing).filter_by(category=category_name).order_by(Listing.created_at.desc()).all()
            
            result = []
            for listing in listings:
                listing_dict = {
                    'id': listing.id,
                    'title': listing.title,
                    'description': listing.description,
                    'price': listing.price,
                    'username': listing.username,
                    'category': listing.category,
                    'created_at': listing.created_at
                }
                result.append(listing_dict)
            
            return result
        finally:
            session.close()
    
    # 在 DBStore (persistence 層) 中
    def find_categories_with_max_listing_count(self):
        """查詢具有最大列表數量的所有類別"""
        session = self.Session()
        try:
            # 首先找出最大的 listing_count
            max_count = session.query(func.max(Category.listing_count)).scalar()
            if max_count is None:
                return []
            
            # 查詢所有具有該數量的類別
            categories = session.query(Category).filter_by(listing_count=max_count).all()
            
            # 將 ORM 對象轉換為字典
            result = []
            for cat in categories:
                result.append({
                    'name': cat.name,
                    'listing_count': cat.listing_count
                })
                
            return result
        finally:
            session.close()
    
    def synchronize_category_counts(self):
        """同步所有類別的 listing_count 與實際的 Listing 數量"""
        session = self.Session()
        try:
            # 獲取所有類別
            categories = session.query(Category).all()
            
            for category in categories:
                # 計算該類別的實際列表數
                actual_count = session.query(Listing).filter_by(category=category.name).count()
                
                # 更新類別的 listing_count
                category.listing_count = actual_count
            
            session.commit()
            return True, None
        except Exception as e:
            session.rollback()
            return False, str(e)
        finally:
            session.close()