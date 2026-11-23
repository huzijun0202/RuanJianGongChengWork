# -*- coding: utf-8 -*-
"""实验四演示程序：依次运行 B1、B2、B3 三个状态机模型。"""
import io
import sys

from b1_water_tank import WaterTank
from b2_control_panel import ControlPanel
from b3_string_extractor import StringExtractor, extract_strings


def show(title):
    print("\n" + "=" * 66)
    print(title)
    print("=" * 66)


def demo_b1():
    show("B1 恒温水箱状态机")
    tank = WaterTank()
    print("启动:", tank)
    tank.sensor(15, True)        # 温度低于 20 且有水 -> 加热
    print("采样(15℃, 有水):", tank)
    tank.sensor(60, True)        # 加热中，未到 100 -> 保持加热
    print("采样(60℃, 有水):", tank)
    tank.sensor(100, True)       # 达到 100 -> 断电回到待机
    print("采样(100℃, 有水):", tank)
    tank.sensor(18, False)       # 低于 20 但无水 -> 不加热
    print("采样(18℃, 无水):", tank)
    tank.sensor(18, True)
    tank.breakdown()             # 水箱烧坏 -> 维修
    print("水箱烧坏:", tank)
    tank.repair_done()           # 维修完成 -> 待机
    print("维修完成:", tank)
    tank.clock(23)               # 23:00 -> 休眠
    print("23:00:", tank)
    tank.clock(7)                # 7:00 -> 恢复恒温过程
    print("7:00:", tank)
    print("\n状态迁移过程：")
    for h in tank.history:
        print("  [%s] 继电器=%s  %s" % (h["state"], "开" if h["relay"] else "关", h["event"]))


def demo_b2():
    show("B2 SafeHome 控制面板状态机")
    panel = ControlPanel("1234")
    print("上电:", panel)
    for key in "1234":
        panel.press(key)
    print("输入 1234:", panel)
    panel.exit_function_select()
    print("退出功能选择:", panel)
    for _ in range(3):
        for key in "0000":
            panel.press(key)
    print("连续输错 3 次:", panel)
    panel.press("1")
    print("锁定期间按键:", panel)
    panel.tick(60)
    print("锁定 60 秒:", panel)
    panel.tick(60)
    print("锁定 120 秒:", panel)
    for key in "1234":
        panel.press(key)
    print("重新输入正确密码:", panel)
    print("\n状态迁移过程：")
    for h in panel.history:
        print("  [%s] 失败次数=%d  %s" % (h["state"], h["failures"], h["event"]))


def demo_b3():
    show("B3 源文件字符串提取状态机")
    source = '"一般学习一门编程语言的时候，基本上第一个程序是输出\\"Hello World!\\""'
    print("源文本：", source)
    extractor = StringExtractor()
    result = extractor.feed(source)
    print("提取结果：", result)
    assert result == ['一般学习一门编程语言的时候，基本上第一个程序是输出"Hello World!"']

    source2 = 'print("Hello \\"Rose\\" and \\"World\\"");'
    print("\n源文本：", source2)
    print("提取结果：", extract_strings(source2))
    assert extract_strings(source2) == ['Hello "Rose" and "World"']

    print("\n状态迁移过程（第一条源文本）：")
    for h in extractor.history:
        print("  [%s] %s  %s" % (h["state"], h["in_string"], h["event"]))


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    demo_b1()
    demo_b2()
    demo_b3()
    print("\n全部演示完成。")
