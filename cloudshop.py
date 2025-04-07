#!/usr/bin/env python3

import os
import sys
from persistence.db_store import DBStore
from services.user_service import UserService
from services.listing_service import ListingService
from services.category_service import CategoryService
from presentation.cli import CLI

def main():
    # 獲取數據庫路徑，默認為當前目錄下的 cloudshop.db
    db_path = os.environ.get('CLOUDSHOP_DB', 'cloudshop.db')
    
    # 構建 SQLAlchemy 風格的 URL
    db_url = f"sqlite:///{db_path}"
    
    # 創建存儲 (使用 URL 字符串)
    store = DBStore(db_url)  
    
    # 創建服務
    user_service = UserService(store)
    listing_service = ListingService(store)
    category_service = CategoryService(store)
    
    # 創建 CLI
    cli = CLI(user_service, listing_service, category_service)

    # 檢查是否有輸入重定向
    if not sys.stdin.isatty():
        # 從標準輸入讀取命令
        for line in sys.stdin:
            line = line.strip()
            if line:
                result = cli.process_command(line)
                print(result)
    else:
        # 交互式模式
        print("CloudShop CLI started. Type commands to interact.")
        while True:
            try:
                command = input("# ")
                if command.lower() in ['exit', 'quit']:
                    break
                
                result = cli.process_command(command)
                print(result)
                
            except EOFError:
                break
            except KeyboardInterrupt:
                break
    

if __name__ == "__main__":
    main()