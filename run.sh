#!/bin/bash

# 檢查虛擬環境是否存在
if [ ! -d "venv" ]; then
  echo "Virtual environment not found. Please run build.sh first."
  exit 1
fi

# 啟用虛擬環境
source venv/bin/activate

# 運行應用程序
python cloudshop.py "$@"

# 退出虛擬環境
deactivate