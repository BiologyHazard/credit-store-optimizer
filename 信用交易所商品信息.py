import csv
import json
from pathlib import Path


信用交易所商品信息路径 = Path("数据/信用交易所商品信息.csv")
物品价值表路径 = Path("数据/item_value_table.json")
物品价值表 = json.loads(物品价值表路径.read_text('utf-8'))
物品名称到价值的映射字典 = {item['name']: item['apValue'] for item in 物品价值表} | {
    '家具零件': 0.0001,
    '加急许可': 0.01,
}
信用交易所商品名称列表: list[str] = []
信用交易所商品价格: dict[str, int] = {}
信用交易所商品理智价值: dict[str, float] = {}
with open(信用交易所商品信息路径, 'r', encoding='utf-8', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile, delimiter='\t', quotechar='|')
    for row in csv_reader:
        名称 = row['名称']
        物品 = row['物品']
        数量 = int(row['数量'])
        if not row['价格']:  # 跳过 讯使、嘉维尔、坚雷
            continue
        价格 = int(row['价格'])
        信用交易所商品名称列表.append(名称)
        信用交易所商品价格[名称] = 价格
        物品的理智价值 = 物品名称到价值的映射字典[物品]
        信用交易所商品理智价值[名称] = 物品的理智价值 * 数量
