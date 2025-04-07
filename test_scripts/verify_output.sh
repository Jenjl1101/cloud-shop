#!/bin/bash

# 執行應用程序並捕獲輸出
chmod +x run.sh
./run.sh < tests/commands.txt | tee tests/output.log

cd tests

# 移除時間戳記並比較輸出
sed 's/[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\} [0-9]\{2\}:[0-9]\{2\}:[0-9]\{2\}/TIMESTAMP/g' output.log > output_no_timestamps.log
sed 's/[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\} [0-9]\{2\}:[0-9]\{2\}:[0-9]\{2\}/TIMESTAMP/g' expected_output.log > expected_output_no_timestamps.log

if diff output_no_timestamps.log expected_output_no_timestamps.log; then
  echo "Output is as expected, ignoring timestamps."
  exit 0
else
  echo "Output differs from expected."
  exit 1
fi 