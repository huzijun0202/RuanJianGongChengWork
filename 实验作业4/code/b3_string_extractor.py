# -*- coding: utf-8 -*-
"""B3 从源文件文本中提取字符串的状态机实现。

状态图见实验报告 B3：普通文本、字符串内、转义三个状态。
字符串由一对双引号界定；字符串内的反斜杠会转义下一个字符，
例如 "输出 \\"Hello World!\\"" 提取结果为 输出 "Hello World!"。
"""

NORMAL = "普通文本"
IN_STRING = "字符串内"
ESCAPE = "转义"


class StringExtractor(object):
    """字符串提取状态机：逐字符扫描，输出所有字符串的内容（已去转义）。"""

    def __init__(self):
        self.state = NORMAL
        self.results = []
        self.current = []
        self.history = []
        self._record("输入开始：初始状态 -> 普通文本")

    def _record(self, event):
        self.history.append({"state": self.state,
                             "in_string": "".join(self.current), "event": event})

    def feed(self, text):
        """逐字符驱动状态机。"""
        for ch in text:
            self._step(ch)
        self._finish()
        return self.results

    def _step(self, ch):
        if self.state == NORMAL:
            if ch == '"':
                self.current = []
                self.state = IN_STRING
                self._record("遇到起始双引号：普通文本 -> 字符串内")
            else:
                self._record("字符 %r 不是双引号：原样输出" % ch)

        elif self.state == IN_STRING:
            if ch == "\\":
                self.state = ESCAPE
                self._record("遇到反斜杠：字符串内 -> 转义")
            elif ch == '"':
                self.results.append("".join(self.current))
                self.state = NORMAL
                self.current = []
                self._record("遇到结束双引号：字符串内 -> 普通文本，输出字符串")
            else:
                self.current.append(ch)
                self._record("普通字符 %r：追加字符" % ch)

        elif self.state == ESCAPE:
            self.current.append(ch)
            self.state = IN_STRING
            self._record("转义字符 %r：转义 -> 字符串内，追加转义后的字符" % ch)

    def _finish(self):
        if self.state == IN_STRING:
            # 输入结束时字符串未闭合：按题目约定丢弃该不完整字符串
            self._record("输入结束但字符串未闭合：丢弃不完整字符串")
            self.current = []
            self.state = NORMAL


def extract_strings(source):
    """便捷函数：返回 source 中所有双引号字符串的内容。"""
    return StringExtractor().feed(source)


if __name__ == "__main__":
    demo = '一般学习一门编程语言的时候，基本上第一个程序是输出\\"Hello World!\\"'
    source = '"%s"' % demo
    print(source)
    for i, s in enumerate(extract_strings(source), 1):
        print(i, repr(s))
