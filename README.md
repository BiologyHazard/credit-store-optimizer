# Credit Store Optimizer

信用商店最优购买策略、信用的价值

- bilibili: https://www.bilibili.com/read/cv36832660
- 森空岛: https://www.skland.com/article?id=2162530
- NGA: https://bbs.nga.cn/read.php?tid=41171729

---

- 购买指标向量：一个 10-元组，每个元素都是 `bool` 类型，表示是否购买了对应位置的商品。例如，`(True, False, True, False, False, False, False, False, False, False)` 表示购买了第 1 和第 3 个物品。

## $K_C^n(c)$ 相关的变量命名规则
- `KnCc` 是一个实数，即 $K_C^n(c)$
- 每用一个 `"·"`，就表示这一维是变量
- 例如，`KnC·` 是一个 1 维数组（或者 1 个变量的函数），`KnC·[c]` = $K_C^n(c)$
- 例如，`Kn··` 是一个 2 维数组或函数，`Kn··[C][c]` = $K_C^n(c)$
- 例如，`K···` 是一个 3 维数组或函数，`K···[n][C][c]` = $K_C^n(c)$
- 例如，`K·C·` 是一个 2 维数组或函数，`K·C·[n][c]` = $K_C^n(c)$
- 可能会使用下划线 `"_"` 分隔，例如，`K_n_C_·` 与 `KnC·` 是等价的

## $L_D^n(c, e)$ 相关的变量命名规则
- `LnDce` 是一个实数，即 $L_D^n(c, e)$
- 每用一个 `"·"`，就表示这一维是变量
