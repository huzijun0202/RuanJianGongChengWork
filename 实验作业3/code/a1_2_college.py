# -*- coding: utf-8 -*-
"""A1-2 College / Building / Course 的聚合、组合与约束。

UML 对应（见实验报告 A1-2）：
    College  <>----  Building   聚合（aggregation） 1 : 1..*
    College  <#>---- Course     组合（composition） 1 : 1..*
    约束注释：{Course 一定在某个 Building 中进行}

语义要点：
  * 聚合：Building 可以脱离 College 独立存在（弱拥有），College 被删除时
    Building 仍然保留，只是不再属于该学院；
  * 组合：Course 的生命周期由 College 决定（强拥有），College 被删除时
    其课程一并销毁；
  * 约束：任何 Course 在加入 College 之前必须先归属某个 Building，
    否则违反 "{Course 一定在某个 Building 中进行}"。
"""

from __future__ import annotations


class Building:
    """教学楼（可独立存在）。"""

    def __init__(self, name: str) -> None:
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name

    def __repr__(self) -> str:
        return f"Building({self.__name})"


class Course:
    """课程；必须确定在某栋 Building 中进行（约束调用方保证）。"""

    def __init__(self, name: str, building: Building) -> None:
        if not isinstance(building, Building):
            raise TypeError("Course 必须位于某个 Building 中")
        self.__name = name
        self.__building = building
        self.__destroyed = False

    def _mark_destroyed(self) -> None:
        self.__destroyed = True

    @property
    def destroyed(self) -> bool:
        return self.__destroyed

    @property
    def name(self) -> str:
        return self.__name

    @property
    def building(self) -> Building:
        return self.__building

    def __repr__(self) -> str:
        return f"Course({self.__name} @ {self.__building.name})"


class College:
    """学院：聚合 Building（可独立存在），组合 Course（同生共死）。"""

    def __init__(self, name: str) -> None:
        self.__name = name
        self.__buildings: list[Building] = []   # 聚合端 1..*
        self.__courses: list[Course] = []        # 组合端 1..*

    # ---- 聚合：Building ----
    def addBuilding(self, building: Building) -> None:
        if building not in self.__buildings:
            self.__buildings.append(building)

    def removeBuilding(self, building: Building) -> None:
        """解除聚合关系；Building 本身仍然存活。"""
        if building in self.__buildings:
            self.__buildings.remove(building)

    # ---- 组合：Course ----
    def addCourse(self, course: Course) -> None:
        # 约束 {Course 一定在某个 Building 中进行}
        if course.building not in self.__buildings:
            self.addBuilding(course.building)
        self.__courses.append(course)

    def removeCourse(self, course: Course) -> None:
        """从组合中移除并销毁课程。"""
        if course in self.__courses:
            self.__courses.remove(course)
        course._mark_destroyed()  # 组合中的部分对象随整体销毁

    @property
    def buildings(self) -> list[Building]:
        return list(self.__buildings)

    @property
    def courses(self) -> list[Course]:
        return list(self.__courses)

    def __repr__(self) -> str:
        return (
            f"College({self.__name}, buildings={len(self.__buildings)}, "
            f"courses={len(self.__courses)})"
        )
