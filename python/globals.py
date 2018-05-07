# Singleton/BorgSingleton.py
# Alex Martelli's 'Borg'
class Borg:
    _shared_state = {}
    def __init__(self):
        self.__dict__ = self._shared_state

class ComQueue(Borg):
    def __init__(self):
        Borg.__init__(self)

    def setComQueue(self, arg):
        self.val = arg

    def getComQueue(self):
        return self.val
    # def __str__(self): return self.val
