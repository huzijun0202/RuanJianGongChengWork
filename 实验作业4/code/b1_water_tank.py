# -*- coding: utf-8 -*-
"""B1 恒温水箱的状态机实现。

状态图见实验报告 B1：待机、加热、维修、休眠四个状态。
温度传感器与水量传感器事件驱动状态迁移，23:00 进入休眠，7:00 恢复恒温过程。
"""

STANDBY = "待机"
HEATING = "加热"
REPAIRING = "维修"
SLEEPING = "休眠"

STATE_NAMES = {
    STANDBY: "待机",
    HEATING: "加热",
    REPAIRING: "维修",
    SLEEPING: "休眠",
}


class WaterTank(object):
    """恒温水箱控制器：只暴露传感器事件与时钟事件。"""

    def __init__(self):
        self.state = STANDBY          # 初始伪状态 -> 待机
        self.relay = False            # 继电器（加热电源）
        self.history = []
        self._record("启动：初始状态 -> 待机")

    # ------------------------------------------------------------ 内部
    def _record(self, event):
        self.history.append({
            "state": self.state,
            "relay": self.relay,
            "event": event,
        })

    def _to(self, new_state, event):
        self.state = new_state
        self._record(event)

    # ------------------------------------------------------------ 事件
    def start(self):
        """启动水箱，进入恒温烧水过程。"""
        if self.state == SLEEPING:
            self._to(STANDBY, "7:00 到达：休眠 -> 待机")

    def sensor(self, temperature, has_water):
        """温度/水量传感器采样：温度 < 20 触发加热判断，达到 100 断电。"""
        if self.state == STANDBY and temperature < 20:
            if has_water:
                self.relay = True
                self._to(HEATING, "温度 %.1f < 20 且 有水：打开继电器，待机 -> 加热" % temperature)
            else:
                self.relay = False
                self._record("温度 %.1f < 20 且 无水：不打开电源，留在待机" % temperature)
        elif self.state == HEATING:
            if temperature >= 100:
                self.relay = False
                self._to(STANDBY, "温度达到 100：断开电源，加热 -> 待机")

    def breakdown(self):
        """水箱烧坏：进入维修状态。"""
        if self.state in (STANDBY, HEATING):
            old = STATE_NAMES[self.state]
            self.relay = False
            self._to(REPAIRING, "水箱烧坏：%s -> 维修" % old)

    def repair_done(self):
        """维修完成：回到待机。"""
        if self.state == REPAIRING:
            self._to(STANDBY, "维修完成：维修 -> 待机")

    def clock(self, hour):
        """整点事件：23:00 断电休眠，7:00 恢复恒温过程。"""
        if hour == 23 and self.state in (STANDBY, HEATING):
            self.relay = False
            self._to(SLEEPING, "23:00：断开电源，%s -> 休眠" % STATE_NAMES[self.state])
        elif hour == 7 and self.state == SLEEPING:
            self._to(STANDBY, "7:00：休眠 -> 待机，自动恢复恒温过程")

    # ------------------------------------------------------------ 查询
    def __str__(self):
        on_off = "开" if self.relay else "关"
        return "状态=%s 继电器=%s" % (STATE_NAMES[self.state], on_off)
