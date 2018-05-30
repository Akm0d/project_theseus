class MockGPIO(object):
    BCM = 0
    IN = 0

    @staticmethod
    def setmode(bcm):
        return 0

    @staticmethod
    def setup(*args, **kwargs):
        return 0

    @staticmethod
    def cleanup(*args, **kwargs):
        return 0

    @staticmethod
    def wait_for_edge(*args, **kwargs):
        return 0
