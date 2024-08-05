import csv
import json
from datetime import date, datetime
from pathlib import Path

from 信用交易所模型 import 信用交易所, 信用交易所商品


已通关主题曲3_8账号序号列表路径 = Path("数据/已通关主题曲3-8账号序号列表.json")
已通关主题曲3_8账号序号列表 = json.loads(已通关主题曲3_8账号序号列表路径.read_text('utf-8'))


def 初步筛选函数(账号序号):
    return 账号序号 in 已通关主题曲3_8账号序号列表


原始数据路径 = Path("数据/统计数据.csv")
信用交易所统计字典: dict[tuple[int, date], 信用交易所] = {}
with open(原始数据路径, 'r', encoding='utf-8', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile, delimiter='\t', quotechar='|')
    try:
        while True:
            接下来10行 = [next(csv_reader) for _ in range(10)]
            接下来首行 = 接下来10行[0]
            账号序号 = int(接下来首行['账号序号'])
            if not 初步筛选函数(账号序号):
                continue
            日期 = datetime.strptime(接下来首行['日期'], '%Y-%m-%d').date()
            剩余信用 = int(接下来首行['剩余信用'])
            商品列表 = []
            for i, row in enumerate(接下来10行):
                序号 = int(row['序号'])
                assert 序号 == i
                物品名称 = row['名称']
                折扣 = int(row['折扣'])
                是否购买 = row['是否购买'] == 'TRUE'
                商品列表.append(信用交易所商品(物品名称=物品名称, 折扣=折扣, 已购买=是否购买))
            信用交易所统计字典[账号序号, 日期] = 信用交易所(剩余信用=剩余信用, 商品列表=商品列表)
    except StopIteration:
        pass
