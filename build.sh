#!/bin/bash

REQUIRED_PYTHON="3.6"
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')

if [[ $(echo -e "$PYTHON_VERSION\n$REQUIRED_PYTHON" | sort -V | head -n1) != "$REQUIRED_PYTHON" ]]; then
  echo "Python 3.6 or higher is required. Found: $PYTHON_VERSION"
  exit 1
fi

# 創建虛擬環境
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi

# 啟動虛擬環境並安裝相依套件
source venv/bin/activate

# 安裝依賴（如果有 requirements.txt）
if [ -f "requirements.txt" ]; then
  echo "Installing dependencies..."
  pip install -r requirements.txt
fi


# 刪除現有的數據庫文件（如果存在）
if [ -f "cloudshop.db" ]; then
  echo "Removing existing database..."
  rm cloudshop.db
fi

# 確保文件可執行
chmod +x cloudshop.py
chmod +x run.sh

# 離開虛擬環境
deactivate

echo "Build completed successfully."
