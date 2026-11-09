# -*- coding: utf-8 -*-
"""实验三 A1-1 ~ A1-4 的对象模型演示程序。

运行：python demo.py
"""

from datetime import date

from a1_1_thoroughbred import Thoroughbred
from a1_2_college import Building, College, Course
from a1_3_school import Department, Instructor, School, Student, Subject
from a1_4_shopping import (
    AliPay,
    Cash,
    Credit,
    Customer,
    Order,
    OrderDetail,
    OrderStatus,
    Product,
    WeixinPay,
    WireTransfer,
)


def demo_a1_1() -> None:
    print("=" * 62)
    print("A1-1 Thoroughbred 类")
    sire = Thoroughbred(date(2014, 3, 20))
    dam = Thoroughbred(date(2016, 5, 1))
    foal = Thoroughbred(date(2021, 4, 12), mother=dam, father=sire)
    print("  father :", foal.getFather())
    print("  mother :", foal.getMother())
    print("  age    :", foal.getCurrentAge(), "岁")


def demo_a1_2() -> None:
    print("=" * 62)
    print("A1-2 College / Building / Course（聚合、组合与约束）")
    college = College("计算机学院")
    b1 = Building("实验楼 A")
    b2 = Building("教学楼 B")
    college.addBuilding(b1)
    c1 = Course("软件工程", b1)
    c2 = Course("数据库原理", b2)     # b2 尚未加入学院，addCourse 会自动补上
    college.addCourse(c1)
    college.addCourse(c2)
    print(" ", college)
    print("  课程:", college.courses)
    # 聚合：Building 可独立存在
    college.removeBuilding(b1)
    print("  移除实验楼 A 后 Building 依然存在:", b1)
    # 组合：移除课程即销毁
    college.removeCourse(c2)
    print("  课程被组合销毁:", c2, "destroyed =", c2.destroyed)


def demo_a1_3() -> None:
    print("=" * 62)
    print("A1-3 School / Department / Instructor / Subject / Student")
    school = School("人工智能与计算机学院")
    cs = Department("计算机科学系")
    se = Department("软件工程系")

    s_prog = Subject("程序设计基础")
    s_ds = Subject("数据结构")
    s_se = Subject("软件工程")
    s_db = Subject("数据库原理")

    t1 = Instructor("张老师")
    t2 = Instructor("李老师")
    cs.addInstructor(t1)
    se.addInstructor(t2)
    cs.offerSubject(s_prog)
    cs.offerSubject(s_ds)
    se.offerSubject(s_se)
    se.offerSubject(s_db)

    t1.teach(s_prog)
    t1.teach(s_ds)
    t2.teach(s_se)

    stu = Student("胡梓俊")
    stu.enroll(s_prog)
    stu.enroll(s_se)

    school.addDepartment(cs)
    school.addDepartment(se)
    school.addStudent(stu)
    school.validate()
    print(" ", school)
    print("  系:", school.departments)
    print("  学生课程:", stu.subjects)
    try:
        for extra in ("a", "b", "c", "d"):
            stu.enroll(Subject(f"选修{extra}"))
    except ValueError as exc:
        print("  多重性校验生效:", exc)


def demo_a1_4() -> None:
    print("=" * 62)
    print("A1-4 网上购物系统")
    customer = Customer("胡梓俊", "138-0000-0000", "江苏省镇江市")
    order = Order(date(2026, 11, 9))

    p1 = Product("机械键盘", 0.9, "87 键机械键盘", 399.0)
    p2 = Product("UML 建模指南", 0.6, "教材", 59.0)
    order.addDetail(OrderDetail(p1, 1))
    order.addDetail(OrderDetail(p2, 2))
    customer.placeOrder(order)

    print(" ", customer)
    print(" ", order)
    print("  明细小计:", [d.calculateSubTotal() for d in order.details])
    print("  总重量  :", order.calculateWeight())

    payments = [
        Credit(order.calculateSubTotal(), "6222-0000-1111-2222", "Visa", date(2029, 1, 1)),
        Cash(order.calculateSubTotal(), 600.0),
        WireTransfer(order.calculateSubTotal(), "ICBC-001", "工商银行"),
        AliPay(order.calculateSubTotal(), "alipay@example.com"),
        WeixinPay(order.calculateSubTotal(), "wx_0001"),
    ]
    for payment in payments:
        order.addPayment(payment)
        print(f"  {payment!r:>48} -> pay() = {payment.pay()}")
    print("  订单状态:", order.status.value)
    order.setStatus(OrderStatus.SHIPPING)
    print("  更新状态:", order.status.value)


if __name__ == "__main__":
    demo_a1_1()
    demo_a1_2()
    demo_a1_3()
    demo_a1_4()
    print("=" * 62)
    print("演示结束。")
