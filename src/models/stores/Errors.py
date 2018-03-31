class StoreErrors(Exception):
    def __init__(self, massage):
        self.massage = massage


class StoreNotFoundException(StoreErrors):
    pass