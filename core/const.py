# -*- coding: utf-8 -*-

class const:
    """
    save global variables so that every threads can read/change it
    """
    LEFT = -1
    RIGHT = 1

    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const (%s)" % name)
