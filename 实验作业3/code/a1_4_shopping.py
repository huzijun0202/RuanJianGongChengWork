# -*- coding: utf-8 -*-
"""A1-4 简化的网上购物系统类模型。

UML 对应（见实验报告 A1-4）：
    Customer  1 --- 0..* Order
    Order     <#>--- 1..* OrderDetail   组合
    OrderDetail 0..* --- 1 Product
    Order     <>--- 0..* Payment        聚合
    Payment 为抽象类，Credit / Cash / WireTransfer / AliPay / WeixinPay 继承之

Order.status 取值为 CREATE、PAID、SHIPPING、DELIVERED、CANCEL 五种状态。
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from enum import Enum


class OrderStatus(Enum):
    CREATE = "CREATE"
    PAID = "PAID"
    SHIPPING = "SHIPPING"
    DELIVERED = "DELIVERED"
    CANCEL = "CANCEL"


class Product:
    """商品项。"""

    def __init__(self, title: str, weight: float, description: str, unit_price: float) -> None:
        self.__title = title
        self.__weight = weight
        self.__description = description
        self.__unit_price = unit_price

    @property
    def title(self) -> str:
        return self.__title

    @property
    def weight(self) -> float:
        return self.__weight

    @property
    def description(self) -> str:
        return self.__description

    # ---------------- 操作 ----------------
    def getPriceForQuantity(self, quantity: int) -> float:
        """按数量计算商品项小计。"""
        if quantity < 0:
            raise ValueError("数量不能为负")
        return round(self.__unit_price * quantity, 2)

    def getWeight(self) -> float:
        return self.__weight

    def __repr__(self) -> str:
        return f"Product({self.__title}, price={self.__unit_price})"


class OrderDetail:
    """订单详情：一条明细对应一种商品及购买数量。"""

    def __init__(self, product: Product, quantity: int) -> None:
        self.__quantity = quantity
        self.__product = product

    @property
    def quantity(self) -> int:
        return self.__quantity

    @property
    def product(self) -> Product:
        return self.__product

    def calculateSubTotal(self) -> float:
        return self.__product.getPriceForQuantity(self.__quantity)

    def calculateWeight(self) -> float:
        return round(self.__product.getWeight() * self.__quantity, 2)

    def __repr__(self) -> str:
        return f"OrderDetail({self.__product.title} x{self.__quantity})"


class Payment(ABC):
    """支付方式抽象类。"""

    def __init__(self, amount: float) -> None:
        self.__amount = amount

    @property
    def amount(self) -> float:
        return self.__amount

    @abstractmethod
    def pay(self) -> bool:
        """执行支付；返回是否成功。"""
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{type(self).__name__}(amount={self.__amount})"


class Credit(Payment):
    def __init__(self, amount: float, number: str, type_: str, expire_date: date) -> None:
        super().__init__(amount)
        self.__number = number
        self.__type = type_
        self.__expireDate = expire_date

    def pay(self) -> bool:
        if self.__expireDate < date.today():
            return False
        return True


class Cash(Payment):
    def __init__(self, amount: float, cash_tendered: float) -> None:
        super().__init__(amount)
        self.__cashTendered = cash_tendered

    def pay(self) -> bool:
        return self.__cashTendered >= self.amount


class WireTransfer(Payment):
    def __init__(self, amount: float, bank_id: str, bank_name: str) -> None:
        super().__init__(amount)
        self.__bankID = bank_id
        self.__bankName = bank_name

    def pay(self) -> bool:
        return bool(self.__bankID and self.__bankName)


class AliPay(Payment):
    def __init__(self, amount: float, number: str) -> None:
        super().__init__(amount)
        self.__number = number

    def pay(self) -> bool:
        return bool(self.__number)


class WeixinPay(Payment):
    def __init__(self, amount: float, number: str) -> None:
        super().__init__(amount)
        self.__number = number

    def pay(self) -> bool:
        return bool(self.__number)


class Order:
    """订单：组合若干订单详情，并聚合其支付记录。"""

    def __init__(self, create_date: date) -> None:
        self.__createDate = create_date
        self.__status = OrderStatus.CREATE
        self.__details: list[OrderDetail] = []     # 组合 1..*
        self.__payments: list[Payment] = []         # 聚合 0..*

    @property
    def createDate(self) -> date:
        return self.__createDate

    @property
    def status(self) -> OrderStatus:
        return self.__status

    def setStatus(self, status: OrderStatus) -> None:
        self.__status = status

    def addDetail(self, detail: OrderDetail) -> None:
        self.__details.append(detail)

    def addPayment(self, payment: Payment) -> None:
        self.__payments.append(payment)
        if payment.pay():
            self.__status = OrderStatus.PAID

    @property
    def details(self) -> list[OrderDetail]:
        return list(self.__details)

    @property
    def payments(self) -> list[Payment]:
        return list(self.__payments)

    def calculateSubTotal(self) -> float:
        return round(sum(d.calculateSubTotal() for d in self.__details), 2)

    def calculateWeight(self) -> float:
        return round(sum(d.calculateWeight() for d in self.__details), 2)

    def __repr__(self) -> str:
        return (
            f"Order({self.__createDate.isoformat()}, status={self.__status.value}, "
            f"subtotal={self.calculateSubTotal()})"
        )


class Customer:
    """客户：1 个客户对应 0..* 个订单。"""

    def __init__(self, name: str, contact: str, delivery_address: str) -> None:
        self.__name = name
        self.__contact = contact
        self.__deliveryAddress = delivery_address
        self.__active = True
        self.__orders: list[Order] = []

    @property
    def name(self) -> str:
        return self.__name

    @property
    def active(self) -> bool:
        return self.__active

    def activate(self) -> None:
        self.__active = True

    def deactivate(self) -> None:
        self.__active = False

    def placeOrder(self, order: Order) -> None:
        if not self.__active:
            raise RuntimeError("客户未激活，不能下单")
        self.__orders.append(order)

    @property
    def orders(self) -> list[Order]:
        return list(self.__orders)

    def __repr__(self) -> str:
        return f"Customer({self.__name}, active={self.__active}, orders={len(self.__orders)})"
