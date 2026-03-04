from src.core.exceptions.base import BaseServiceError


class ConflictError(BaseServiceError):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            code="conflict",
            status_code=409,
        )


class NotFoundError(BaseServiceError):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            code="not_found",
            status_code=404,
        )


class ColorNotFoundError(NotFoundError):
    def __init__(self, name: str):
        super().__init__(message=f"Цвет '{name}' не найден")


class ColorAlreadyExistsError(ConflictError):
    def __init__(self, name: str):
        super().__init__(message=f"Цвет '{name}' уже существует")


class ColorAssignNotFoundError(NotFoundError):
    def __init__(self, assign_id: int):
        super().__init__(message=f"Назначение с ID {assign_id} не найдено")


class ColorAssignAlreadyExistsError(ConflictError):
    def __init__(self, key: str, color: str):
        super().__init__(message=f"Назначение с ключом '{key}' и цветом '{color}' уже существует")


class ColorAssignForeignKeyViolationError(ConflictError):
    def __init__(self, color: str):
        super().__init__(message=f"Цвет '{color}' не существует в таблице color")


# === Price Errors ===


class PriceNotFoundError(NotFoundError):
    def __init__(self, price_id: int):
        super().__init__(message=f"Прайс с ID {price_id} не найден")


class PriceAlreadyExistsError(ConflictError):
    def __init__(self, category: str, supplier: str, region: str):
        super().__init__(
            message=f"Прайс для категории '{category}', поставщика '{supplier}' и региона '{region}' уже существует"
        )


class PriceForeignKeyViolationError(ConflictError):
    def __init__(self):
        super().__init__(message="Нарушение внешней ссылки при операции с прайсом")
