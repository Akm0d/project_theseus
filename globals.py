# The following two classes handle allowing any Resource from the Flask app
# to be able to communicate with the Logic Process. In setup.py, the Logic
# process is forked to another process, and communication is handled via a
# process and thread proof shared queue. The Borg class that ComQueue inherits
# from ensures that all instances of ComQueue have the same state.

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
