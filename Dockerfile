# 使用 Python 3.10 作為基礎鏡像
FROM python:3.10-slim

# 設定工作目錄
WORKDIR /app

# 複製應用程式檔案
COPY . /app/

# 安裝依賴套件
RUN pip install --no-cache-dir -r requirements.txt

# 確保腳本可執行
RUN chmod +x cloudshop.py run.sh

# 刪除現有的資料庫檔案（如果存在）
RUN if [ -f "cloudshop.db" ]; then rm cloudshop.db; fi

# 設定容器啟動時執行的命令
CMD ["./run.sh"]
