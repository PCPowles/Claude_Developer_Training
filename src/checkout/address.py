import re


class AddressValidationError(Exception):
    pass


def validate_postal_code(code):
    if not re.fullmatch(r"\d{5}(-\d{4})?", code):
        raise AddressValidationError("postal code format not recognised")
    return code
