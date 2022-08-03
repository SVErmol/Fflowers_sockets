class CustomException(Exception):
    def __init__(self, error, message):
        self.message = message
        print(message)
        super().__init__(message)


class ErrorUnauthorized(CustomException):
    def __init__(self, *args, **kwargs):
        super().__init__(message="401:Не авторизован!")


class NotFoundError(CustomException):
    def __init__(self, *args, **kwargs):
        super().__init__( message="404:Не найдено!")


class InternalServerError(CustomException):
    def __init__(self, *args, **kwargs):
        super().__init__( message="500:Внутренняя ошибка сервера!")
