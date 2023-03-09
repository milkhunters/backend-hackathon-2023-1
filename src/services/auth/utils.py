import time
from functools import wraps
from typing import Union

from src.exceptions import AccessDenied
from src.models.enums.role import UserRole


def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def int_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')


def filters(
        roles: Union[list[UserRole], UserRole] = None,  # TODO: Error if role is not list
):
    """
    Role Filter decorator for ApplicationServices

    It is necessary that the class of the method being decorated has a field '_current_user'

    :param roles: user role
    :return: decorator
    """

    # if roles is None:
    #     roles = [role for role in UserRole]
    # if not isinstance(roles, list):
    #     roles = list().append(roles)

    if not isinstance(roles, list):
        if not roles:
            roles = [role for role in UserRole]
        else:
            roles = [roles]
    else:
        roles = roles.copy()

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):

            service_class: object = args[0]
            current_user = service_class.__getattribute__('_current_user')
            if not current_user:
                raise ValueError('AuthMiddleware not found')

            if current_user.role in roles:
                return await func(*args, **kwargs)
            else:
                raise AccessDenied('User has no access')

        return wrapper

    return decorator
