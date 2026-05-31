```python
from telethon.sync import TelegramClient
import re
import os

api_id = int(
    os.environ.get("API_ID")
)

api_hash = os.environ.get(
    "API_HASH"
)

channel = "pc28"

SAVE_FILE = "history.txt"


def extract_category(text):

    match = re.search(
        r'(小单|大单|小双|大双)',
        text
    )

    if match:
        return match.group(1)

    return None


with TelegramClient(
    "session",
    api_id,
    api_hash
) as client:

    messages = client.get_messages(
        channel,
        limit=100
    )

    history = []

    for msg in reversed(messages):

        if not msg.text:
            continue

        cat = extract_category(
            msg.text
        )

        if cat:
            history.append(cat)

    with open(
        SAVE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            "\n".join(history)
        )

    print(
        "Saved",
        len(history),
        "rounds"
    )
```
