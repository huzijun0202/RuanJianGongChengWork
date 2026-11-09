# 软件工程实验三 · 面向对象的系统建模 A

本目录为《软件工程》实验三的实现代码，对应实验报告中的四个 UML 类模型：

| 图号 | 模型 | 源文件 |
| --- | --- | --- |
| A1-1 | `Thoroughbred` 优良品质的马 | `a1_1_thoroughbred.py` |
| A1-2 | `College` / `Building` / `Course`（聚合、组合、约束） | `a1_2_college.py` |
| A1-3 | `School` / `Department` / `Instructor` / `Subject` / `Student`（多重性） | `a1_3_school.py` |
| A1-4 | 网上购物系统（抽象类、泛化、组合、聚合） | `a1_4_shopping.py` |

## 运行

```bash
cd 实验作业3/code
python demo.py
```

依赖：Python 3.9+，仅使用标准库（`datetime`、`abc`、`enum`），无需安装第三方包。

## 设计与 UML 的对应关系

- **可见性**：UML 中前缀 `-` 的属性在代码中对应 `__name` 私有属性；前缀 `+` 的操作对应公有方法。
- **A1-2**：`College` 通过列表*聚合* `Building`（移除后 `Building` 仍然存活），
  通过列表*组合* `Course`（移除即销毁），并用 `addCourse` 保证
  `{Course 一定在某个 Building 中进行}` 这一约束。
- **A1-3**：用校验方法保证题设多重性——每个系至少 1 名教师、1 门课程；
  每位教师教授 1~3 门课；每名学生参加 1~5 门课；学院可有 0..* 名学生。
- **A1-4**：`Payment` 为抽象类（`pay()` 为抽象方法），
  `Credit` / `Cash` / `WireTransfer` / `AliPay` / `WeixinPay` 为其五个子类；
  `Order` 组合 `OrderDetail`、聚合 `Payment`，`OrderDetail` 关联 `Product` 并实现
  `calculateSubTotal()` 与 `calculateWeight()`；`Product` 提供
  `getPriceForQuantity(quantity)` 与 `getWeight()`。
