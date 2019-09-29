class GlanceBaseException(Exception):
    pass


class GlanceLookOpenError(GlanceBaseException):
    """
    Error for handling looks that are open and being used in computation.
    """
    def __init__(self, look=None):
        self.message = "Attempting to access an open look for computation. Did you remember to close it?"
        if look:
            self.look = look


class GlanceLookNotFoundError(GlanceBaseException):
    """
    Error for when a look cannot be found.
    """
    def __init__(self, look_id: str):
        self.message = f"The look with id: {look_id} could not be found."


class GlanceLookClosedError(GlanceBaseException):
    """
    Error for when given Look is already closed.
    """
    def __init__(self, look = None):
        self.message = "The given look is already closed. Are you sure you want to overwrite the current end time?"
        if look:
            self.look = look


class GlanceWatchOpenError(GlanceBaseException):
    """
    Error for handling watches that are open and being used in computation.
    """
    def __init__(self, watch=None):
        self.message = "Attempting to access an open watch for computation. Did you remember to close it?"
        if watch:
            self.watch = watch


class GlanceWatchNotFoundError(GlanceBaseException):
    """
    Error for when a look cannot be found.
    """
    def __init__(self, watch_target: str):
        self.message = f"The watch with target: {watch_target} could not be found."


class GlanceWatchClosedError(GlanceBaseException):
    """
    Error for when given watch is already closed.
    """
    def __init__(self, watch = None):
        self.message = "The given watch is already closed. Are you sure you want to overwrite the current end time?"
        if watch:
            self.watch = watch


class GlanceClosedError(GlanceBaseException):
    """
    Error for glance already closed.
    """
    def __init__(self):
        self.message = "Glance is already closed. Are you sure you want to overwrite the current end time?"


class GlanceWatchExistsError(GlanceBaseException):
    """
    Error gor glance already containing a given watch.
    """
    def __init__(self, watch_target: str):
        self.message = f"Given watch with target: {watch_target} already exists."
