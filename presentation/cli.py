import shlex
import re
from typing import Tuple, Optional

class CLI:
    def __init__(self, user_service, listing_service, category_service):
        self.user_service = user_service
        self.listing_service = listing_service
        self.category_service = category_service
    
    def parse_command(self, command: str) -> list[str]:
        """正確解析命令字串，處理單引號與雙引號的內容"""
        pattern = r'(\w+|"(?:[^"]*)"|\'(?:[^\']*)\')'
        matches = re.findall(pattern, command)
        # 移除引號
        return [m.strip("'\"") for m in matches]

    def process_command(self, command: str) -> str:
        """處理用戶命令"""
        args = self.parse_command(command)

        if not args:
            return ""

        cmd, args = args[0], args[1:]

        if cmd == "REGISTER":
            if len(args) != 1:
                return "Error - invalid command format"

            response, error = self.user_service.register(args[0])
            if error:
                return f"Error - {error}"
            return response

        elif cmd == "CREATE_LISTING":
            if len(args) != 5:
                return "Error - invalid command format"

            username = args[0]
            title = args[1]
            description = args[2]

            try:
                price = float(args[3])
            except ValueError:
                return "Error - invalid price format"

            category = args[4]

            response, error = self.listing_service.create_listing(
                username, title, description, price, category
            )
            if error:
                return f"Error - {error}"
            return response

        elif cmd == "GET_LISTING":
            if len(args) != 2:
                return "Error - invalid command format"

            username = args[0]

            try:
                listing_id = int(args[1])
            except ValueError:
                return "Error - invalid listing ID"

            response, error = self.listing_service.get_listing(username, listing_id)
            if error:
                return f"Error - {error}"
            return response

        elif cmd == "DELETE_LISTING":
            if len(args) != 2:
                return "Error - invalid command format"

            username = args[0]

            try:
                listing_id = int(args[1])
            except ValueError:
                return "Error - invalid listing ID"

            response, error = self.listing_service.delete_listing(username, listing_id)
            if error:
                return f"Error - {error}"
            return response

        elif cmd == "GET_CATEGORY":
            if len(args) != 2:
                return "Error - invalid command format"

            username = args[0]
            category = args[1]

            response, error = self.category_service.get_category_listings(username, category)
            if error:
                return f"Error - {error}"
            return response

        elif cmd == "GET_TOP_CATEGORY":
            if len(args) != 1:
                return "Error - invalid command format"

            username = args[0]

            response, error = self.category_service.get_top_category(username)
            if error:
                return f"Error - {error}"
            return response

        else:
            return f"Error - unknown command: {cmd}"
