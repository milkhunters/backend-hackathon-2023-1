from enum import Enum, unique


@unique
class UserRole(int, Enum):
    GUEST = 1
    BANNED = 2
    USER = 3
    ADMIN = 4
