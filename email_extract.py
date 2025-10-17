import re
from typing import List

EMAIL_RE = re.compile(
    r"""
    (?P<email>
        [a-zA-Z0-9._%+-]+      # local part
        @
        [a-zA-Z0-9.-]+         # domain
        \.
        [a-zA-Z]{2,}           # TLD
    )
    """,
    re.VERBOSE,
)

def extract_emails(text: str) -> List[str]:
    return [m.group("email") for m in EMAIL_RE.finditer(text)]
