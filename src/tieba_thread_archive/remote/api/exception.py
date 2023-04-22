__all__ = ("TiebaApiError",)


class TiebaApiError(Exception):
    def __init__(self, code: int, message: str):
        super().__init__(message)
        self.code = code
