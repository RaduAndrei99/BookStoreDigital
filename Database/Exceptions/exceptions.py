class OutOfStockException(Exception):
    def __init__(self, message):
        self.message = message

class EmailAlreadyExistsException(Exception):
    def __init__(self, message):
        self.message = message

class WrongPasswordException(Exception):
    def __init__(self, message):
        self.message = message

class EmailNotFoundException(Exception):
    def __init__(self, message):
        self.message = message

class BookNotFoundException(Exception):
    def __init__(self, message):
        self.message = message