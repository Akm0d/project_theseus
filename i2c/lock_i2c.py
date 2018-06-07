from smbus2 import SMBus
from sched import scheduler
from i2c.i2c_module import I2CModule
import time
import logging

logger = logging.Logger(__name__)


class BoxLock(I2CModule):

    def __init__(self, bus, addr=0x39):
        super().__init__(bus, addr)
        self._open = False
        self.write_byte(0xFF)
        self.scheduler = scheduler(time.time, time.sleep)

    @property
    def powered(self):
        return bool(self.read_byte()[1] & 0x40)

    def open(self):
        self._open = True
        s = self.write_byte(0x7F)
        if s:
            self.scheduler.enter(10, 1, self.close)
            self.scheduler.run(blocking=False)

    def close(self):
        s = self.write_byte(0xFF)
        if s:
            self._open = False
        else:
            logger.error('Solenoid close failed!!!!')
            self.scheduler.enter(10, 1, self.close)
            self.scheduler.run(blocking=False)


def main():
    bus = SMBus(1)
    lock = BoxLock(bus)
    while True:
        print('Powered: {}'.format(lock.powered))
        lock.open()
        time.sleep(10)


if __name__ == '__main__':
    main()