
class GlanceBaseException(Exception):
    pass


class GlanceLookOpenError(GlanceBaseException):
    def __init__(self):
        self.message = "Attempting to access an open look for computation. Did you remember to close it?"
