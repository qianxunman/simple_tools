# simple_tools
平时开发的小工具

## Google Maps 距离汇总（支持途径点）
`apps/google_maps_distance.py` 可以读取行程数据（CSV/Excel），调用 Google Maps Directions API 计算每个人每天的开车距离，且会考虑途径点（waypoints）。

示例：

```bash
export GOOGLE_MAPS_API_KEY="你的 API Key"
python apps/google_maps_distance.py \
  --input data/trips.xlsx \
  --output data/daily_km.xlsx \
  --waypoint-separator "|"  # 多个途径点用 | 分隔
```

输入文件需包含列：`name`、`date`、`origin`、`destination`，可选列 `waypoints`（如 `A站|B站`）。脚本会按 `name+date` 汇总每日总里程。
