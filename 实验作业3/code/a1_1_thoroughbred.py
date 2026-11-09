# -*- coding: utf-8 -*-
"""A1-1 用 Thoroughbred 类对优良品质的马进行建模。

UML 对应（见实验报告 A1-1）：
    Thoroughbred
    - mother : Thoroughbred
    - father : Thoroughbred
    - birthyear : Date
    + getCurrentAge() : Integer
    + getFather() : Thoroughbred
    + getMother() : Thoroughbred
"""

from __future__ import annotations

from datetime import date


class Thoroughbred:
    """一匹优良品质的马：记录其父母与出生年份，并可推算年龄。"""

    def __init__(
        self,
        birthyear: date,
        mother: "Thoroughbred | None" = None,
        father: "Thoroughbred | None" = None,
    ) -> None:
        # 三个属性全部为私有（UML 中前缀 "-"），只能通过操作访问
        self.__birthyear = birthyear
        self.__mother = mother
        self.__father = father

    # ---- 操作（公有，UML 中前缀 "+"） ----
    def getCurrentAge(self) -> int:
        """按出生年份计算当前年龄（周岁）。"""
        today = date.today()
        age = today.year - self.__birthyear.year
        # 生日尚未到则减一岁
        if (today.month, today.day) < (self.__birthyear.month, self.__birthyear.day):
            age -= 1
        return max(age, 0)

    def getFather(self) -> "Thoroughbred | None":
        return self.__father

    def getMother(self) -> "Thoroughbred | None":
        return self.__mother

    # ---- Python 侧的只读属性，便于打印；不改变 UML 的私有语义 ----
    @property
    def birthyear(self) -> date:
        return self.__birthyear

    def __repr__(self) -> str:  # 便于演示输出
        return f"Thoroughbred(birthyear={self.__birthyear.isoformat()})"
