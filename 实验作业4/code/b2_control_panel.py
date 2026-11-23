# -*- coding: utf-8 -*-
"""B2 SafeHome 控制面板 ControlPanel 的状态机实现。

状态图见实验报告 B2：读取键入字符、验证密码、系统功能选择、锁定四个状态。
密码固定为 4 位；连续输错 3 次锁定，锁定满 120 秒后允许重新输入。
"""

READING = "读取键入字符"
VERIFYING = "验证密码"
SELECTING = "系统功能选择"
LOCKED = "锁定"

STATE_NAMES = {
    READING: "读取键入字符",
    VERIFYING: "验证密码",
    SELECTING: "系统功能选择",
    LOCKED: "锁定",
}

PASSWORD = "1234"
PASSWORD_LEN = 4
MAX_FAILURES = 3
LOCK_SECONDS = 120


class ControlPanel(object):
    """SafeHome 控制面板：键盘输入、密码验证、锁定计时。"""

    def __init__(self, password=PASSWORD):
        self.password = password
        self.state = READING          # 初始伪状态 -> 读取键入字符
        self.buffer = ""
        self.failures = 0
        self.locked_seconds = 0
        self.history = []
        self._record("上电：初始状态 -> 读取键入字符")

    # ------------------------------------------------------------ 内部
    def _record(self, event):
        self.history.append({"state": self.state, "buffer": self.buffer,
                             "failures": self.failures, "event": event})

    def _to(self, new_state, event):
        self.state = new_state
        self._record(event)

    # ------------------------------------------------------------ 键盘事件
    def press(self, key):
        """户主敲击一个字符键。"""
        if self.state == LOCKED:
            self._record("面板已锁定，忽略按键 %r" % key)
            return
        if self.state == SELECTING:
            self._record("当前处于功能选择状态，按键 %r 被忽略" % key)
            return

        if self.state == READING:
            if len(self.buffer) < PASSWORD_LEN:
                self.buffer += key
                self._record("按键 %r：保存字符（%d/%d）" % (key, len(self.buffer), PASSWORD_LEN))
            if len(self.buffer) == PASSWORD_LEN:
                self._verify()

    def _verify(self):
        """输入达到 4 位后比较密码。"""
        self._to(VERIFYING, "字符数达到 4：读取键入字符 -> 验证密码")
        if self.buffer == self.password:
            self.failures = 0
            self.buffer = ""
            self._to(SELECTING, "密码正确：验证密码 -> 系统功能选择")
        else:
            self.failures += 1
            if self.failures >= MAX_FAILURES:
                self.buffer = ""
                self._to(LOCKED, "连续错误 %d 次：验证密码 -> 锁定" % self.failures)
                self.locked_seconds = 0
            else:
                self.buffer = ""
                self._to(READING, "密码错误且失败次数 %d < %d：验证密码 -> 读取键入字符"
                         % (self.failures, MAX_FAILURES))

    # ------------------------------------------------------------ 计时事件
    def tick(self, seconds):
        """锁定计时；满 120 秒自动解锁并重置失败次数。"""
        if self.state != LOCKED:
            return
        self.locked_seconds += seconds
        if self.locked_seconds >= LOCK_SECONDS:
            self.failures = 0
            self.locked_seconds = 0
            self._to(READING, "锁定超过 %d 秒：锁定 -> 读取键入字符，重置失败次数" % LOCK_SECONDS)

    # ------------------------------------------------------------ 功能操作
    def exit_function_select(self):
        """退出功能选择，回到读取键入字符。"""
        if self.state == SELECTING:
            self._to(READING, "退出功能选择：系统功能选择 -> 读取键入字符")

    def __str__(self):
        return "状态=%s 已输入=%r 失败次数=%d" % (
            STATE_NAMES[self.state], self.buffer, self.failures)
