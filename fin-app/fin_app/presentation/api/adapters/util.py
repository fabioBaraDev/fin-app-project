from uuid import UUID


def is_valid_uuid(id):
    try:
        UUID(id)
        return True
    except ValueError:
        return False
