from typing import Optional

from rest_framework import status


class FinAppError(Exception):
    def __init__(
        self,
        type,
        errors=None,
        error_status=500,
        message="unexpected error",
    ):
        self.type = type
        self.error_status = error_status
        self.errors = errors
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        message = f"{self.type} -> {self.message}"
        if self.errors:
            return message + f" -> {self.errors}"

        return message


class AccountNotFoundError(FinAppError):
    def __init__(self, type, message: Optional[str] = "account not found error"):
        super().__init__(type, error_status=status.HTTP_404_NOT_FOUND, message=message)
