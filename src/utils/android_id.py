import secrets

__all__ = ("generate_android_id",)


def generate_android_id():
    return secrets.token_hex(16)
