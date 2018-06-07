from smbus2 import SMBus
from sched import scheduler
from i2c.i2c_module import I2CModule
import time
import logging
from threading import Timer

logger = logging.Logger(__name__)


class BoxLock(I2CModule):

    def __init__(self, bus, addr=0x39):
        super().__init__(bus, addr)
        self._open = False
        self.write_byte(0xFF)
        self.scheduler = scheduler(time.time, time.sleep)
        self.timer = Timer(0, self.close)

    @property
    def powered(self):
        return bool(self.read_byte()[1] & 0x40)

    def open(self):
        if self._open:
            if not self.timer.is_alive():
                logger.error('Lock open and timer not running! Closing.')
                self.close()
        else:
            s = self.write_byte(0x7F)
            if s:
                self._open = True
                self.timer = Timer(2, self.close)
                self.timer.start()

    def close(self):
        s = self.write_byte(0xFF)
        if s:
            self._open = False
        else:
            logger.error('Solenoid close failed!!!!')
            self.timer = Timer(1, self.close)
            self.timer.start()


def main():
    bus = SMBus(1)
    lock = BoxLock(bus)
    while True:
        print('Powered: {}'.format(lock.powered))
        if lock.powered:
            lock.open()
            print('lock opened')
        time.sleep(10)


if __name__ == '__main__':
    main()