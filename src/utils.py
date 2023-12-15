import re
from typing import Optional


def extract_version_string(text: str, custom_regex: str | None = None) -> Optional[str]:
    """
    Extract the SemVer from an input string. Returns none if no match can be found.
    Can be overridden using a custom regex pattern.

    Example: 'v11.22.33-beta' -> '11.22.33' or 'no version here' -> None
    :param text: Input string
    :param custom_regex: Custom regex definition to overwrite the existing one.
    :return: SemVer string or None
    """
    if custom_regex:
        pattern = re.compile(custom_regex)
    else:
        pattern = re.compile("(v?\\d+\\.\\d+\\.\\d+)")
    match = pattern.search(text)
    if match:
        return match.group(1)
    else:
        return None
