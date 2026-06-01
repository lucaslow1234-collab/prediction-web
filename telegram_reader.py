```python
import requests
import re
from bs4 import BeautifulSoup


URL = "https://t.me/s/pc28"


def fetch_history():

    try:

        headers = {
            "User-Agent":
            "Mozilla/5.0"
        }

        response = requests.get(
            URL,
            headers=headers,
            timeout=20
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Telegram messages
        messages = soup.find_all(
            "div",
            class_=
            "tgme_widget_message_text"
        )

        history = []

        for msg in messages:

            text = msg.get_text(
                "\n",
                strip=True
            )

            match = re.search(
                r"(小单|大单|小双|大双)",
                text
            )

            if match:
                history.append(
                    match.group(1)
                )

        # keep latest 100
        history = history[-100:]

        if not history:
            print(
                "No results found"
            )
            return

        with open(
            "history.txt",
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

    except Exception as e:

        print(
            "Telegram error:",
            str(e)
        )


fetch_history()
```
