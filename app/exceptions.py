from fastapi import HTTPException, status

class BookingException(HTTPException):
    status_code = 500 # <-- задаем значения по умолчанию
    detail = ""
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="Пользователь уже существует"


class IncorrectEmailOrPasswordException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неверная почта или пароль"


class TokenExpiredException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Токен истек"


class TokenAbsentException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Нет Токена"


class IncorrectTokenFormatException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Некорректный формат Токена"


class UserIsNotPresentException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Такого пользователя нет"

class RoomCannotBeException(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="Комната не забронирована"
