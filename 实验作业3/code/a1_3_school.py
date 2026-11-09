# -*- coding: utf-8 -*-
"""A1-3 School / Department / Instructor / Subject / Student 的多重性建模。

UML 对应（见实验报告 A1-3）：
    School      <#>---- Department   1 : 1..*
    School      <>----- Student      1 : 0..*
    Department  -----  Instructor    1..* : 1..*
    Department  -----  Subject       1 : 1..*
    Instructor  -----  Subject       * : 1..3
    Student     -----  Subject       * : 1..5

实现时用校验保证题设的多重性约束：
  * 每个系至少有 1 名指导教师、至少提供 1 门课程；
  * 每位指导教师至少属于 1 个系、教授 1~3 门课程；
  * 每名学生参加 1~5 门课程；
  * 学院可以有 0 到多名学生。
"""

from __future__ import annotations


class Subject:
    def __init__(self, name: str) -> None:
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name

    def __repr__(self) -> str:
        return f"Subject({self.__name})"


class Instructor:
    """指导教师：至少属于 1 个系，教授 1~3 门课程。"""

    def __init__(self, name: str) -> None:
        self.__name = name
        self.__departments: list["Department"] = []
        self.__subjects: list[Subject] = []

    @property
    def name(self) -> str:
        return self.__name

    @property
    def departments(self) -> list["Department"]:
        return list(self.__departments)

    @property
    def subjects(self) -> list[Subject]:
        return list(self.__subjects)

    def assignToDepartment(self, department: "Department") -> None:
        if department not in self.__departments:
            self.__departments.append(department)

    def teach(self, subject: Subject) -> None:
        if len(self.__subjects) >= 3:
            raise ValueError("每位指导教师最多教授 3 门课程")
        if subject not in self.__subjects:
            self.__subjects.append(subject)

    def __repr__(self) -> str:
        return f"Instructor({self.__name}, subjects={len(self.__subjects)})"


class Student:
    """学生：参加 1~5 门课程。"""

    def __init__(self, name: str) -> None:
        self.__name = name
        self.__subjects: list[Subject] = []

    @property
    def name(self) -> str:
        return self.__name

    def enroll(self, subject: Subject) -> None:
        if len(self.__subjects) >= 5:
            raise ValueError("每名学生最多参加 5 门课程")
        if subject not in self.__subjects:
            self.__subjects.append(subject)

    @property
    def subjects(self) -> list[Subject]:
        return list(self.__subjects)

    def __repr__(self) -> str:
        return f"Student({self.__name}, subjects={len(self.__subjects)})"


class Department:
    """系：至少 1 名指导教师，至少提供 1 门课程。"""

    def __init__(self, name: str) -> None:
        self.__name = name
        self.__instructors: list[Instructor] = []
        self.__subjects: list[Subject] = []

    @property
    def name(self) -> str:
        return self.__name

    def addInstructor(self, instructor: Instructor) -> None:
        if instructor not in self.__instructors:
            self.__instructors.append(instructor)
        instructor.assignToDepartment(self)

    def offerSubject(self, subject: Subject) -> None:
        if subject not in self.__subjects:
            self.__subjects.append(subject)

    def validate(self) -> None:
        """检查题设的多重性：1..* 指导教师、1..* 课程。"""
        if not self.__instructors:
            raise ValueError(f"系 {self.__name} 至少需要 1 名指导教师")
        if not self.__subjects:
            raise ValueError(f"系 {self.__name} 至少需要提供 1 门课程")

    @property
    def instructors(self) -> list[Instructor]:
        return list(self.__instructors)

    @property
    def subjects(self) -> list[Subject]:
        return list(self.__subjects)

    def __repr__(self) -> str:
        return (
            f"Department({self.__name}, instructors={len(self.__instructors)}, "
            f"subjects={len(self.__subjects)})"
        )


class School:
    """学院：组合 Department（1..*），聚合 Student（0..*）。"""

    def __init__(self, name: str) -> None:
        self.__name = name
        self.__departments: list[Department] = []   # 组合 1..*
        self.__students: list[Student] = []          # 聚合 0..*

    @property
    def name(self) -> str:
        return self.__name

    def addDepartment(self, department: Department) -> None:
        if department not in self.__departments:
            self.__departments.append(department)

    def addStudent(self, student: Student) -> None:
        if student not in self.__students:
            self.__students.append(student)

    def removeStudent(self, student: Student) -> None:
        """解除聚合：学生离开学院但仍然存在。"""
        if student in self.__students:
            self.__students.remove(student)

    def validate(self) -> None:
        if not self.__departments:
            raise ValueError("学院至少要有 1 个系")
        for d in self.__departments:
            d.validate()

    @property
    def departments(self) -> list[Department]:
        return list(self.__departments)

    @property
    def students(self) -> list[Student]:
        return list(self.__students)

    def __repr__(self) -> str:
        return (
            f"School({self.__name}, departments={len(self.__departments)}, "
            f"students={len(self.__students)})"
        )
