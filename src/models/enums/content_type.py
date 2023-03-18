from enum import Enum, unique


@unique
class ContentType(Enum):
    """
    Типы контента
    """
    IMAGE_JPEG = "image/jpeg"
    IMAGE_PNG = "image/png"
    DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    DOC = "application/msword"
    PDF = "application/pdf"
    XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    XLS = "application/vnd.ms-excel"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
