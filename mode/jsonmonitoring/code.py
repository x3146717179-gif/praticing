import json
from collections import defaultdict
from pathlib import Path
from typing import Any
def analyze_json_files(json_files:str)-> dict[str,Any]:
    #保存每台设备的数据,defaultdict的默认值是一个字典，如果device_id不存在，则会创建一个新的字典作为默认值
    #lambda函数用于定义默认值的结构
    stats = defaultdict(lambda: {
        "count": 0,
        "total":0,
        "average":0
    })
    high_temperature_count = 0
    skip_files_count = 0
    path = Path(json_files)
    #判断路径是否存在
    if not path.exists():
        print(f"路径{json_files}不存在")
    #with打开文件，自动关闭，逐行读取
    with path.open("r",encoding="utf-8") as f:
        for line in f:
            try:
                record = json.loads(line)
                if not isinstance(record,dict):
                    print(f"跳过无效的json记录: {line.strip()}")
                    skip_files_count += 1
                    continue
                device_id = record.get("device_id")
                temperature = record.get("temperature")
                #检查设备id
                if device_id is None or temperature is None:
                    print(f"跳过缺少字段的记录：{line.strip()}")
                    skip_files_count += 1
                    continue
            except (json.JSONDecodeError, TypeError) :
                print(f"跳过无效的json记录: {line.strip()}")
                skip_files_count += 1
                continue
            stats[device_id]["count"] += 1
            stats[device_id]["total"] += temperature
            if temperature > 30:
                high_temperature_count += 1
    for device_id,data in stats.items():
        data["average"] = data["total"] / data["count"]
    return {
        "device_stats": dict(stats),
        "high_temperature_count": high_temperature_count,
        "skip_files_count": skip_files_count
    }

