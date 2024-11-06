import ulid

from common_constants.support import MASKED_ID

def generate_unique_id():
    generated = str(ulid.ULID())
    while generated == MASKED_ID:
        generated = str(ulid.ULID())
    return generated

def validate_ulid(inp: str):
    try:
        ulid.ULID.from_str(inp)
        return True
    except:
        return False