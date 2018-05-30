from functools import wraps


class I2CModule:

    def __init__(self, bus, addr):
        self.bus = bus
        self.addr = addr

    def _write_except(f):
        @wraps(f)
        def wrapped(inst, *args, **kwargs):
            try:
                f(inst, *args, **kwargs)
            except OSError:
                print('i2c write error')
                return False
            return True

        return wrapped

    def _read_except(f):
        @wraps(f)
        def wrapped(inst, *args, **kwargs):
            result = None
            try:
                result = f(inst, *args, **kwargs)
            except OSError:
                print('i2c read error')
                return False, None
            return True, result

        return wrapped

    @_write_except
    def write_byte(self, byte):
        try:
            self.bus.write_byte(self.addr, byte)
        except OSError:
            self.i2c_error()
            return False
        return True

    @_write_except
    def write_reg_byte(self, reg, byte):
        self.bus.write_byte_data(self.addr, reg, byte)

    @_write_except
    def write_reg_bytes(self, reg, data):
        self.bus.write_i2c_block_data(self.addr, reg, data)

    @_read_except
    def read_byte(self):
        return self.bus.read_byte(self.addr)

    @_read_except
    def read_reg_byte(self, reg):
        return self.bus.read_byte_data(self.addr, reg)

    @_read_except
    def read_reg_bytes(self, reg, n=32):
        return self.bus.read_i2c_block_data(self.addr, reg, n)
