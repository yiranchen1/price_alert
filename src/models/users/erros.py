
class UserError(Exception):
    def __init__(self, massage):
        self.massage = massage


class UserNotExistError(UserError):
    pass

class IncorrectPasswordError(UserError):
    pass

class UserAlreadyRegisteredError(UserError):
    pass

class InvalidEmailError(UserError):
    pass